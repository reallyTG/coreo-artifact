"""Choose which properties enter the joint model fit.

`analyzer.fit_model_for_metric_and_features` tries one model per assignment of
a complexity class to a feature, so its cost is `len(complexity_classes) **
len(features)`. At six properties that is 46,656 fits and about sixteen
seconds; at nine it is 10,077,696 and roughly an hour. Grammar-derived
properties push a subject past that count.

Cost is not the only reason to select. Grammar counts correlate strongly with
each other, because every count rises with input length. Most of those ten
million models are near-duplicates of each other, so the search is expensive
*and* redundant.

Selection runs in two steps, in this order:

  1. Relevance. Score each property by how strongly it tracks any metric on
     any system, OR how strongly it tracks the RATIO between two systems on
     that metric, and drop the ones that track neither.
  2. Redundancy. Walk the survivors from most relevant down, keeping a
     property only when it is not already explained by one that is kept.

The two relevance criteria are not the same question, and on a comparative
subject they can rank the properties in nearly opposite orders. A property
that marks the code path one version changed can be the best predictor of
WHICH VERSION WINS and among the worst of how long the input takes. Scoring on
the metric alone drops it, the loop never targets it, and the two versions are
reported equivalent while the corpus holds a difference in the region that
property names.

So a property can be irrelevant to absolute cost and decisive for the
comparison. Since `compare.py` exists to state where one system beats another,
selection has to score for that question too, and the property's score is the
better of the two. The ratio criterion is skipped when there is one system,
where it has nothing to say.

The set is chosen once per subject, over every metric and system pooled, so
all systems are modelled on the same properties and their fits stay
comparable. Selection never touches the single-feature plots and fits: those
are linear in the property count and are where a dropped property still shows
up, which is what keeps the drop honest rather than hidden.
"""
import csv
import math

import scipy.stats as ss


def _rho(xs, ys):
    """Spearman |rho|, or 0.0 when either side is constant or degenerate."""
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return 0.0
    r = ss.spearmanr(xs, ys).statistic
    return 0.0 if (r is None or math.isnan(r)) else abs(r)


def _read(summary_csv, metrics, properties):
    """Return (rows_by_system, property columns) as floats, skipping bad cells."""
    by_system = {}
    with open(summary_csv) as fh:
        for row in csv.DictReader(fh):
            cols = by_system.setdefault(row.get("function_name", "?"), {})
            for key in list(metrics) + list(properties):
                try:
                    cols.setdefault(key, []).append(float(row[key]))
                except (KeyError, TypeError, ValueError):
                    cols.setdefault(key, []).append(float("nan"))
    return by_system


def _read_paired(summary_csv, metrics, properties):
    """Return {input_id: ({system: {metric: v}}, {property: v})}.

    Properties are a function of the input, so they are the same on every row
    for an input; the metrics are not, and pairing them is the whole point.
    """
    rows = {}
    with open(summary_csv) as fh:
        for row in csv.DictReader(fh):
            key = row.get("input_id")
            if key is None:
                continue
            systems, props = rows.setdefault(key, ({}, {}))
            per = systems.setdefault(row.get("function_name", "?"), {})
            for metric in metrics:
                try:
                    per[metric] = float(row[metric])
                except (KeyError, TypeError, ValueError):
                    pass
            for prop in properties:
                try:
                    props[prop] = float(row[prop])
                except (KeyError, TypeError, ValueError):
                    pass
    return rows


def _ratio_relevance(summary_csv, metrics, properties):
    """{property -> max |rho| against a between-system ratio}, or {} if n/a.

    One score per property: the strongest association it has with the ratio
    between any two systems on any metric. Ratios are formed per input and
    only where both systems produced a positive value, so an input one system
    refused contributes to neither the numerator nor the count.
    """
    rows = _read_paired(summary_csv, metrics, properties)
    if not rows:
        return {}
    systems = sorted({s for per, _ in rows.values() for s in per})
    if len(systems) < 2:
        return {}

    best = {p: 0.0 for p in properties}
    for i, a in enumerate(systems):
        for b in systems[i + 1:]:
            for metric in metrics:
                ratios, keep = [], []
                for per, props in rows.values():
                    va = per.get(a, {}).get(metric)
                    vb = per.get(b, {}).get(metric)
                    if not va or not vb or va <= 0 or vb <= 0:
                        continue
                    if math.isnan(va) or math.isnan(vb):
                        continue
                    ratios.append(vb / va)
                    keep.append(props)
                if len(ratios) < 3:
                    continue
                for prop in properties:
                    xs, ys = _clean_pair([p.get(prop, float("nan")) for p in keep],
                                         ratios)
                    best[prop] = max(best[prop], _rho(xs, ys))
    return best


def _clean_pair(xs, ys):
    """Drop index positions where either series is NaN."""
    keep = [(x, y) for x, y in zip(xs, ys)
            if not (math.isnan(x) or math.isnan(y))]
    if not keep:
        return [], []
    a, b = zip(*keep)
    return list(a), list(b)


def select(summary_csv, metrics, properties, max_features=4,
           corr_threshold=0.8, relevance_floor=0.05, protect=(),
           return_groups=False):
    """Return (selected, report_lines) for the joint fit.

    `selected` preserves the caller's property order so downstream output does
    not depend on scoring noise. `report_lines` names every dropped property
    and why, for printing.
    """
    properties = list(properties)
    by_system = _read(summary_csv, metrics, properties)
    if not by_system:
        out = (properties[:max_features],
               ["[select] no rows; passing properties through"])
        if return_groups:
            return (*out, {"groups": {p: [] for p in properties[:max_features]},
                           "relevance": {}})
        return out

    # 1. Relevance: the strongest association this property has with any metric
    #    on any system. Max rather than mean, so a property that drives one
    #    system and not the others still survives.
    absolute = {}
    for prop in properties:
        best = 0.0
        for cols in by_system.values():
            for metric in metrics:
                xs, ys = _clean_pair(cols.get(prop, []), cols.get(metric, []))
                best = max(best, _rho(xs, ys))
        absolute[prop] = best

    # ...and the strongest association it has with the RATIO between two
    # systems, which is a different question and the one `compare.py` asks. A
    # property's score is the better of the two: irrelevant to absolute cost
    # is not irrelevant to which system wins.
    comparative = _ratio_relevance(summary_csv, metrics, properties)
    relevance = {p: max(absolute[p], comparative.get(p, 0.0)) for p in properties}

    # Rank by BOTH criteria round-robin rather than by the better score. Taking
    # the max settles which properties clear the floor, but it decides the cap
    # badly: a property that is decisive for the comparison and mediocre for
    # the metric loses its slot to one that is good for the metric and useless
    # for the comparison, which is backwards for a comparative profiler.
    #
    # Interleaving gives each criterion its turn instead of letting one order
    # the whole list.
    ranked = sorted(properties, key=lambda p: absolute[p], reverse=True)
    if comparative:
        by_ratio = sorted(properties, key=lambda p: comparative[p], reverse=True)
        interleaved = []
        for a, b in zip(ranked, by_ratio):
            for prop in (a, b):
                if prop not in interleaved:
                    interleaved.append(prop)
        ranked = interleaved
    report = ["[select] relevance (max |rho| vs any metric on any system): "
              + ", ".join(f"{p}={absolute[p]:.2f}" for p in ranked)]
    if comparative:
        report.append("[select] comparative relevance (max |rho| vs a "
                      "between-system ratio): "
                      + ", ".join(f"{p}={comparative[p]:.2f}" for p in ranked))
        lifted = [p for p in ranked if comparative.get(p, 0.0) > absolute[p] + 0.05]
        if lifted:
            report.append("[select] scored on the comparison rather than on the "
                          "metric: " + ", ".join(
                              f"{p} ({absolute[p]:.2f} -> {comparative[p]:.2f})"
                              for p in lifted))

    # A property whose axis the loop has not finished pushing is exempt from the
    # relevance floor. Its score is computed on the corpus that exists, and if
    # the loop has not gone looking along that axis then "tracks no metric"
    # says more about the sampling than about the property -- and dropping it
    # stops the loop ever collecting the data that would prove otherwise.
    weak = [p for p in ranked
            if relevance[p] < relevance_floor and p not in set(protect)]
    kept_unexplored = [p for p in ranked
                       if relevance[p] < relevance_floor and p in set(protect)]
    for p in kept_unexplored:
        report.append(f"[select] kept {p} despite |rho|={relevance[p]:.2f}: "
                      f"its axis is not explored yet, so a low score there is "
                      f"absence of data rather than absence of effect")
    ranked = [p for p in ranked if p not in weak]
    for p in weak:
        report.append(f"[select] dropped {p}: tracks no metric "
                      f"(|rho|={relevance[p]:.2f} < {relevance_floor})")

    # 2. Redundancy: pooled across systems, since the property values are the
    #    same inputs measured by each. Take the largest correlation seen.
    def pair_rho(a, b):
        best = 0.0
        for cols in by_system.values():
            xs, ys = _clean_pair(cols.get(a, []), cols.get(b, []))
            best = max(best, _rho(xs, ys))
        return best

    kept = []
    # Which properties each kept one absorbed as redundant. At |rho| >= the
    # threshold the data cannot tell the members of a group apart, so naming
    # the representative and discarding the rest overstates what was learned:
    # an absorbed property may be the axis the change under test actually
    # moves. The group is what the loop found; the representative is an
    # arbitrary member of it.
    groups = {}
    for prop in ranked:
        if len(kept) >= max_features:
            report.append(f"[select] dropped {prop}: over the "
                          f"{max_features}-property cap")
            continue
        clash = next(((k, r) for k in kept
                      if (r := pair_rho(prop, k)) >= corr_threshold), None)
        if clash:
            groups.setdefault(clash[0], []).append(prop)
            report.append(f"[select] dropped {prop}: |rho|={clash[1]:.2f} "
                          f"with {clash[0]}, which is already kept")
        else:
            kept.append(prop)
            groups.setdefault(prop, [])

    selected = [p for p in properties if p in kept]
    for k in selected:
        if groups.get(k):
            report.append(f"[select] {k} stands for "
                          f"{', '.join(groups[k])} (indistinguishable here)")
    report.append(f"[select] joint fit uses {len(selected)} of "
                  f"{len(properties)} properties: {', '.join(selected)} "
                  f"({6 ** len(selected):,} model fits)")
    if return_groups:
        # Relevance rides along because it is what a reader needs to judge a
        # selected property, and it must NOT be used to filter. A relative
        # floor drops a weak property that decides the comparison as readily
        # as a weak one that is non-causal. Nothing in the numbers separates
        # weak-but-decisive from weak-and-leftover, so the honest move is to
        # report the score, not to threshold on it.
        return selected, report, {
            "groups": {k: groups.get(k, []) for k in selected},
            "relevance": {k: round(relevance.get(k, 0.0), 2) for k in selected},
        }
    return selected, report
