"""Where would new measurements settle an undecided model?

`core.model_fit.near_ties` names the complexity classes a corpus does not
separate. This module answers the next question: which inputs to ask for so the
next fit is decided by evidence rather than by the tie-break.

The obvious criterion, "sample where the candidates' predictions differ most",
is wrong. Two tied candidates such as Linear and Linearithmic can differ most,
as a share of the predicted value, at n = 1. Sampling there settles nothing: at
n = 1 the linearithmic term is zero, so the whole disagreement there is about
the INTERCEPT, and the rival absorbs new points by moving it. A criterion over
fixed curves cannot see that, because it never asks what the loser would do
next.

So the criterion here is a simulated experiment. Assume each tied candidate is
true in turn, generate points in the region with the measurement noise the
harness actually achieves, REFIT every candidate on the corpus plus those
points, and count how often the fit names the candidate that generated them.
0.5 means the region is uninformative (the answer does not depend on the truth);
1.0 means it is decisive. A rival re-fitting its way out of the disagreement is
then visible, because it shows up as the fit naming the wrong model.

When the informative region lies past the largest value in the corpus, the
answer is to extend the frontier, but that is a conclusion of the method, not
an assumption in it. A subject whose informative region sits inside its range
gets that answer instead.
"""
import numpy as np

# Simulation budget. Fitting is a least-squares solve over a few hundred rows,
# so this is milliseconds; the cost that matters is the SUT runs the proposal
# leads to, not the search for it.
TRIALS = 40
# Starts at 5, not 1. A relative-error fit gives an extrapolated point enormous
# leverage, so two measurements past the frontier really can flip a verdict a
# thousand rows hold -- the power calculation is right about that, and a
# verdict resting on two measurements is still not one to report.
POINT_LADDER = (5, 8, 12, 20, 32)

# Power a region must reach before it is worth requesting. Below this the
# request spends SUT time without changing the answer.
TARGET_POWER = 0.95

# Fallback relative noise when the corpus carries no usable CIs. The measurement
# stopping rule targets rel_margin=0.05, so this is what it delivers.
DEFAULT_EPS = 0.05


# A tie only poses a question when the property explains the metric at all.
# Every complexity class fits equally badly against a property the metric does
# not respond to, so all of them land inside the tie band. Those are not
# undecided models; they are absent relationships, and no amount of data
# anywhere makes a complexity class meaningful. A tie is taken as a real
# question only when the best class beats Constant by this factor.
RELEVANCE = 2.0

# Simulation cost grows with the number of candidates, and past three the tie is
# telling you the same thing the relevance test does.
MAX_CANDIDATES = 3


def worth_deciding(fitted, tied):
    """Is this tie a question data could answer?

    `fitted` is the full {class instance: residual} map, `tied` the near-ties.
    """
    from big_o import complexities

    if not 2 <= len(tied) <= MAX_CANDIDATES:
        return False
    best = min(fitted.values())
    const = [v for k, v in fitted.items()
             if isinstance(k, complexities.Constant)]
    if not const or best <= 0:
        return True                  # no Constant to compare against; allow it
    return (const[0] / best) >= RELEVANCE


def noise_floor(rows, metric, default=DEFAULT_EPS):
    """Relative CI half-width the harness actually achieves on this metric."""
    vals = []
    for r in rows:
        try:
            m = float(r[metric])
            lo, hi = float(r[f"{metric}_ci_lo"]), float(r[f"{metric}_ci_hi"])
        except (KeyError, TypeError, ValueError):
            continue
        if m > 0 and np.isfinite(lo) and np.isfinite(hi) and hi >= lo:
            vals.append((hi - lo) / 2 / m)
    return float(np.median(vals)) if vals else default


def region_residuals(xs, ys, candidate, lo, hi, eps):
    """Observed relative residuals of `candidate` in [lo, hi), or None.

    Simulating with the measurement noise alone assumes the candidate is exactly
    true everywhere, and the place that assumption fails hardest is the small-n
    end, where the system is doing constant work that no complexity class
    describes. The observed residual spread there can be several times the
    measurement noise, so simulating with the measurement noise overstates the
    region's power by a wide margin and the proposer picks it.

    Using the observed residuals instead folds model misspecification into the
    design criterion: a region the model family already fits badly needs far
    more points to decide anything, and drops down the ranking on its own. No
    cutoff and no minimum length has to be chosen.

    They are resampled rather than reduced to a standard deviation, because the
    misfit is systematic and not centred. Residuals in a badly fitted region
    sit to one side; drawing centred Gaussians of the same width would model a
    biased region as an unbiased noisy one and overstate what data there can
    settle.

    Beyond the corpus there is no residual to measure, and falling back to the
    measurement noise flatters exactly the regions where models diverge most:
    the proposal becomes an extrapolation that claims a handful of inputs
    would settle a tie held by the whole corpus. The outermost observed band
    is the better prior -- how far the model misses by at the edge of what has
    been seen is the closest evidence available for how far it will miss just
    outside. It still assumes the system keeps following one of the candidates
    out there, which is the hypothesis under test, so read a proposal past the
    frontier as "if it continues to follow one of these, this many points
    tells them apart".
    """
    m = (xs >= lo) & (xs < hi)
    if m.sum() < 3:
        top = np.quantile(xs, 0.75)
        m = xs >= top
        if m.sum() < 3:
            return None
    pred = np.asarray(candidate.compute(xs[m]), dtype=float)
    ok = np.isfinite(pred) & (ys[m] > 0)
    if ok.sum() < 3:
        return None
    resid = (ys[m][ok] - pred[ok]) / ys[m][ok]
    if float(np.std(resid)) < eps:
        return None          # fits to within measurement noise; use eps
    return resid


def power(xs, ys, tied, lo, hi, n_points, eps, trials=TRIALS, rng=None):
    """Fraction of simulated experiments in which the fit names the truth.

    0.5 is the uninformative floor for two candidates: the fit returns the same
    class whatever generated the new points.
    """
    from core import model_fit

    rng = rng or np.random.default_rng(0)
    classes = [type(t) for t in tied]
    hits = n = 0
    for truth in tied:
        # Noise for data generated by `truth` is how far the real system already
        # sits from `truth` here -- if the system is truth, that spread is what
        # a new measurement will show.
        resid = region_residuals(xs, ys, truth, lo, hi, eps)
        for _ in range(trials):
            nx = np.exp(rng.uniform(np.log(lo), np.log(hi), n_points))
            ny = np.asarray(truth.compute(nx), dtype=float)
            if resid is None:
                draw = rng.normal(0, eps, n_points)
            else:
                draw = rng.choice(resid, size=n_points, replace=True)
            ny = np.maximum(ny * (1 + draw), 1.0)
            try:
                best, _ = model_fit.infer_complexity(
                    np.r_[xs, nx], np.r_[ys, ny], classes=classes)
            except ValueError:
                continue
            hits += (type(best) is type(truth))
            n += 1
    return hits / n if n else 0.0


def _candidate_regions(xs, reach):
    """Half-decade bands over the observed range, then out to `reach`.

    Bands are equal-ratio rather than equal-width because that is the scale a
    complexity class lives on: a band from 700 to 1101 spans less than a
    doubling and cannot tell any two classes apart.
    """
    lo, hi = float(np.min(xs)), float(np.max(xs))
    lo = max(lo, 1.0)
    edges = list(np.geomspace(lo, max(hi, lo * 2), 7))
    if reach and reach > hi:
        edges += list(np.geomspace(hi, reach, 4))[1:]
    edges = sorted(set(round(e, 6) for e in edges))
    return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)
            if edges[i + 1] > edges[i] * 1.2]


def propose(xs, ys, tied, *, reach=None, eps=DEFAULT_EPS,
            target_power=TARGET_POWER, cost_model=None, rng=None):
    """The cheapest region and sample count that would settle the tie.

    `reach` is the largest property value the grammar and node budget can
    actually produce; regions beyond it are not proposed, because a request that
    cannot be satisfied costs a generation and returns nothing (which is what
    `prop_beyond`'s frontier ledger exists to remember).

    `cost_model` predicts the metric at a property value, and is used only to
    rank affordable regions against each other. The best-fitting class is the
    natural choice: it is already a model of what a run there will cost.

    Returns None when there is nothing to decide or nothing affordable decides
    it.
    """
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    if len(tied) < 2:
        return None                      # the data already picked a winner

    rng = rng or np.random.default_rng(0)
    best = None
    for lo, hi in _candidate_regions(xs, reach):
        for k in POINT_LADDER:
            p = power(xs, ys, tied, lo, hi, k, eps, rng=rng)
            if p < target_power:
                continue
            mid = float(np.sqrt(lo * hi))
            # big_o's compute() wants an array, not a scalar.
            cost = k * (float(np.asarray(cost_model(np.array([mid])),
                                         dtype=float).ravel()[0])
                        if cost_model else 1.0)
            if best is None or cost < best["cost"]:
                best = {"lo": lo, "hi": hi, "n_points": k, "power": p,
                        "cost": cost,
                        "candidates": [type(t).__name__ for t in tied]}
            break                        # smallest k that works for this region
    return best
