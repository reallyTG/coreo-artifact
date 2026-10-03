"""Complexity-class inference with scale-free residuals.

big_o.infer_big_o_class fits every candidate class by unweighted least squares
and picks the smallest sum of squared errors. Over a metric that spans decades
the largest points are the only ones the criterion can see, and a class wins by
bending up at the top whether or not it describes the rest of the data. A
quadratic system can read as Cubic that way.

So both halves differ here. A class is fitted by minimising relative error
rather than absolute, and classes are compared on relative error too. A point
at the small end of the property and a point at the large end then count the
same, which is what "which curve describes this system" means.

Classes that already fit in log-time space (Polynomial, Exponential) are left
unweighted, because that space is scale-free to begin with; they are still
scored on the same relative criterion as everything else, so the comparison
across all classes is like for like.
"""
import numpy as np

try:                                    # the classes and their formatting are
    from big_o import complexities      # big_o's; only the fitting is not
    ALL_CLASSES = complexities.ALL_CLASSES
except ImportError:                     # pragma: no cover
    complexities = None
    ALL_CLASSES = []

# Classes that answer "which complexity class is this". Polynomial is excluded:
# it fits a free exponent, so it is strictly more flexible than every
# fixed-shape class and wins almost whatever the data does. An answer such as
# n^1.2 is true and useless when the question is whether the system is
# linearithmic. Its exponent is still worth having, so `fitted_exponent`
# reports it beside the chosen class.
RANKED_CLASSES = [c for c in ALL_CLASSES
                  if getattr(c, "__name__", "") != "Polynomial"]

# Preference for the simpler class when two are within this fraction of each
# other. Quadratic and Cubic do not nest in this parameterisation, but a cubic
# with a small leading coefficient tracks a quadratic closely over a bounded
# range, so the higher-order class wins those near-ties on rounding. Relative,
# because the residuals are relative.
#
# A class chosen inside this band is chosen by the bias rather than by the
# data, which `near_ties` is there to make visible.
SIMPLICITY_BIAS = 0.10


def _fit_one(inst, ns, times):
    """Fit one complexity class. Returns its relative SSR, or inf.

    The fit runs in the class's own transform space, weighted so that each
    point contributes its relative error. The score is always computed on the
    original scale, so classes fitted in different spaces stay comparable.
    """
    x = inst._transform_n(ns)
    y = inst._transform_time(times)
    log_time = not np.allclose(y, times)

    if log_time:
        # already scale-free; weighting it again would over-weight whichever
        # points happen to sit near log(t) = 0
        w = np.ones_like(times)
    else:
        w = 1.0 / times

    try:
        coeff, *_ = np.linalg.lstsq(x * w[:, None], y * w, rcond=None)
    except np.linalg.LinAlgError:
        return np.inf
    inst.coeff = coeff

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        pred = np.asarray(inst.compute(ns), dtype=float)
        rel = (pred - times) / times
        ssr = float(np.sum(rel ** 2))
    if not np.isfinite(ssr):
        return np.inf
    return ssr


def infer_complexity(ns, times, classes=None):
    """Best-fitting complexity class, and every class's relative SSR.

    Signature-compatible with big_o.infer_big_o_class: returns
    (best_instance, {instance: residual}), so callers keep using
    `best.compute(...)` and big_o's report formatting.
    """
    ns = np.asanyarray(ns, dtype=float)
    times = np.asanyarray(times, dtype=float)
    if classes is None:
        classes = RANKED_CLASSES

    keep = np.isfinite(ns) & np.isfinite(times) & (times > 0)
    ns, times = ns[keep], times[keep]
    if len(ns) < 3:
        raise ValueError(f"need at least 3 usable points, have {len(ns)}")

    fitted = {}
    for class_ in classes:
        inst = class_()
        fitted[inst] = _fit_one(inst, ns, times)

    # Simplest class within SIMPLICITY_BIAS of the best. big_o gives each class
    # an `order`, so "simplest" is well defined without hard-coding a ranking.
    best_ssr = min(fitted.values())
    if not np.isfinite(best_ssr):
        raise ValueError("no complexity class could be fitted")
    near = [i for i, r in fitted.items() if r <= best_ssr * (1.0 + SIMPLICITY_BIAS)]
    best = min(near, key=lambda i: getattr(i, "order", 0))
    return best, fitted


def near_ties(fitted, bias=SIMPLICITY_BIAS):
    """Classes the data does not separate, best first.

    A selection with more than one entry here was decided by the tie-break
    rather than by evidence, which is the case worth spending a targeted
    request on: ask for inputs in the property range where these candidates
    disagree most, and the next fit is decided by data.
    """
    ranked = sorted(fitted.items(), key=lambda kv: kv[1])
    best = ranked[0][1]
    if not np.isfinite(best) or best <= 0:
        return [inst for inst, _ in ranked[:1]]
    return [inst for inst, r in ranked if r <= best * (1.0 + bias)]


def fitted_exponent(ns, times):
    """The free exponent b in t = a * n ** b, or None.

    A diagnostic rather than a class: 1.2 says linearithmic territory, 1.9 says
    quadratic. Reported beside the chosen class because it does not depend on
    the candidate set.
    """
    if complexities is None:
        return None
    ns = np.asanyarray(ns, dtype=float)
    times = np.asanyarray(times, dtype=float)
    keep = np.isfinite(ns) & np.isfinite(times) & (ns > 0) & (times > 0)
    ns, times = ns[keep], times[keep]
    if len(ns) < 3:
        return None
    try:
        inst = complexities.Polynomial()
        _fit_one(inst, ns, times)
        return float(inst.coeff[1])
    except Exception:
        return None


def relative_weights(y):
    """statsmodels WLS weights that minimise relative error.

    WLS minimises sum(w * (y - yhat) ** 2), so w = 1 / y ** 2 makes each term
    ((y - yhat) / y) ** 2. Non-positive or non-finite entries get zero weight
    rather than an infinite one.
    """
    y = np.asarray(y, dtype=float)
    w = np.zeros_like(y)
    ok = np.isfinite(y) & (y > 0)
    w[ok] = 1.0 / (y[ok] ** 2)
    return w
