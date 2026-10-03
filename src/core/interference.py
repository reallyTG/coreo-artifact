"""Does the metric's response to one property depend on another?

Exploration is one-dimensional, one property at a time. This analysis checks
whether there is evidence of cross-property interference, and so which pairs
are candidates for a joint structural exploration.

It is deliberately an analysis and not more sampling. It reads the corpus that
exists -- no generation, no SUT executions -- so the exponential blowup of
sampling property combinations never happens here. What it produces is
evidence about whether the marginal exploration was sufficient, and which
pairs deserve a joint request.

## What it measures

For an ordered pair (A, B) and a metric: split the corpus into strata of B, and
compute the rank correlation between A and the metric INSIDE each stratum. If
that correlation is the same in every stratum, A's effect does not depend on B
and one-dimensional regions describe the subject honestly. If it swings -- 0.9
where B is small and 0.1 where B is large -- then a claim about A is really a
claim about A at some particular B, and only a joint region can state it.

## Why a permutation null

A rank correlation computed on a few dozen rows is noisy, so some spread across
strata appears whatever the truth is, and more strata means more spread by
chance alone. Comparing the observed spread against a fixed threshold would
therefore report interference most loudly on the subjects with the least data.

The null here re-partitions the SAME rows into groups of the same sizes at
random, and recomputes the spread. That holds the overall A-metric relationship
and the stratum sizes fixed, and asks only whether B's particular way of
splitting the data produces more variation than an arbitrary split would. That
is the question; shuffling the metric instead would test "no relationship
anywhere", which is not what is being asked.
"""
import math
import random

import scipy.stats as ss

# Strata a pair is split into, and the rows each needs before its correlation is
# worth computing. Four rather than six: every stratum has to carry enough rows
# to estimate a correlation, and the corpora here run to a few hundred inputs.
N_STRATA = 4
MIN_PER_STRATUM = 12
PERMUTATIONS = 300
# Below this the pair is reported but not called interference; a swing smaller
# than this is not worth a joint request even when it is statistically real.
MIN_SPREAD = 0.25
ALPHA = 0.05


def _f(row, key):
    try:
        v = float(row.get(key, ""))
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def _rho(xs, ys):
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    r = ss.spearmanr(xs, ys).statistic
    return None if (r is None or math.isnan(r)) else r


def _strata(rows, prop, n_strata):
    """Equal-count strata of `prop`. Equal COUNT, not equal width, so every
    stratum has the rows it needs to estimate a correlation -- which equal-width
    bins do not give on a property whose distribution is skewed."""
    vals = [(v, r) for r in rows if (v := _f(r, prop)) is not None]
    if len(vals) < n_strata * MIN_PER_STRATUM:
        return []
    vals.sort(key=lambda t: t[0])
    size = len(vals) // n_strata
    out = []
    for i in range(n_strata):
        chunk = vals[i * size: (i + 1) * size if i < n_strata - 1 else len(vals)]
        if len({v for v, _ in chunk}) < 2 and i < n_strata - 1:
            return []           # a stratum with no variation in B is not a stratum
        out.append([r for _, r in chunk])
    return out


def _spread(groups, prop, metric):
    """Range of the within-group correlation, or None if any group is unusable."""
    rhos = []
    for g in groups:
        xs, ys = [], []
        for r in g:
            a, m = _f(r, prop), _f(r, metric)
            if a is not None and m is not None and m > 0:
                xs.append(a); ys.append(m)
        rho = _rho(xs, ys)
        if rho is None:
            return None, []
        rhos.append(rho)
    return max(rhos) - min(rhos), rhos


def pair(rows, a, b, metric, n_strata=N_STRATA, permutations=PERMUTATIONS,
         seed=0):
    """Evidence that A's effect on `metric` depends on B. None if untestable."""
    groups = _strata(rows, b, n_strata)
    if not groups:
        return None
    observed, rhos = _spread(groups, a, metric)
    if observed is None:
        return None

    sizes = [len(g) for g in groups]
    flat = [r for g in groups for r in g]
    rng = random.Random(seed)
    hits = 0
    for _ in range(permutations):
        rng.shuffle(flat)
        cut, parts = 0, []
        for s in sizes:
            parts.append(flat[cut:cut + s])
            cut += s
        null, _ = _spread(parts, a, metric)
        if null is not None and null >= observed:
            hits += 1
    p = (hits + 1) / (permutations + 1)
    return {"a": a, "b": b, "metric": metric, "spread": observed,
            "rhos": rhos, "p": p, "n": len(flat),
            "interferes": observed >= MIN_SPREAD and p <= ALPHA}


def report(rows, metrics, properties, n_strata=N_STRATA):
    """Lines naming the pairs whose effects are not separable."""
    from core.corpus import accepted

    usable = [r for r in rows if accepted(r)]
    if len(usable) < n_strata * MIN_PER_STRATUM:
        return []
    found, tested = [], 0
    for metric in metrics:
        for a in properties:
            for b in properties:
                if a == b:
                    continue
                v = pair(usable, a, b, metric, n_strata)
                if v is None:
                    continue
                tested += 1
                if v["interferes"]:
                    found.append(v)
    if not tested:
        return []
    lines = [f"[interference] {tested} property pair(s) tested over "
             f"{len(usable)} rows; {len(found)} show a dependence"]
    for v in sorted(found, key=lambda x: -x["spread"])[:6]:
        detail = ", ".join(f"{r:+.2f}" for r in v["rhos"])
        lines.append(
            f"  {v['a']} vs {v['metric']} changes with {v['b']}: "
            f"rho by {v['b']} stratum = [{detail}], spread {v['spread']:.2f}, "
            f"p={v['p']:.3f}")
    if found:
        lines.append("  -> a one-dimensional region on these properties states "
                     "less than it appears to; they are candidates for a joint "
                     "request.")
    return lines
