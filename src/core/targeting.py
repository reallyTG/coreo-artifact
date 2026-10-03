"""Corpus-aware targeting: pick regions to push into, derive structural targets.

Reads the corpus (source of truth) and, for each metric, proposes regions:
- extreme: top/bottom k% by metric (find expensive / cheap inputs)
- sparse:  under-sampled metric bins (fill coverage gaps)
- divergence: inputs where the functionally-equivalent systems differ MOST in
  the metric (the comparative-fuzzing endgame)

Each region is turned into (1) a STRUCTURAL property box -- the span of each
property over the region's rows -> emitted as `where prop(<start>) >= lo` /
`<= hi` clauses (model-directed targeting; works without running the SUT during
generation), and (2) seed input hashes (read from the corpus's content-addressed
input files).
"""
import hashlib
import json
import math
import pathlib
from collections import defaultdict

# Frontier ledger: the observed max of each property at the moment we last asked
# for inputs beyond it. Lives beside corpus.csv and persists across runs, the
# same way the corpus does, because "has the frontier moved?" is only meaningful
# over the accumulated corpus rather than one run's slice.
FRONTIER_FILE = "frontier.json"


def _measured(rows, key):
    """Rows carrying a real observation of `key`.

    A censored or failed measurement is stored as NaN (see corpus.upsert).
    Every comparison against NaN is False, so leaving one in would silently
    scramble a sort or land it in an arbitrary bin. Metric-axis regions are
    therefore chosen over measured rows only; property-axis regions still see
    every row, since properties are always known.
    """
    out = []
    for r in rows:
        try:
            if math.isfinite(float(r.get(key, ""))):
                out.append(r)
        except (TypeError, ValueError):
            continue
    return out


def _f(row, key):
    try:
        return float(row.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def _prop_box(rows, properties):
    box = {}
    for p in properties:
        vals = [_f(r, p) for r in rows]
        if vals:
            box[p] = (min(vals), max(vals))
    return box


def _extreme(rows, metric, k_frac):
    if not rows:
        return []
    ordered = sorted(rows, key=lambda r: _f(r, metric))
    n = max(1, int(len(ordered) * k_frac))
    return [
        {"label": f"{metric}_high", "rows": ordered[-n:]},
        {"label": f"{metric}_low", "rows": ordered[:n]},
    ]


def _sparse(rows, metric, n_bins, n_regions):
    if not rows:
        return []
    vals = [_f(r, metric) for r in rows]
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return []
    step = (hi - lo) / n_bins
    bins = defaultdict(list)
    for r in rows:
        b = min(n_bins - 1, int((_f(r, metric) - lo) / step))
        bins[b].append(r)
    sparsest = sorted((rs for rs in bins.values() if rs), key=len)[:n_regions]
    return [{"label": f"{metric}_sparse{i}", "rows": rs} for i, rs in enumerate(sparsest)]


def _divergence(rows, metric, k_frac):
    by_input = defaultdict(dict)
    for r in rows:
        by_input[r["input_hash"]][r["function_name"]] = r
    spreads = []
    for fnrows in by_input.values():
        if len(fnrows) >= 2:
            vals = [_f(r, metric) for r in fnrows.values()]
            spreads.append((max(vals) - min(vals), list(fnrows.values())))
    if not spreads:
        return []
    spreads.sort(key=lambda s: s[0], reverse=True)
    n = max(1, int(len(spreads) * k_frac))
    region_rows = [r for _, frs in spreads[:n] for r in frs]
    return [{"label": f"{metric}_divergence", "rows": region_rows}]


# --- property-axis regions: target the property space directly (structural-only
#     generation lets us *control* properties during generation, unlike metrics) ---

def _property_edge(rows, prop, k_frac, sites=None):
    """Push the high end of an observed property (extremes often drive cost).

    Realised structurally where a repetition governs the property, for the
    reason every other kind is: telling the grammar to produce the shape is
    both faster and certain, where asking the search to find it can return
    nothing.
    """
    ordered = sorted(rows, key=lambda r: _f(r, prop))
    n = max(1, int(len(ordered) * k_frac))
    top = ordered[-n:]
    lo, hi = _f(top[0], prop), _f(top[-1], prop)
    if hi <= lo:
        return []
    site = (sites or {}).get(prop)
    if site is None:
        return [{"label": f"{prop}_edge", "rows": top, "prop_box": {prop: (lo, hi)}}]
    out = []
    for i, (rlo, rhi) in enumerate(_site_band(rows, prop, site, lo, hi)):
        out.append({"label": f"{prop}_edge{i}", "rows": [], "prop_box": {},
                    "structural": True, "rewrite": [(site.nt, rlo, rhi)],
                    "max_nodes": _node_budget(site, rhi),
                    "note": f"{site.nt}{{{rlo},{rhi}}} for the top {k_frac:.0%} "
                            f"of {prop} ([{lo:g},{hi:g}])"})
    return out


def _property_sparse(rows, prop, n_bins, n_regions, sites=None):
    """Fill under-sampled bins of a property axis (coverage).

    Realised structurally when a repetition governs the property, for the same
    reason the frontier request is: a bin is a shape the grammar can be told to
    produce, and telling it is both faster and certain, where asking the search
    to find the bin can come back empty.
    """
    vals = [_f(r, prop) for r in rows]
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return []
    step = (hi - lo) / n_bins
    counts = [0] * n_bins
    for v in vals:
        counts[min(n_bins - 1, int((v - lo) / step))] += 1
    site = (sites or {}).get(prop)
    out = []
    for b in sorted(range(n_bins), key=lambda i: counts[i])[:n_regions]:
        blo, bhi = lo + b * step, lo + (b + 1) * step
        center = (blo + bhi) / 2
        seeds = sorted(rows, key=lambda r: abs(_f(r, prop) - center))[:6]
        if site is not None:
            for i, (rlo, rhi) in enumerate(_site_band(rows, prop, site, blo, bhi)):
                out.append({"label": f"{prop}_sparse{b}_{i}", "rows": [],
                            "prop_box": {}, "structural": True,
                            "rewrite": [(site.nt, rlo, rhi)],
                            "max_nodes": _node_budget(site, rhi),
                            "note": f"{site.nt}{{{rlo},{rhi}}} for {prop} "
                                    f"in [{blo:g},{bhi:g}]"})
        else:
            out.append({"label": f"{prop}_sparse{b}", "rows": seeds,
                        "prop_box": {prop: (blo, bhi)}})
    return out


JOINT_FILE = "joint.json"
# Iterations a joint band may fail to improve its objective before it is retired
# and a fresh one opened elsewhere.
JOINT_STALLS = 2
# Improvement counted as progress, in units of the objective property.
JOINT_EPS = 0.005


def load_joint(corpus):
    path = corpus.root / JOINT_FILE
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (ValueError, OSError):
        return {}


def save_joint(corpus, ledger):
    (corpus.root / JOINT_FILE).write_text(json.dumps(ledger, indent=2, sort_keys=True))


def _dominance(rows, metrics, properties, sites, n_bins=6):
    """Regions where settling a metric would change the OVERALL verdict.

    `_compare` asks for inputs wherever a single metric's interval is wide. This
    asks only where the answer depends on it, which is the same principle
    `core.design` uses for model ties: sample where the conclusion would move,
    not merely where the uncertainty is largest.

    The pivotal case is `ahead_incomplete` -- one system winning some metrics
    with others undecided. Settling those turns it into DOMINATES, which lets
    the other system be dropped from consideration, or into a TRADE-OFF, which
    says no single answer exists. Either is actionable and neither is available
    while the metrics stay undecided.

    A pair already known to trade off is skipped however wide its remaining
    intervals are: each side already wins something, so nothing a third metric
    could say changes the overall verdict, and inputs bought there buy nothing.
    """
    from core import compare

    want = {}
    names = compare.systems(rows)
    if len(names) < 2 or len(metrics) < 2:
        return []
    for prop in properties:
        prop_of = {}
        for r in rows:
            v = _f(r, prop)
            if v is not None:
                prop_of[r["input_hash"]] = v
        if not prop_of:
            continue
        bins = compare.property_bins(prop_of.values(), n_bins)
        for i, (blo, bhi) in enumerate(bins):
            top = i == len(bins) - 1
            sub = [r for r in rows
                   if compare.in_region(prop_of.get(r["input_hash"]), blo, bhi, top)]
            if len({r["input_hash"] for r in sub}) < compare.MIN_PAIRS:
                continue
            for j, a in enumerate(names):
                for b in names[j + 1:]:
                    d = compare.dominance(sub, a, b, metrics)
                    if d["verdict"] not in ("ahead_incomplete", "undecided"):
                        continue
                    key = (prop, round(blo, 6), round(bhi, 6))
                    want.setdefault(key, []).append(
                        f"{a} vs {b} ({', '.join(d['undecided'])} undecided)")

    out = []
    for (prop, lo, hi), why in want.items():
        site = (sites or {}).get(prop)
        note = (f"settling {prop} {compare.region_label(lo, hi)} would decide "
                f"{len(why)} dominance verdict(s): {why[0]}"
                + (f" and {len(why)-1} more" if len(why) > 1 else ""))
        base = {"bin": (prop, lo, hi)}
        if site is not None:
            for i, (rlo, rhi) in enumerate(_site_band(rows, prop, site, lo, hi)):
                out.append({**base, "label": f"{prop}_dominance{i}", "rows": [],
                            "prop_box": {}, "structural": True,
                            "rewrite": [(site.nt, rlo, rhi)],
                            "max_nodes": _node_budget(site, rhi),
                            "note": f"{note} -> {site.nt}{{{rlo},{rhi}}}"})
        else:
            seeds = sorted(rows, key=lambda r: abs(_f(r, prop) - (lo + hi) / 2))[:6]
            out.append({**base, "label": f"{prop}_dominance", "rows": seeds,
                        "prop_box": {prop: (lo, hi)}, "note": note})
    return out


def _compare(rows, metrics, properties, sites, n_bins=6):
    """Regions where the comparison between two systems is not yet decided.

    Where statistical confidence is low in a region, the loop requests more
    inputs in that region to gather evidence. `core.compare` marks a bin
    UNDECIDED when the confidence interval on the per-input ratio spans the
    equivalence band -- the systems differ there, or they do not, and the data
    cannot say which. That is the one kind of region where more inputs are
    guaranteed to buy something.

    Deduplicated across system pairs and metrics: the same bin is usually
    undecided for several pairs at once, and it only needs asking for once.
    """
    from core import compare

    want = {}
    names = compare.systems(rows)
    for metric in metrics:
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                for prop in properties:
                    for reg in compare.undecided(
                            compare.by_region(rows, a, b, metric, prop, n_bins)):
                        key = (prop, round(reg["lo"], 6), round(reg["hi"], 6))
                        want.setdefault(key, []).append(f"{a} vs {b} on {metric}")

    out = []
    for (prop, lo, hi), why in want.items():
        site = (sites or {}).get(prop)
        note = (f"{len(why)} comparison(s) undecided in "
                f"{prop} {compare.region_label(lo, hi)}: {why[0]}"
                + (f" and {len(why)-1} more" if len(why) > 1 else ""))
        base = {"bin": (prop, lo, hi)}
        if site is not None:
            for i, (rlo, rhi) in enumerate(_site_band(rows, prop, site, lo, hi)):
                out.append({**base, "label": f"{prop}_undecided{i}", "rows": [],
                            "prop_box": {}, "structural": True,
                            "rewrite": [(site.nt, rlo, rhi)],
                            "max_nodes": _node_budget(site, rhi),
                            "note": f"{note} -> {site.nt}{{{rlo},{rhi}}}"})
        else:
            seeds = sorted(rows, key=lambda r: abs(_f(r, prop) - (lo + hi) / 2))[:6]
            out.append({**base, "label": f"{prop}_undecided", "rows": seeds,
                        "prop_box": {prop: (lo, hi)}, "note": note})
    return out


def _joint(rows, properties, sites, ledger=None, k_frac=0.15, narrow=0.5):
    """Regions naming a COMBINATION the corpus does not occupy.

    Every other kind names a single property, so none can ask for a low value
    of an intensive property (a ratio) AND a high value of an extensive one (a
    count). A corpus built one axis at a time leaves that hole: the ratio
    spans its whole range on small inputs and a narrow band on large ones. A
    property with no variation where it matters scores as irrelevant in
    loop-front selection.

    A pair is worth requesting when the intensive property's spread inside the
    band is much narrower than its spread overall; the direction asked for is
    whichever end went missing. Each half is realised the way it can be: the
    extensive property by rewriting the repetition that governs it, the
    intensive one as a soft objective, since nothing structural controls a ratio
    and a hard clause on one gives the search no gradient at all.

    The band is HELD across iterations, and that is what makes progress
    amortise. Recomputed each round it would chase the frontier `prop_beyond`
    is pushing, so the previous best inputs could not parse against the moved
    bound and the descent would restart. Held, with the best inputs so far as
    seeds, the objective keeps improving on the same band. It is retired once
    it stops paying, and a fresh one opens at the current top.
    """
    ext = [p for p in properties if (sites or {}).get(p) is not None]
    inten = [p for p in properties if (sites or {}).get(p) is None]
    out = []
    for e in ext:
        ordered = sorted(rows, key=lambda r: _f(r, e))
        n = max(1, int(len(ordered) * k_frac))
        top = ordered[-n:]
        top_lo = _f(top[0], e)
        if _f(top[-1], e) <= 0:
            continue
        for i in inten:
            allv = [_f(r, i) for r in rows]
            if not allv or max(allv) - min(allv) <= 0:
                continue
            span = max(allv) - min(allv)

            key = f"{e}|{i}"
            entry = (ledger or {}).get(key, {})
            if entry.get("retired"):
                continue

            # The window the band covers: the one it was opened for if it is
            # being held, otherwise the current top of the extensive property.
            # Everything below -- whether the pair is worth asking for, whether
            # the last round paid, and which inputs may seed it -- is measured
            # over THIS window. Measuring it over the current frontier instead
            # would read the intensive property where the band is not, see no
            # improvement where there was one, and retire the pair early.
            held = bool(entry.get("band"))
            w_lo, w_hi = (entry["window"] if held and entry.get("window")
                          else (top_lo, max(top_lo * 1.2, top_lo + 1)))
            win = [r for r in rows if w_lo <= _f(r, e) <= w_hi]
            if not win:
                win = top
            winv = [_f(r, i) for r in win]

            if not held and (max(winv) - min(winv)) / span > narrow:
                continue                 # already spread here; nothing to ask

            gap_low = min(winv) - min(allv)
            gap_high = max(allv) - max(winv)
            direction = entry.get("direction") or (
                "minimizing" if gap_low >= gap_high else "maximizing")
            best_now = min(winv) if direction == "minimizing" else max(winv)

            site = sites[e]
            if held:
                prev = entry.get("best")
                gain = (prev - best_now) if direction == "minimizing" else (best_now - prev)
                entry["stalls"] = 0 if (prev is None or gain > JOINT_EPS) \
                    else entry.get("stalls", 0) + 1
                if entry["stalls"] >= JOINT_STALLS:
                    entry.update(retired=True, best=best_now)
                    if ledger is not None:
                        ledger[key] = entry
                    continue
                rlo, rhi = entry["band"]
            else:
                bands = _site_band(rows, e, site, w_lo, w_hi, bands=1)
                if not bands:
                    continue
                rlo, rhi = bands[0]
                entry["stalls"] = 0
            entry.update(band=[rlo, rhi], window=[w_lo, w_hi], best=best_now,
                         direction=direction, extensive=e, intensive=i)
            if ledger is not None:
                ledger[key] = entry

            out.append({
                "label": f"{e}_x_{i}_joint",
                "rows": [], "prop_box": {}, "structural": True,
                "rewrite": [(site.nt, rlo, rhi)],
                "soft": [f"{direction} {i}(<start>)"],
                "objective": (i, direction),
                "seed_within": (e, w_lo, w_hi),
                "max_nodes": _node_budget(site, rhi),
                "note": (f"{i} spans {min(allv):g}..{max(allv):g} overall, "
                         f"{min(winv):g}..{max(winv):g} at {e} in "
                         f"[{w_lo:g},{w_hi:g}]; {direction} it at "
                         f"{site.nt}{{{rlo},{rhi}}}"
                         + (f" (held, best {entry['best']:.4g})" if held else "")),
            })
    return out


# How far past the current repetition scale each structural rung reaches. The
# bands double per rung; each rung is one generation attempt, and the ledger
# remembers which have been spent.
#
# One rung: ask for 2x the observed scale, and if that returns nothing, pin.
# The frontier still advances (a hit moves the max and the next iteration asks
# for 2x the new max). More rungs would jump to 4x-16x after a miss, which with
# auto-stratified exploration's larger maxima builds trees the machine cannot
# hold (on JSONPath: swap full, a 60-minute run took 97).
STRUCTURAL_RUNGS = 1
# Rungs available to a property with no governing repetition, where the only
# levers are the node budget and a soft objective.
SEARCH_RUNGS = 2


def _site_scale(rows, site, max_repetition):
    """Roughly how many repetitions the corpus has been getting at `site`.

    Prefers the site non-terminal's own count property when the corpus carries
    it, since that is the quantity being rewritten. Falls back to the language
    bound, and then to `max_repetition`, which is what bounds a free `*` or
    `+`.
    """
    from core import grammar_props

    name = grammar_props.property_name(site.nt)
    observed = [_f(r, name) for r in rows if name in r]
    if observed and max(observed) > 0:
        return max(observed)
    if site.lang_max < grammar_props.INF:
        return site.lang_max
    return max_repetition


# Node allowance per repetition when the grammar cannot bound it (a recursive
# body). Generous on purpose: too small is silently wrong, too large is slow.
FALLBACK_NODES_PER_ITEM = 60
# Never ask for fewer nodes than Fandango's own default would give.
MIN_STRUCTURAL_NODES = 4000
# ...and never ask for more than one machine can build. The ladder doubles the
# band every rung, so the node budget doubles with it: uncapped, jsonpath_js
# goes 33k, 80k, 188k, 447k, 1.04M, 2.49M nodes over ten iterations, asking for
# `<segment>{23044,27652}`, and the operating system kills the run for memory
# during the final fit. A budget past this ceiling is also of
# little use even when it fits: Fandango takes the cheapest derivation for
# every element once the budget binds, so the count moves and the content
# degenerates. A property whose next rung needs more than this pins with
# reason "budget" instead, which the frontier report then states.
#
# 30,000 because at 200,000 a JSONPath request with a population of 20 fills
# 16 GB of swap.
MAX_STRUCTURAL_NODES = 30_000
# Upper bound for a frontier request with no governing repetition: at most this
# multiple of the observed max (see _search_beyond).
SEARCH_REACH = 2
# Free-repetition ceiling for the soft-objective rung of _search_beyond.
SEARCH_MAX_REPETITION = 400


def _recursive_cap(site, count):
    """Clamp a requested repetition count for a site whose body can recurse.

    Breadth and depth MULTIPLY under recursion, so a band asking for 200
    repetitions applies at every level. `grammar_props.stratify_axes` caps
    this for EXPLORATION bands, and the targeted path needs the same cap:
    without it `_structural_beyond` keeps doubling toward `max_repetition`
    with a node budget scaled to match, and exhausts memory.

    A site with no finite `nodes_per_item` is exactly the recursive case --
    `expansion_nodes` returns None when some count beneath it is unbounded.
    """
    from core import grammar_props

    if site.nodes_per_item is None:
        return min(count, grammar_props.RECURSIVE_CEILING)
    return count


def _node_budget(site, count):
    """Nodes a request for `count` repetitions of `site` needs.

    Without this the count is honoured and the CONTENT is not. Fandango takes
    the cheapest derivation for every element once the budget binds, so a
    200-repetition band at the default 200 nodes returns near-identical
    elements. The count moves and the data is worthless -- the failure mode
    a frontier report cannot see, because the property it tracks did move.
    """
    return _clamp_nodes(_node_budget_raw(site, count))


def _node_budget_raw(site, count):
    """What the request would need, before the ceiling is applied."""
    per = site.nodes_per_item or FALLBACK_NODES_PER_ITEM
    count = _recursive_cap(site, count)
    return max(MIN_STRUCTURAL_NODES, int(count * per * 1.5))


def _clamp_nodes(nodes):
    """Hold a node budget under the ceiling; see MAX_STRUCTURAL_NODES."""
    return min(int(nodes), MAX_STRUCTURAL_NODES)


def _site_band(rows, prop, site, target_lo, target_hi, bands=3):
    """Repetition bands that should land `prop` inside [target_lo, target_hi].

    The repetition count and the property are not the same quantity -- a list's
    length is its `<more_x>` count plus one, and a count deeper in the tree
    rises at whatever rate the rest of the grammar dictates -- so
    the conversion is read off the corpus rather than assumed: the median ratio
    of the site's own count to the property, over rows that have both.

    Several narrow bands, not one wide one, because Fandango lands on a band's
    lower bound and stays there. One band per request would make every
    structural request a spike at a single value, which is the wrong shape for
    fitting anything.
    """
    from core import grammar_props

    if target_hi is not None and target_lo <= 0 and target_hi <= 0:
        # The zero region of `compare.property_bins`: the inputs it asks for
        # have none of the construct, so the band is exactly zero repetitions.
        # The general path below floors the band at 1..2, which would ask for
        # the one thing the region excludes.
        return [(0, 0)]
    name = grammar_props.property_name(site.nt)
    ratios = []
    for r in rows:
        p, s = _f(r, prop), _f(r, name)
        if p > 0 and s > 0:
            ratios.append(s / p)
    ratio = sorted(ratios)[len(ratios) // 2] if ratios else 1.0
    lo, hi = max(1.0, target_lo * ratio), max(2.0, (target_hi or target_lo) * ratio)
    if hi <= lo:
        hi = lo * 1.2
    lo, hi = _recursive_cap(site, lo), _recursive_cap(site, hi)
    step = max(1.0, (hi - lo) / bands)
    out = []
    for b in range(bands):
        blo = int(lo + b * step)
        out.append((blo, max(blo + 1, int(blo + max(2, step)))))
    return out


def _structural_beyond(rows, prop, site, entry, max_repetition,
                       allow_beyond_language=False):
    """Widen the repetition governing `prop`, instead of constraining `prop`.

    The alternative is a hard `where prop >= max+1` clause, which asks the
    search to find a shape the grammar can be told to produce. The clause is
    slower, and it is also the case that fails outright rather than degrading,
    since an unsatisfiable hard constraint yields no inputs at all.

    No `where` clause is emitted alongside the rewrite. Adding one would
    reintroduce exactly that failure whenever the property is not an exact
    multiple of the repetition count.

    A finite bound written in the grammar is respected rather than widened,
    because a bound like `<x>{0,40}` is part of the language under test and
    going past it changes L(G). The run says so and pins;
    `allow_beyond_language` turns it into the deliberate experiment it should
    be.
    """
    rung = entry.get("rung", 0) + 1
    if rung > STRUCTURAL_RUNGS:
        entry.update(pinned=True, reason="search")
        return []
    base = max(1.0, _site_scale(rows, site, max_repetition))
    lo = _recursive_cap(site, int(base * (2 ** rung)))
    if site.lang_max < float("inf") and lo > site.lang_max:
        if not allow_beyond_language:
            entry.update(pinned=True, reason="language",
                         language_bound=site.lang_max, site=site.nt)
            return []
        entry["widened_language"] = True
    hi = lo + max(2, lo // 5)
    needed = _node_budget_raw(site, hi)
    if needed > MAX_STRUCTURAL_NODES:
        # Asking anyway would either exhaust memory or, once the budget binds,
        # return the count with degenerate content. Say so and stop here.
        entry.update(pinned=True, reason="budget", site=site.nt,
                     needed_nodes=needed, node_cap=MAX_STRUCTURAL_NODES,
                     band=[lo, hi])
        return []
    entry.update(rung=rung, pending=True, pinned=False, constant=False,
                 site=site.nt, band=[lo, hi], reason=None)
    return [{"label": f"{prop}_beyond", "rows": [], "prop_box": {},
             "structural": True, "rewrite": [(site.nt, lo, hi)],
             "max_nodes": _node_budget(site, hi),
             "note": f"{site.nt}{{{lo},{hi}}} (rung {rung}, "
                     f"{_node_budget(site, hi)} nodes)"}]


def _search_beyond(rows, prop, entry, new_lo, seeds):
    """Push a property no repetition governs: node budget, then a soft objective.

    This is the recursion-driven case (nesting depth, selector depth):
    there is no `{lo,hi}` to rewrite, so the hard clause is all there is. Rung 1
    keeps it and raises the node budget; rung 2 drops it for `maximizing`, which
    degrades to "as far as it got" instead of returning nothing.
    """
    rung = entry.get("rung", 0) + 1
    if rung > SEARCH_RUNGS:
        entry.update(pinned=True, reason="search")
        return []
    # Bounded above at SEARCH_REACH x the observed max. Unbounded, rung 2's
    # soft objective with max_repetition 200*4**rung (3,200 on every free
    # repetition, recursive ones included) asks JSONPath for queries past
    # 10,647 characters and fills the machine's swap. The window [max+1,
    # 2*max] is wide, not a needle the GA has to hit exactly.
    upper = max(new_lo + 2, int(SEARCH_REACH * (new_lo - 1)))
    entry.update(rung=rung, pending=True, pinned=False, constant=False,
                 requested=[new_lo, upper], reason=None)
    region = {"label": f"{prop}_beyond", "rows": seeds,
              "max_nodes": _clamp_nodes(4000 * (4 ** rung))}
    if rung == 1:
        region["prop_box"] = {prop: (new_lo, upper)}
    else:
        region["prop_box"] = {prop: (None, upper)}
        region["structural"] = True      # the objective does the work below the cap
        region["soft"] = [f"maximizing {prop}(<start>)"]
        region["max_repetition"] = min(200 * (4 ** rung), SEARCH_MAX_REPETITION)
    region["note"] = f"rung {rung}"
    return [region]


def _property_beyond(rows, prop, ledger, sites=None, max_repetition=20,
                     allow_beyond_language=False, reach_frac=0.1):
    """Extrapolate UP and AWAY from the observed max of a property.

    e.g. a property observed in [0,34] -> request [35,37], seeded with the
    near-boundary inputs (those in [~30,34]) to help evolution climb.

    Two ways this request is known in advance to return nothing, and each
    would cost a full generation attempt per iteration:

    * The property never varied over the whole corpus. There is no frontier to
      push, only a value the grammar cannot move off. `_property_edge` and
      `_property_sparse` decline this case too.
    * The last request beyond this property's max came back empty and the max
      has not moved since. The property is pinned, whether by a repetition
      bound, by an alternative count, or by a production the grammar does not
      contain at all. Deciding this statically would mean reasoning about
      arbitrary Python over a derivation tree, so it is decided from the
      corpus: ask once, and do not ask again until something else moves the
      max.

    A pinned property is a fact worth reporting rather than only a request
    worth skipping -- it is the loop saying the grammar, not the system, is the
    limit here. See `frontier_report`.
    """
    vals = [_f(r, prop) for r in rows]
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        entry = ledger.setdefault(prop, {})
        entry.update(last_max=hi, pinned=True, constant=True)
        entry["misses"] = entry.get("misses", 0)
        return []
    prev = _resolve(ledger, prop, hi)
    if prev is not None and prev.get("pinned"):
        return []
    span = hi - lo
    reach = max(2, round(span * reach_frac))
    new_lo = hi + 1                                # just beyond the observed max
    seed_lo = hi - reach - 1                       # near-boundary inputs as seeds
    seeds = [r for r in rows if _f(r, prop) >= seed_lo]
    if not seeds:
        seeds = sorted(rows, key=lambda r: _f(r, prop))[-6:]
    entry = ledger.setdefault(prop, {})
    entry["last_max"] = hi          # NOT misses: `_resolve` just counted one

    site = (sites or {}).get(prop)
    if site is not None:
        return _structural_beyond(rows, prop, site, entry, max_repetition,
                                  allow_beyond_language)
    # Not `[hi+1, hi+reach]`, for the rung that still uses a clause: a narrow
    # window is a needle the GA has to hit exactly, and hitting it buys nothing
    # -- a frontier request wants to go further than the corpus has been, not
    # to land inside a slice just past it.
    return _search_beyond(rows, prop, entry, new_lo, seeds)


def _discriminating(rows, metric, prop, reach=None):
    """Regions whose data would settle a model the corpus cannot decide.

    The other kinds here target the input space: extremes, sparse bins, places
    where two systems diverge. This one targets the MODEL. `model_fit.near_ties`
    names the complexity classes a corpus does not separate, and `core.design`
    simulates which region's data would separate them; see that module for why
    the obvious criterion (sample where predictions differ most) picks the one
    place that settles nothing.

    Emitted per (system, metric, property), since a tie is a property of one
    system's fit and not of the corpus as a whole.
    """
    from core import design, model_fit

    out = []
    by_system = defaultdict(list)
    for r in rows:
        by_system[r.get("function_name", "?")].append(r)

    for system, srows in by_system.items():
        xs, ys, keep = [], [], []
        for r in srows:
            x, y = _f(r, prop), _f(r, metric)
            if x > 0 and y > 0 and math.isfinite(x) and math.isfinite(y):
                xs.append(x); ys.append(y); keep.append(r)
        if len(xs) < 8:
            continue
        try:
            best, fitted = model_fit.infer_complexity(xs, ys)
        except ValueError:
            continue
        tied = model_fit.near_ties(fitted)
        if not design.worth_deciding(fitted, tied):
            # Either the data already picked a winner, or the property does not
            # explain the metric and every class ties for want of a signal.
            continue
        # Without an explicit ceiling, look up to 3x past what has been
        # observed. Asking further is not obviously wrong, but an unsatisfiable
        # request costs a whole generation, and the frontier ledger is what
        # records that so it is not asked twice.
        ceiling = reach if reach is not None else max(xs) * 3
        plan = design.propose(xs, ys, tied, reach=ceiling,
                              eps=design.noise_floor(keep, metric),
                              cost_model=best.compute)
        if plan is None:
            continue
        # Seed from the inputs nearest the proposed region, so evolution starts
        # from something already close on this axis.
        mid = (plan["lo"] + plan["hi"]) / 2
        seeds = sorted(keep, key=lambda r: abs(_f(r, prop) - mid))[:6]
        box = (math.floor(plan["lo"]), math.ceil(plan["hi"]))
        out.append({
            "label": f"{system}_{metric}_{prop}_discriminate",
            "rows": seeds,
            "prop_box": {prop: box},
            "note": (f"{' vs '.join(plan['candidates'])} tied; "
                     f"{plan['n_points']} inputs here decide it "
                     f"(power {plan['power']:.2f})"),
        })
    return out


def _resolve(ledger, prop, observed_max):
    """Settle an outstanding beyond-request for `prop` against the corpus.

    The outcome of a request is only visible in the corpus that follows it, so
    it is judged here rather than at generation time: if the observed max moved
    past what we asked beyond, the request landed; if it did not, it came back
    empty and the property is pinned. Called both before proposing the next
    region and when reporting, so a run that ends on a miss still reports it.
    """
    entry = ledger.get(prop)
    if entry is None:
        return None
    if observed_max > entry.get("last_max", float("-inf")):
        # The lever worked. Reset the ladder: the next request is computed from
        # the corpus that just grew, so starting again at the first rung still
        # asks for more than this one did, and the climb stays geometric.
        entry.pop("pending", None)
        entry.update(pinned=False, misses=0, rung=0, reason=None)
        return entry
    if entry.pop("pending", False):
        entry["misses"] = entry.get("misses", 0) + 1
    # Deliberately NOT pinned here. Pinning on a miss would make one failed
    # request the end of the matter; whether there is another lever left to
    # pull is the ladder's judgement, and it pins when it runs out.
    return entry


def _grammar_digest(grammar_path):
    if grammar_path is None:
        return None
    try:
        return hashlib.sha1(
            pathlib.Path(grammar_path).read_bytes()).hexdigest()
    except OSError:
        return None


def _invalidate_on_grammar_change(ledger, grammar_path, sites=None,
                                  max_repetition=None):
    """Forget every pin when the grammar or the generation budget changes.

    A pin is a claim about what this grammar can express, so editing the grammar
    voids it. Without this the ledger deadlocks exactly where widening matters:
    raise a bound to unpin a property and the corpus max has not moved yet, so
    the request stays skipped and nothing can ever move it. Any edit clears the
    pins -- a comment change costs one probe per property, which is the cheap
    side of the trade.

    The digest covers the generation budget as well as the grammar text.
    Leaving it out has the same deadlock in it: raising `max_repetition` to
    unpin a property would leave every pin standing, since it does not appear
    in the .fan file, so the request that would prove the pin wrong would
    never be issued again.
    """
    digest = _grammar_digest(grammar_path)
    if digest is None:
        return
    digest = hashlib.sha1(
        f"{digest}|{max_repetition}|"
        f"{sorted((k, v.nt) for k, v in (sites or {}).items())}"
        .encode()).hexdigest()
    meta = ledger.setdefault("__grammar__", {})
    if meta.get("digest") == digest:
        return
    meta["digest"] = digest
    # For a ledger carrying pins but no digest, the grammar it was written
    # against is unknown. Unknown is treated as changed: a stale
    # pin is the harmful direction, since it silently withholds the request
    # that would prove it wrong.
    for prop, entry in ledger.items():
        if prop == "__grammar__" or not isinstance(entry, dict):
            continue
        entry.pop("pending", None)
        entry.pop("requested", None)
        entry["pinned"] = False
        entry["misses"] = 0
        entry["last_max"] = float("-inf")


def _frontier_path(corpus):
    return corpus.root / FRONTIER_FILE


def load_frontier(corpus):
    path = _frontier_path(corpus)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (ValueError, OSError):
        return {}


def save_frontier(corpus, ledger):
    _frontier_path(corpus).write_text(json.dumps(ledger, indent=2, sort_keys=True))


def explored_properties(corpus, properties=None):
    """Properties whose axis the loop has finished pushing.

    A property is settled once the frontier ledger has PINNED it (we escalated
    until nothing moved) or found it constant. Anything else has not been
    pushed to its limit yet, and a near-zero relevance score for one of those
    means "not yet looked", not "does not matter".

    That distinction matters because selection gates what the loop may spend
    requests on. A property can score near-zero relevance because it has no
    variation where it matters, which is exactly the data the loop has not
    collected. Dropping it for that would be circular.
    """
    ledger = load_frontier(corpus)
    names = list(properties) if properties is not None else sorted(ledger)
    out = set()
    for prop in names:
        e = ledger.get(prop)
        if isinstance(e, dict) and (e.get("pinned") or e.get("constant")):
            out.add(prop)
    return out


def frontier_report(corpus, properties=None):
    """Lines describing each property the loop could not push past.

    A pinned property means every input the grammar can express already sits at
    or below this value, so a null result on any axis that needs a larger one
    is a statement about the grammar rather than about the systems compared.
    """
    ledger = load_frontier(corpus)
    names = list(properties) if properties is not None else sorted(ledger)
    rows = list(corpus.rows.values())
    for prop in names:
        if prop in ledger and prop != "__grammar__" and rows:
            _resolve(ledger, prop, max(_f(r, prop) for r in rows))
    if ledger:
        save_frontier(corpus, ledger)
    lines = []
    for prop in names:
        e = ledger.get(prop)
        if not e or not e.get("pinned"):
            continue
        m = e.get("last_max")
        if e.get("constant"):
            lines.append(f"  {prop}: constant at {m:g} over the corpus; "
                         f"the grammar cannot vary it.")
        elif e.get("reason") == "language":
            # A property stopped by a bound written in the grammar is a fact
            # about the subject: every input the spec admits already sits at or
            # below it, so a null result on an axis needing more is a statement
            # about the language, not about the systems. One stopped by the
            # search is a statement about the search.
            lines.append(
                f"  {prop}: pinned at {m:g} by the LANGUAGE "
                f"({e.get('site')}{{..,{e.get('language_bound'):g}}}); "
                f"no input this grammar admits goes further.")
        elif e.get("reason") == "budget":
            # A third kind of stop, and as much a statement about this machine
            # as the language bound is about the subject: the next rung needed
            # more derivation nodes than the ceiling allows, so the request was
            # never made. Raising MAX_STRUCTURAL_NODES is what moves this one.
            band = e.get("band") or [None, None]
            lines.append(
                f"  {prop}: pinned at {m:g} by the NODE BUDGET; "
                f"{e.get('site')}{{{band[0]},{band[1]}}} would need "
                f"{e.get('needed_nodes'):,} nodes against a cap of "
                f"{e.get('node_cap'):,}.")
        else:
            rungs = e.get("rung", e.get("misses", 1))
            lines.append(
                f"  {prop}: pinned at {m:g} by the SEARCH; "
                f"{rungs} escalating request(s) returned nothing further.")
    return lines


def regions(corpus, metrics, properties,
            want=("divergence", "dominance", "compare", "joint",
                  "discriminate", "prop_beyond", "extreme", "prop_edge",
                  "sparse", "prop_sparse"),
            k_frac=0.15, n_bins=10, n_sparse=2, grammar_path=None,
            reach=None, sites=None, max_repetition=20,
            allow_beyond_language=False):
    # Rejected inputs are excluded here for the same reason write_summary
    # excludes them: they exit early and their cost is a different population,
    # so targeting them chases the error path's shape rather than the system's.
    # They stay in the corpus, so they are not regenerated.
    from core.corpus import accepted
    rows = [r for r in corpus.rows.values() if accepted(r)]
    if not rows:
        return []
    # Grouped by KIND, then interleaved, so the caller's request cap takes one
    # of each kind before a second of any. A flat cap over a kind-ordered list
    # does not: `discriminate` emits one region per (system, metric, property),
    # so it and `divergence` would consume the whole budget and `prop_beyond`
    # -- the kind that expands the frontier -- would never be reached.
    by_kind = {}

    def emit(kind, regions):
        if regions:
            by_kind.setdefault(kind, []).extend(regions)

    if "divergence" in want:
        for m in metrics:
            emit("divergence", _divergence(_measured(rows, m), m, k_frac))
    if "dominance" in want:
        emit("dominance", _dominance(rows, metrics, properties, sites))
    if "compare" in want:
        claimed = {r.get("bin") for r in by_kind.get("dominance", [])}
        # A bin already claimed for blocking a dominance verdict does not also
        # need a single-metric request: same inputs, weaker reason.
        emit("compare", [r for r in _compare(rows, metrics, properties, sites)
                         if r.get("bin") not in claimed])
    if "joint" in want:
        jl = load_joint(corpus)
        emit("joint", _joint(rows, properties, sites, ledger=jl))
        save_joint(corpus, jl)
    if "discriminate" in want:
        for m in metrics:
            for p in properties:
                emit("discriminate",
                     _discriminating(_measured(rows, m), m, p, reach=reach))
    if "prop_beyond" in want:
        ledger = load_frontier(corpus)
        _invalidate_on_grammar_change(ledger, grammar_path, sites, max_repetition)
        for p in properties:
            emit("prop_beyond",
                 _property_beyond(rows, p, ledger, sites=sites,
                                  max_repetition=max_repetition,
                                  allow_beyond_language=allow_beyond_language))
        save_frontier(corpus, ledger)
    if "extreme" in want:
        for m in metrics:
            emit("extreme", _extreme(_measured(rows, m), m, k_frac))
    if "prop_edge" in want:
        for p in properties:
            emit("prop_edge", _property_edge(rows, p, k_frac, sites=sites))
    if "sparse" in want:
        for m in metrics:
            emit("sparse", _sparse(_measured(rows, m), m, n_bins, n_sparse))
    if "prop_sparse" in want:
        for p in properties:
            emit("prop_sparse",
                 _property_sparse(rows, p, n_bins, n_sparse, sites=sites))

    # Round-robin over the kinds, in the priority order of `want`.
    order = [k for k in want if k in by_kind]

    # ...and round-robin over the PROPERTY AXIS within each kind, which the
    # kind-level interleave alone does not do. Every kind emits its regions in
    # `properties` order, so the outer loop below takes index 0 of each kind
    # and index 0 is the same property every time: one axis collects a region
    # of every kind while the others get none, and an axis the loop reports
    # undecided can sit behind the request cap and never be requested.
    #
    # Each kind also STARTS at a different axis, because leading every kind
    # with the same one just moves the problem: with k kinds and n axes the
    # first k requests then cover ceil(k/n) regions per axis instead of k of
    # one.
    def axis(reg):
        box = reg.get("prop_box") or {}
        if len(box) == 1:
            return next(iter(box))
        label = reg.get("label", "")
        for prop in sorted(properties, key=len, reverse=True):
            if label.startswith(prop + "_"):
                return prop
        return None                     # a metric-wide region, on no one axis

    for j, kind in enumerate(order):
        groups = {}
        for reg in by_kind[kind]:
            groups.setdefault(axis(reg), []).append(reg)
        keys = list(groups)
        if len(keys) > 1:
            cut = j % len(keys)
            keys = keys[cut:] + keys[:cut]
        merged = []
        for i in range(max(len(v) for v in groups.values())):
            for key in keys:
                if i < len(groups[key]):
                    merged.append(groups[key][i])
        by_kind[kind] = merged

    out = []
    for i in range(max(len(v) for v in by_kind.values()) if by_kind else 0):
        for kind in order:
            if i < len(by_kind[kind]):
                by_kind[kind][i]["kind"] = kind
                out.append(by_kind[kind][i])
    for reg in out:
        # property-axis regions carry an explicit prop_box; metric regions derive
        # one from the span of their rows. A structural region carries no box on
        # purpose -- the rewritten repetition is what puts the inputs where they
        # are asked for, and adding a clause back would reintroduce the search
        # that the rewrite replaces.
        if not reg.get("structural"):
            reg["prop_box"] = reg.get("prop_box") or _prop_box(reg["rows"], properties)
        reg["seeds"] = list({r["input_hash"] for r in reg.get("rows") or []})
        reg.pop("rows", None)
    # Drop degenerate regions: nothing to constrain, rewrite or optimise.
    return [r for r in out
            if r["prop_box"] or r.get("rewrite") or r.get("soft")]


def where_clauses(region):
    """Property-box -> `where` clause bodies (without the `where` keyword)."""
    clauses = []
    for prop, (lo, hi) in region["prop_box"].items():
        # A None bound is open on that side; `prop_beyond` uses it to ask for
        # "further than the corpus has been" without also pinning an upper end.
        if lo is not None:
            clauses.append(f"{prop}(<start>) >= {lo}")
        if hi is not None:
            clauses.append(f"{prop}(<start>) <= {hi}")
    return clauses
