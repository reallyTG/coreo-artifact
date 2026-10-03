"""Which system is better, where, and with what confidence.

This module provides two things: regions where one system beats another,
decided statistically rather than by eye, and a verdict that says where it holds
rather than only overall. The shape to produce is one system ahead at one end of
a property and behind at the other, and producing it needs the crossover, not a
single number.

Three choices, in order of how much they matter.

**Paired.** Every input in the corpus is measured on every system, because that
is how `_measure_inputs` works. So the comparison is over per-input DIFFERENCES,
not over two independent samples. Input-to-input variation in a corpus spans
decades while the difference between two systems on one input is what is being
asked about; pooling them unpaired buries the effect under the spread. Pairing
is also what makes a few dozen inputs enough to decide a region.

**Ratios, not differences.** Runtime runs over several orders of magnitude. An
absolute difference is dominated by the largest inputs and says nothing about
the rest, the same reason `core.model_fit` fits on relative error. The statistic
is the median per-input ratio, reported as "1.8x".

**A practical floor, not just a p-value.** With hundreds of paired inputs a 1%
difference is significant and meaningless, and it is smaller than the per-input
measurement precision. So a ratio inside `EQUIVALENCE` is reported as "no
practical difference" rather than as a win. A region is only called for a system
when the confidence interval clears that band, which also means "these two are
equivalent here" can be stated positively instead of as a failure to reject.

A region the interval spans is UNDECIDED, and that is a request for more inputs
rather than a conclusion.
"""
import math
import statistics
from collections import defaultdict

# Ratios inside this band count as no practical difference. Set above the
# per-input measurement precision, so a "win" is never just the harness's own
# noise.
EQUIVALENCE = 1.10
# Bootstrap resamples for the interval on the median ratio.
RESAMPLES = 2000
CONFIDENCE = 0.95
# Paired inputs a region needs before it is worth testing at all.
MIN_PAIRS = 8


def _f(row, key):
    try:
        v = float(row.get(key, ""))
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def paired(rows, metric):
    """{input_hash: {system: value}} over rows with a usable measurement."""
    from core.corpus import accepted

    out = defaultdict(dict)
    for r in rows:
        if not accepted(r):
            continue
        v = _f(r, metric)
        if v is not None and v > 0:
            out[r["input_hash"]][r["function_name"]] = v
    return out


def _bootstrap_median(values, resamples=RESAMPLES, confidence=CONFIDENCE, seed=0):
    import random

    rng = random.Random(seed)
    n = len(values)
    meds = sorted(statistics.median(rng.choices(values, k=n))
                  for _ in range(resamples))
    lo = meds[int((1 - confidence) / 2 * resamples)]
    hi = meds[min(resamples - 1, int((1 + confidence) / 2 * resamples))]
    return lo, hi


def compare_pair(by_input, a, b, metric, equivalence=EQUIVALENCE):
    """Compare systems `a` and `b` over the inputs both were measured on.

    Returns a verdict dict, or None when too few inputs are shared. The ratio is
    b/a, so a ratio above 1 means `a` is the cheaper system.
    """
    import scipy.stats as ss

    ratios = []
    for vals in by_input.values():
        if a in vals and b in vals:
            ratios.append(vals[b] / vals[a])
    if len(ratios) < MIN_PAIRS:
        return None

    logs = [math.log(r) for r in ratios]
    med = statistics.median(ratios)
    lo, hi = _bootstrap_median(ratios)
    try:
        p = float(ss.wilcoxon(logs).pvalue)
    except ValueError:            # all differences zero
        p = 1.0

    if lo > equivalence:
        verdict, winner = "a_faster", a
    elif hi < 1 / equivalence:
        verdict, winner = "b_faster", b
    elif 1 / equivalence <= lo and hi <= equivalence:
        # The interval sits inside the band: equivalent, stated positively.
        verdict, winner = "equivalent", None
    else:
        verdict, winner = "undecided", None
    return {"a": a, "b": b, "metric": metric, "n": len(ratios),
            "ratio": med, "ci": (lo, hi), "p": p,
            "verdict": verdict, "winner": winner}


# Positive values spanning at least this ratio get equal-ratio bins; narrower
# ones get equal-width bins. Count properties that run over orders of magnitude
# clear it; bounded ones do not (jsonpath_js `count_slice` 1..6 is 6x).
GEOMETRIC_SPAN = 10.0


def property_bins(values, n_bins):
    """Region bounds over a property axis, as (lo, hi) pairs in ascending order.

    Every finite value lands in exactly one region under `in_region`. That is
    the invariant. Equal-ratio edges built from positive values only would
    leave every input at 0 outside every region. Most properties are grammar
    counts, and 0 is the commonest count there is (jsonpath_js `count_slice`
    is 0 on 306 of 568 inputs), so per-region verdicts that dropped it would
    be about a minority of the corpus.

    * **Zero** is its own degenerate region (0, 0), placed before the positive
      bins. "No slices at all" is a shape of input, not the bottom end of
      "few slices", and no log-scale bin can hold it anyway.
    * **Negatives**, which no shipped property produces, share one region
      below zero rather than being dropped.
    * **Positives** get equal-ratio bins when they span `GEOMETRIC_SPAN` or
      more. Count properties run over orders of magnitude with most inputs at
      small values, and equal-width bins would put nearly every input in the
      bottom bin and decide nothing about the rest. A narrower span gets
      equal-width bins, since equal-ratio edges on a bounded property make
      the bottom bin several times narrower than the top one for no reason
      in the property. A span under 2x is not split.

    Bins are half-open [lo, hi) except the last, which includes the observed
    maximum: a half-open last bin drops the largest input in the corpus, and
    that is exactly the one a cost comparison cares most about.
    """
    vals = [v for v in values if v is not None and math.isfinite(v)]
    neg = [v for v in vals if v < 0]
    pos = sorted(v for v in vals if v > 0)
    has_zero = any(v == 0 for v in vals)

    out = []
    if neg:
        # Up to 0 exclusive when anything sits at or above it; otherwise the
        # region is last and closed, so its own maximum stays in.
        out.append((min(neg), 0.0 if (has_zero or pos) else max(neg)))
    if has_zero:
        out.append((0.0, 0.0))
    if not pos:
        return out
    lo, hi = pos[0], pos[-1]
    if lo == hi:                  # one distinct positive value
        return out + [(lo, hi)]
    if hi / lo < 2:               # too narrow to split meaningfully
        return out + [(lo, hi)]
    import numpy as np
    if hi / lo >= GEOMETRIC_SPAN:
        edges = list(np.geomspace(lo, hi, n_bins + 1))
    else:
        edges = list(np.linspace(lo, hi, n_bins + 1))
    # Pin the ends to the observed values, so float error in the spacing can
    # neither exclude the minimum nor leave the maximum above the top edge.
    edges[0], edges[-1] = lo, hi
    return out + [(float(edges[i]), float(edges[i + 1]))
                  for i in range(len(edges) - 1)]


def in_region(v, lo, hi, last):
    """Whether `v` belongs to the region [lo, hi) -- closed when it is the
    `last` region, and exactly `lo` when the region is degenerate (the zero
    region, or a property with one distinct positive value)."""
    if v is None:
        return False
    if lo == hi:
        return v == lo
    return lo <= v < hi or (last and v == hi)


def region_label(lo, hi, last=False):
    """How a region prints: `=0` for a degenerate one, else [lo,hi) or [lo,hi]."""
    if lo == hi:
        return f"={lo:.4g}"
    return f"[{lo:.4g},{hi:.4g}{']' if last else ')'}"


def by_region(rows, a, b, metric, prop, n_bins=6, equivalence=EQUIVALENCE):
    """Verdicts per bin of `prop`, each with the bin's bounds attached.

    This is the shape the comparison reports: not "which system is better" but
    "better where", so that a crossover can be seen and reported.

    Regions come from `property_bins`, so every input with a finite `prop` is
    in exactly one of them, including the zero region. Each region carries
    `closed`, true on the last, which is what `in_region` needs to test
    membership the same way elsewhere (`_bin_ratios`, `confounds`).
    """
    prop_of = {}
    for r in rows:
        v = _f(r, prop)
        if v is not None:
            prop_of[r["input_hash"]] = v
    if not prop_of:
        return []
    bins = property_bins(prop_of.values(), n_bins)
    all_paired = paired(rows, metric)

    out = []
    for i, (blo, bhi) in enumerate(bins):
        top = i == len(bins) - 1
        sub = {h: v for h, v in all_paired.items()
               if in_region(prop_of.get(h), blo, bhi, top)}
        v = compare_pair(sub, a, b, metric, equivalence)
        if v is None:
            out.append({"lo": blo, "hi": bhi, "closed": top, "n": len(sub),
                        "verdict": "insufficient", "winner": None,
                        "a": a, "b": b, "metric": metric, "prop": prop})
            continue
        v.update(lo=blo, hi=bhi, closed=top, prop=prop)
        out.append(v)
    return out


def weighted_ratio(rows, a, b, metric, prop, n_bins=6,
                   equivalence=EQUIVALENCE, weights=None):
    """Paired ratio with each REGION counted once, not each input.

    The pooled verdict weights bins by how many inputs the loop happened to put
    in them, and the loop is actively reshaping that. Bin sizes are uneven, so
    one bin can carry a large share of the verdict for no reason anyone chose,
    and the pooled ratio can favour one system while the bins counted equally
    favour the other. The sign then depends on the sampling, not on the
    systems.

    On a wide-span property, equal weight per equal-ratio bin IS a log-uniform
    measure over the positive values: each decade counts the same. On a narrow
    one `property_bins` spaces the bins evenly, so the measure is uniform over
    the property instead. Either way the zero region, when present, is one more
    bin with the same weight as any other -- inputs with none of a construct
    count as one region, not as the share of the corpus they happen to be. It
    needs nothing from the caller, and unlike integrating a fitted model it
    cannot be poisoned by a bad fit -- a bin with no data becomes a reported
    gap rather than an extrapolated number.

    The statistic is the GEOMETRIC MEAN of the per-bin median ratios -- the
    natural average on a ratio scale, reading as: the typical cost ratio when
    every decade of `prop` matters equally. That is a stated choice with a
    consequence worth knowing: a decade where one system is 20x better outweighs
    three decades where the other is 2x better, because it averages log-ratios
    rather than counting bins, so it can name a different winner than the
    median of the same bins. The geometric mean is the defensible default for
    costs, and it is stable and stated -- unlike corpus weighting, which is
    neither -- but it is not neutral, and the per-region table remains the
    claim that assumes nothing.

    `weights` overrides the equal weighting, for a caller who knows the real
    workload; the measure used is always named in the result.
    """
    regions = by_region(rows, a, b, metric, prop, n_bins, equivalence)
    usable = [r for r in regions if r.get("ratio")]
    gaps = [r for r in regions if not r.get("ratio")]
    if len(usable) < 2:
        return None
    w = ([weights[i] for i, r in enumerate(regions) if r.get("ratio")]
         if weights else [1.0] * len(usable))
    total = sum(w) or 1.0

    def combine(per_bin):
        return math.exp(sum(wi * math.log(v) for wi, v in zip(w, per_bin)) / total)

    point = combine([r["ratio"] for r in usable])

    # Bootstrap inside each bin, weights held fixed, so the interval reflects
    # sampling error and not the choice of measure.
    import random
    rng = random.Random(0)
    per_bin_ratios = [_bin_ratios(rows, a, b, metric, prop, r) for r in usable]
    draws = []
    for _ in range(RESAMPLES // 4):
        meds = [statistics.median(rng.choices(rs, k=len(rs)))
                for rs in per_bin_ratios]
        draws.append(combine(meds))
    draws.sort()
    lo = draws[int((1 - CONFIDENCE) / 2 * len(draws))]
    hi = draws[min(len(draws) - 1, int((1 + CONFIDENCE) / 2 * len(draws)))]

    if lo > equivalence:
        verdict, winner = "a_faster", a
    elif hi < 1 / equivalence:
        verdict, winner = "b_faster", b
    elif 1 / equivalence <= lo and hi <= equivalence:
        verdict, winner = "equivalent", None
    else:
        verdict, winner = "undecided", None
    return {"a": a, "b": b, "metric": metric, "prop": prop,
            "ratio": point, "ci": (lo, hi), "p": float("nan"),
            "verdict": verdict, "winner": winner,
            "n": sum(r["n"] for r in usable), "bins": len(usable),
            "gaps": [(r["lo"], r["hi"], r["closed"]) for r in gaps],
            "measure": "user weights" if weights else "equal weight per bin"}


def _bin_ratios(rows, a, b, metric, prop, region):
    """The per-input ratios inside one region."""
    prop_of = {}
    for r in rows:
        v = _f(r, prop)
        if v is not None:
            prop_of[r["input_hash"]] = v
    out = []
    for h, vals in paired(rows, metric).items():
        v = prop_of.get(h)
        if v is None or a not in vals or b not in vals:
            continue
        if in_region(v, region["lo"], region["hi"], region.get("closed", True)):
            out.append(vals[b] / vals[a])
    return out or [1.0]


def crossovers(regions):
    """Adjacent decided regions whose winner differs.

    A crossover is the finding a developer acts on ("use one system below
    here, the other above"), and it is invisible in any single overall verdict.
    """
    decided = [r for r in regions if r.get("winner")]
    out = []
    for x, y in zip(decided, decided[1:]):
        if x["winner"] != y["winner"]:
            out.append((x, y))
    return out


def undecided(regions):
    """Regions that need more inputs before they decide anything."""
    return [r for r in regions
            if r.get("verdict") in ("undecided", "insufficient")]


# A region's other properties may swing this much across the bins before the
# verdict is called confounded. 3x is well past what a genuinely independent
# axis shows.
CONFOUND_RATIO = 3.0


def confounds(rows, regions, properties, threshold=CONFOUND_RATIO):
    """Properties that vary systematically ACROSS the bins of this region set.

    A one-dimensional region is only a claim about its own property if the other
    properties are not moving with it. When the bins of one property also
    differ widely in the median of another, a verdict that holds in the low
    bins may be a verdict about the second property, and reporting it as a
    finding about the first would be wrong.

    Checked as a swing in medians across bins rather than as a correlation,
    because the relationship need not be monotonic: medians can swing widely
    across bins while the rank correlation stays near zero, which no
    correlation filter would flag.
    """
    prop_of = {p: {} for p in properties}
    for r in rows:
        for p in properties:
            v = _f(r, p)
            if v is not None:
                prop_of[p][r["input_hash"]] = v
    binned = [r for r in regions if r.get("n", 0) >= MIN_PAIRS]
    if len(binned) < 2:
        return []
    own = binned[0].get("prop")
    out = []
    for p in properties:
        if p == own:
            continue
        meds = []
        for reg in binned:
            vals = [v for h, v in prop_of[p].items()
                    if in_region(prop_of.get(own, {}).get(h), reg["lo"],
                                 reg["hi"], reg.get("closed", True))]
            if len(vals) >= MIN_PAIRS:
                meds.append(statistics.median(vals))
        pos = [m for m in meds if m > 0]
        if len(pos) >= 2 and max(pos) / min(pos) >= threshold:
            out.append(f"{p} ({min(pos):.4g}..{max(pos):.4g} across bins)")
    return out


# Metrics where a LARGER value is better. Everything the framework emits is a
# cost (runtime, resident memory, page faults, leak magnitude), so this is empty
# by default; a subject reporting e.g. a throughput has to say so.
HIGHER_IS_BETTER = frozenset()


def dominance(rows, a, b, metrics, equivalence=EQUIVALENCE,
              higher_is_better=HIGHER_IS_BETTER):
    """Pareto verdict for `a` against `b` across every metric at once.

    Metrics are compared one at a time everywhere else, which leaves the reader
    to combine them. For a version pair that can mean one line per metric,
    equivalent on most and better on one, where the finding is one sentence:
    the newer version costs nothing and fixes the regression. That is a
    dominance, and it is the statement a developer acts on.

    The cases worth separating:

    * DOMINATES -- better on at least one metric, not worse on any. The other
      system can be dropped from consideration.
    * TRADE-OFF -- each side wins something. No single answer exists, and saying
      "A is better" would be false. Concluded even when other metrics are still
      undecided, since nothing they could say would resolve it.
    * AHEAD, INCOMPLETE -- winning some, with others undecided. NOT a dominance
      claim: an undecided metric could still go the other way and make it a
      trade-off. Those metrics are exactly where more inputs are worth buying.
    * EQUIVALENT -- inside the equivalence band on every metric.
    """
    per, wins_a, wins_b, undec, equiv = {}, [], [], [], []
    for m in metrics:
        v = compare_pair(paired(rows, m), a, b, m, equivalence)
        if v is None:
            continue
        per[m] = v
        winner = v["winner"]
        if winner is not None and m in higher_is_better:
            winner = b if winner == a else a
        if winner == a:
            wins_a.append(m)
        elif winner == b:
            wins_b.append(m)
        elif v["verdict"] == "equivalent":
            equiv.append(m)
        else:
            undec.append(m)

    if not per:
        verdict, winner = "insufficient", None
    elif wins_a and wins_b:
        verdict, winner = "tradeoff", None
    elif wins_a and not undec:
        verdict, winner = "dominates", a
    elif wins_b and not undec:
        verdict, winner = "dominates", b
    elif wins_a or wins_b:
        verdict, winner = "ahead_incomplete", (a if wins_a else b)
    elif equiv and not undec:
        verdict, winner = "equivalent", None
    else:
        verdict, winner = "undecided", None
    return {"a": a, "b": b, "verdict": verdict, "winner": winner,
            "wins_a": wins_a, "wins_b": wins_b, "undecided": undec,
            "equivalent": equiv, "per_metric": per}


def describe_dominance(d):
    a, b, w = d["a"], d["b"], d["winner"]
    def mags(metrics):
        out = []
        for m in metrics:
            v = d["per_metric"][m]
            r = v["ratio"] if v["ratio"] > 1 else 1 / v["ratio"]
            out.append(f"{m} {r:.2f}x")
        return ", ".join(out)

    if d["verdict"] == "dominates":
        loser = b if w == a else a
        return (f"{w} DOMINATES {loser}: better on "
                f"{mags(d['wins_a'] or d['wins_b'])}; equivalent on "
                f"{', '.join(d['equivalent']) or 'nothing else'}")
    if d["verdict"] == "tradeoff":
        return (f"{a} vs {b} TRADE-OFF: {a} better on {mags(d['wins_a'])}; "
                f"{b} better on {mags(d['wins_b'])}")
    if d["verdict"] == "ahead_incomplete":
        return (f"{w} ahead on {mags(d['wins_a'] or d['wins_b'])} but "
                f"{', '.join(d['undecided'])} undecided -- not a dominance "
                f"claim until those are settled")
    if d["verdict"] == "equivalent":
        return f"{a} and {b} EQUIVALENT on every metric"
    return f"{a} vs {b} undecided on every metric"


def frontier(rows, metrics, equivalence=EQUIVALENCE,
             higher_is_better=HIGHER_IS_BETTER):
    """(non-dominated systems, {dominated: dominator}).

    A dominated system can be dropped from consideration entirely, which is a
    stronger and more useful statement than any ranking: it says the choice is
    only ever between what remains.
    """
    names = systems(rows)
    dominated = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            d = dominance(rows, a, b, metrics, equivalence, higher_is_better)
            if d["verdict"] == "dominates":
                loser = b if d["winner"] == a else a
                dominated[loser] = d["winner"]
    return [n for n in names if n not in dominated], dominated


def regional_dominance(rows, metrics, prop, n_bins=6, equivalence=EQUIVALENCE,
                       higher_is_better=HIGHER_IS_BETTER):
    """The Pareto frontier per bin of `prop`, and any global claim it refutes.

    A global frontier is weighted by whatever the corpus contains, and dominance
    phrasing makes that weighting sound like a much stronger claim than a ratio
    does. The global frontier can say one system dominates another ("drop it
    from consideration") while the dominated system wins by a wide margin in
    one region. Both come from the same rows, and the loop is what decided
    which regions hold most of them.

    So the frontier is computed per region, and any system the global verdict
    would have discarded while it wins somewhere is reported as a contradiction
    rather than quietly resolved. That contradiction is the finding: it means
    the choice depends on the input, which is the whole premise of comparative
    profiling.
    """
    prop_of = {}
    for r in rows:
        v = _f(r, prop)
        if v is not None:
            prop_of[r["input_hash"]] = v
    if not prop_of:
        return [], []
    bins = property_bins(prop_of.values(), n_bins)
    by_bin = []
    for i, (blo, bhi) in enumerate(bins):
        top = i == len(bins) - 1
        sub = [r for r in rows
               if in_region(prop_of.get(r["input_hash"]), blo, bhi, top)]
        if len({r["input_hash"] for r in sub}) < MIN_PAIRS:
            continue
        nd, dom = frontier(sub, metrics, equivalence, higher_is_better)
        by_bin.append({"lo": blo, "hi": bhi, "closed": top, "non_dominated": nd,
                       "dominated": dom,
                       "n": len({r["input_hash"] for r in sub})})

    _, global_dom = frontier(rows, metrics, equivalence, higher_is_better)
    contradictions = []
    for loser, winner in global_dom.items():
        wins_in = [b for b in by_bin if loser in b["non_dominated"]]
        if wins_in:
            where = ", ".join(region_label(b["lo"], b["hi"], b["closed"])
                              for b in wins_in)
            contradictions.append(
                f"{loser} is dominated by {winner} over the whole corpus but "
                f"survives in {where} on {prop} -- the global verdict is a "
                f"statement about this corpus's mix, not about the systems")
    return by_bin, contradictions


def rejection_report(corpus, properties=None, max_lines=8):
    """Inputs a system refused, and where in the property space they sit.

    A rejection is filtered out of the models and the targeting, for the good
    reason that an input taking the error path does different work and belongs
    to a different population. Filtered is not the same as unreported, though:
    a system that refuses inputs its peers accept is a finding, so it is
    reported.

    The property box the rejected inputs occupy is what makes the line
    actionable: a range on a property names the shape that breaks the system,
    where a bare count does not.
    """
    from core.corpus import accepted

    rows = list(corpus.rows.values())
    if not rows:
        return []
    rejected = [r for r in rows if not accepted(r)]
    if not rejected:
        return []

    by_system = defaultdict(list)
    for r in rejected:
        by_system[r.get("function_name", "?")].append(r)
    total_by_system = defaultdict(int)
    for r in rows:
        total_by_system[r.get("function_name", "?")] += 1

    lines = [f"[reject] {len({r['input_hash'] for r in rejected})} input(s) "
             f"refused by at least one system (kept in the corpus, held out of "
             f"the models):"]
    for system, rs in sorted(by_system.items(), key=lambda kv: -len(kv[1])):
        share = len(rs) / max(1, total_by_system[system])
        where = []
        for p in (properties or []):
            vals = [v for v in (_f(r, p) for r in rs) if v is not None]
            allv = [v for v in (_f(r, p) for r in rows) if v is not None]
            if not vals or not allv or max(allv) == min(allv):
                continue
            # Only worth naming when the rejected inputs sit somewhere
            # particular rather than spread over the whole axis.
            span = (max(vals) - min(vals)) / (max(allv) - min(allv))
            if span <= 0.5:
                where.append(f"{p} in [{min(vals):g},{max(vals):g}]")
        lines.append(f"  {system}: {len(rs)} of {total_by_system[system]} "
                     f"({share:.0%})"
                     + (f" -- all at {'; '.join(where[:3])}" if where else ""))
        if len(lines) > max_lines:
            break
    return lines


def systems(rows):
    return sorted({r["function_name"] for r in rows})


def report(rows, metrics, properties, equivalence=EQUIVALENCE, n_bins=6):
    """Lines describing, per metric: the overall verdict for each system pair,
    and where along each property the winner changes."""
    lines = []
    names = systems(rows)
    for metric in metrics:
        all_paired = paired(rows, metric)
        if not all_paired:
            continue
        lines.append(f"[compare] {metric}: {len(all_paired)} inputs, "
                     f"{len(names)} systems (paired; ratios, {equivalence:.2f}x "
                     f"equivalence band)")
        lines.append("[compare] overall verdicts are weighted by what the "
                     "corpus contains, which the loop itself shapes; the "
                     "per-region lines are the portable claim.")
        # Once, not per pair: whether a property's bins are confounded is a
        # fact about the corpus and the binning, not about which two systems
        # are being compared. Reported per pair it would repeat the same
        # NOTE lines for every pair and bury the verdicts.
        confounded = {}
        for prop in properties:
            probe = by_region(rows, names[0], names[-1], metric, prop,
                              n_bins, equivalence)
            c = confounds(rows, probe, properties)
            if c:
                confounded[prop] = c
        for prop, c in confounded.items():
            lines.append(f"[compare] {prop} bins move with " + "; ".join(c)
                         + " -- those regions are joint, not "
                           f"{prop} findings")
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                v = compare_pair(all_paired, a, b, metric, equivalence)
                if v is None:
                    continue
                lines.append("  " + describe(v))
                # A verdict that moves when the bins are counted equally was a
                # statement about the corpus's shape. Reported only when they
                # disagree, because that disagreement is the finding.
                for prop in properties:
                    w = weighted_ratio(rows, a, b, metric, prop, n_bins,
                                       equivalence)
                    if w is None or w["verdict"] == v["verdict"]:
                        continue
                    lines.append(
                        f"      DEPENDS ON SAMPLING: counting each {prop} bin "
                        f"once gives {w['ratio']:.2f}x (95% CI {w['ci'][0]:.2f}-"
                        f"{w['ci'][1]:.2f}, {w['bins']} bins, {w['measure']}), "
                        f"verdict '{w['verdict']}' not '{v['verdict']}'")
                    if w["gaps"]:
                        lines.append(
                            f"      ... and {len(w['gaps'])} {prop} bin(s) have "
                            f"too little data to enter that: "
                            + ", ".join(region_label(*g) for g in w["gaps"]))
                for prop in properties:
                    regs = by_region(rows, a, b, metric, prop, n_bins, equivalence)
                    tag = " (confounded)" if prop in confounded else ""
                    for x, y in crossovers(regs):
                        lines.append(
                            f"      crossover on {prop}{tag}: {x['winner']} better "
                            f"{_below(x)}, {y['winner']} better {_above(y)}")
                    nd = [r for r in regs if r.get("verdict") == "undecided"]
                    if nd:
                        lines.append(
                            f"      undecided on {prop}{tag} in "
                            + ", ".join(region_label(r["lo"], r["hi"], r["closed"])
                                        for r in nd)
                            + " -- needs more inputs")
    # Dominance across all metrics at once, per region. Reported last because it
    # is the summary the other lines support.
    if len(metrics) > 1:
        lines.append(f"[compare] dominance across {', '.join(metrics)}:")
        names = systems(rows)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                d = dominance(rows, a, b, metrics, equivalence)
                if d["verdict"] != "insufficient":
                    lines.append("  " + describe_dominance(d))
        for prop in properties:
            by_bin, contra = regional_dominance(rows, metrics, prop, n_bins,
                                                equivalence)
            for b in by_bin:
                lines.append(f"      {prop} "
                             f"{region_label(b['lo'], b['hi'], b['closed'])} "
                             f"(n={b['n']}): "
                             f"{', '.join(b['non_dominated'])} not dominated")
            for c in contra:
                lines.append(f"      WARNING {c}")
    return lines


def _below(region):
    """'below 31.6' for a crossover's lower side; 'at 0' for the zero region,
    where 'below 0' would name inputs that do not exist."""
    if region["lo"] == region["hi"]:
        return f"at {region['lo']:.4g}"
    return f"below {region['hi']:.4g}"


def _above(region):
    if region["lo"] == region["hi"]:
        return f"at {region['lo']:.4g}"
    return f"above {region['lo']:.4g}"


def describe(v):
    """One line for a verdict."""
    lo, hi = v["ci"]
    if v["verdict"] == "a_faster":
        return (f"{v['a']} better than {v['b']} on {v['metric']}: {v['ratio']:.2f}x "
                f"(95% CI {lo:.2f}-{hi:.2f}, n={v['n']}, p={v['p']:.3g})")
    if v["verdict"] == "b_faster":
        return (f"{v['b']} better than {v['a']} on {v['metric']}: {1/v['ratio']:.2f}x "
                f"(95% CI {1/hi:.2f}-{1/lo:.2f}, n={v['n']}, p={v['p']:.3g})")
    if v["verdict"] == "equivalent":
        return (f"{v['a']} and {v['b']} equivalent: ratio {v['ratio']:.2f}x "
                f"within the equivalence band (95% CI {lo:.2f}-{hi:.2f}, "
                f"n={v['n']})")
    lead = v["a"] if v["ratio"] > 1 else v["b"]
    mag = v["ratio"] if v["ratio"] > 1 else 1 / v["ratio"]
    return (f"{v['a']} vs {v['b']} undecided: {lead} ahead by {mag:.2f}x but "
            f"the 95% CI ({lo:.2f}-{hi:.2f}, n={v['n']}) spans the equivalence "
            f"band")
