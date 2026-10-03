"""Ablation: what does the loop buy, over what.

    python src/core/ablate.py jsonpath_plus_latest --runs 1 --budget 100

A single "unaided Fandango" baseline is a strawman. Asked for a thousand
inputs with default settings, Fandango returns a thousand short ones, which is
a finding about defaults and not about this method. So the baseline is a
LADDER, and each rung isolates one thing:

  fandango        defaults, N inputs. The floor. Says how bad out-of-the-box is.
  fandango_tuned  same, with max_repetition and max_nodes raised. What a
                  competent Fandango user gets. If the loop only beats the
                  untuned arm, what we have is a configuration note, not a
                  method.
  stratified      structural banding only, no targeted loop. Applies to
                  subjects that declare their own strata. If the targeted
                  iterations add nothing over this, that is a real negative
                  result about the loop.
  structural_rand structural rewrites at RANDOM bands, no feedback. Isolates
                  the structural realisation from the targeting.
  guided          the loop.

The pairs that matter are adjacent rungs, and two of them can go against us.
That is the point: `structural_rand` versus `guided` is a fair fight, and if it
ties, the targeting is not paying for itself.

SCORING is on the tool's deliverable, not a proxy. The headline is how many
regional comparison verdicts come back DECIDED rather than undecided -- what a
user actually gets -- alongside property coverage.

The trap this is built to avoid: an arm that shapes its own corpus also shapes
which regions exist, so it could "win" by moving the goalposts. Every arm is
scored on the SAME fixed region set, computed once over the union of all arms'
observed ranges, before any arm is scored.
"""
import argparse
import csv
import math
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[2]

ARMS = ("fandango", "fandango_tuned", "stratified", "structural_rand", "guided")

# What the tuned baseline gets: bounds high enough that the grammar, not the
# fuzzer's defaults, limits what unaided generation reaches.
TUNED_MAX_REPETITION = 2000
TUNED_MAX_NODES = 20000
# Inputs a bin needs before it counts as covered. Plain occupancy called a
# distribution with 86% of its mass in two bins "6/6 covered"; it cannot see
# clustering, and clustering is exactly what an unguided sampler does.
MIN_PER_BIN = 5


def _config(subject):
    from core.remeasure import _load_config
    return _load_config(subject)


def _fresh(cfg, out_dir, properties):
    """A corpus in its own directory, so arms never share accumulated state."""
    from core.corpus import CorpusStore
    store = CorpusStore(out_dir, cfg.metrics, properties)
    store.load()
    return store


def direct_fuzz(co, cfg, n, input_dir, maxrep=None, nodes=None):
    """Generate `n` inputs straight from the grammar, no genetic algorithm.

    A structural-only grammar has no constraints, so `evolve` has
    no fitness signal to optimise and the GA contributes nothing -- measured,
    it returns the same length distribution as this at three times the cost.
    For an unconstrained baseline `Grammar.fuzz` is the honest entry point, and
    using `evolve` instead would be handicapping the comparator with machinery
    its own author would not invoke here.
    """
    from fandango.api import parse

    with open(cfg.fan_filepath) as fh:
        grammar, _ = parse(fh, use_stdlib=False)
    if maxrep:
        grammar.set_max_repetition(int(maxrep))
    kw = {} if nodes is None else {"max_nodes": nodes}
    out = []
    for i in range(n):
        try:
            sol = grammar.fuzz(**kw)
        except Exception:
            continue
        text, eval_input = co.converter_fan_output(sol)
        if not text and cfg.input_type == "int_array":
            continue
        (input_dir / f"input_f{i}.txt").write_text(text + "\n", encoding="utf-8")
        out.append((f"f{i}", sol, eval_input))
    co._measure_inputs(out)
    return out


def _fuzzer(cfg, properties_map, corpus, budget, random_seed=None):
    from core.fuzzer import Coreografa
    co = Coreografa(cfg.functions, custom_properties=properties_map,
                    input_type=cfg.input_type,
                    population_size=cfg.population_size,
                    desired_solutions=budget,
                    max_generations=cfg.max_generations,
                    max_nodes=cfg.max_nodes,
                    udf_path=cfg.eval_dir / "user_def_functions.py",
                    use_metric_cache=cfg.use_metric_cache,
                    min_n=cfg.metric_min_n, max_n=cfg.metric_max_n,
                    primary_metric=cfg.primary_metric,
                    random_seed=random_seed)
    co.corpus = corpus
    return co


def run_arm(arm, cfg, out_dir, budget, seed, site=None):
    """Fill a fresh corpus with `budget` inputs under one arm's policy."""
    from core import grammar_props as gp, workflow as wf
    from core.grammar_emit import build_targeted_grammar

    props = wf._custom_properties(cfg.udf_module, cfg)
    corpus = _fresh(cfg, out_dir, list(props))
    # PAIRED on the run's seed, so every arm in a run sees the same stream of
    # Fandango randomness and the difference between two arms is the policy
    # rather than the draw.
    co = _fuzzer(cfg, props, corpus, budget, random_seed=seed)
    info = gp.analyze(cfg.fan_filepath)
    sites = {s.nt: s for s in info.sites}
    nt = site or (sorted(sites)[0] if sites else None)

    inputs_dir = out_dir / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    if arm == "fandango":
        direct_fuzz(co, cfg, budget, inputs_dir)
    elif arm == "fandango_tuned":
        # Tuned the way the probe showed actually works: a max_repetition high
        # enough to span the language, not the subject config's value. An
        # under-tuned baseline is the strawman this ladder exists to avoid.
        direct_fuzz(co, cfg, budget, inputs_dir,
                    maxrep=TUNED_MAX_REPETITION, nodes=TUNED_MAX_NODES)
    elif arm == "stratified" and cfg.stratify:
        co.desired_solutions = max(1, budget // _bands(cfg))
        co.fuzz_stratified(cfg.fan_filepath, input_dir=inputs_dir,
                           stratify=cfg.stratify, grammar_dir=out_dir,
                           sites=sites)
    elif arm == "structural_rand" and nt:
        # Same machinery as a targeted request, bands chosen at random rather
        # than from the corpus. This is the arm that tells us whether feedback
        # is doing anything the structure alone does not.
        import random
        from core.targeting import _node_budget
        rng = random.Random(seed)
        rounds = 6
        co.desired_solutions = max(1, budget // rounds)
        # Respect the bound written in the grammar. Drawing a band above it
        # would widen L(G): the arm would be generating inputs outside the
        # specification under test and would not be comparable to any arm that
        # stays inside it.
        ceiling = sites[nt].lang_max
        top = 400 if ceiling == float("inf") else max(4, ceiling)
        for i in range(rounds):
            lo = int(math.exp(rng.uniform(math.log(2), math.log(top))))
            hi = min(int(top), lo + max(2, lo // 5))
            if hi <= lo:
                lo, hi = max(1, int(top) - 2), int(top)
            variant = out_dir / f"rand_{i}.fan"
            variant.write_text(build_targeted_grammar(
                cfg.fan_filepath, cfg.eval_dir / "user_def_functions.py", [],
                rewrites=[(nt, lo, hi)], extra_source=gp.derived_source(info)))
            try:
                co.fuzz(str(variant), input_dir=inputs_dir, request_id=f"r{i}",
                        max_nodes=_node_budget(sites[nt], hi),
                        max_repetition=cfg.max_repetition)
            except Exception as e:
                print(f"    [{arm}] band {lo}-{hi} failed: {type(e).__name__}")
    elif arm == "guided":
        # The real loop, capped at the same number of measured inputs as every
        # other arm. Its own output goes to this arm's directory, so nothing is
        # shared between arms or runs.
        import copy
        from core.workflow import run_workflow
        sub = copy.copy(cfg)
        sub.name = f"ablate-guided"
        sub.max_corpus_inputs = budget
        sub.do_requests = True
        # Exploration gets about half the budget so the targeted loop has
        # something left to spend; otherwise the arm is "stratified" wearing a
        # different name and the cap stops it before a single request.
        bands = _bands(cfg) if cfg.stratify else 1
        sub.desired_solutions = max(1, budget // (2 * bands))
        sub.request_desired_solutions = max(1, budget // 8)
        run_workflow(sub, out_dir)
        corpus = _fresh(cfg, out_dir, list(props))
    corpus.save()
    return corpus


def _bands(cfg):
    specs = [cfg.stratify] if isinstance(cfg.stratify, dict) else list(cfg.stratify)
    n = 1
    for s in specs:
        n *= len(s["bands"])
    return n


# --- scoring -------------------------------------------------------------

def fixed_regions(corpora, prop, n_bins=6):
    """`compare.property_bins` over the UNION of every arm's observed range.

    Computed once, before any arm is scored. An arm that shapes its own corpus
    also shapes which bins exist, so scoring each on its own bins would let it
    win by moving the goalposts. Zero is included: an arm that only ever
    produced inputs at 0 still gets scored on the zero region.
    """
    from core import compare

    vals = []
    for c in corpora:
        for r in c.rows.values():
            v = compare._f(r, prop)
            if v is not None:
                vals.append(v)
    return compare.property_bins(vals, n_bins)


def score(corpus, metrics, prop, bins, keep=None):
    """Decided verdicts and coverage for one arm, over the fixed bins.

    `keep` restricts to a common number of inputs so arms are scored at equal
    budget even when one overshot: the loop's cap can only bind at an iteration
    boundary, so the guided arm reached 77 inputs against a budget of 60 and
    would otherwise have been compared from a stronger position than it was
    given.
    """
    from core import compare

    rows = list(corpus.rows.values())
    if keep is not None:
        rows = [r for r in rows if r["input_hash"] in keep]
    names = compare.systems(rows)
    prop_of = {}
    for r in rows:
        v = compare._f(r, prop)
        if v is not None:
            prop_of[r["input_hash"]] = v

    decided = total = occupied = well_covered = 0
    for i, (lo, hi) in enumerate(bins):
        top = i == len(bins) - 1
        sub = [r for r in rows
               if compare.in_region(prop_of.get(r["input_hash"]), lo, hi, top)]
        n_here = len({r["input_hash"] for r in sub})
        if n_here:
            occupied += 1
        if n_here >= MIN_PER_BIN:
            well_covered += 1
        for j, a in enumerate(names):
            for b in names[j + 1:]:
                for m in metrics:
                    total += 1
                    v = compare.compare_pair(compare.paired(sub, m), a, b, m)
                    if v and v["verdict"] in ("a_faster", "b_faster", "equivalent"):
                        decided += 1
    vals = [v for v in prop_of.values() if v > 0]
    return {"decided": decided, "questions": total,
            "occupied_bins": occupied, "covered_bins": well_covered,
            "bins": len(bins),
            "inputs": len({r["input_hash"] for r in rows}),
            "max_prop": max(vals) if vals else 0.0}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("subject")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--budget", type=int, default=200,
                    help="inputs each arm may measure (the expensive resource)")
    ap.add_argument("--property", default=None)
    ap.add_argument("--site", default=None)
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    cfg = _config(args.subject)
    from core import workflow as wf
    props = list(wf._custom_properties(cfg.udf_module, cfg))
    prop = args.property or ("length" if "length" in props else props[0])
    arms = [a.strip() for a in args.arms.split(",")]

    root = pathlib.Path(args.out or REPO / "output" / f"_ablate_{args.subject}")
    rows = []
    for run in range(1, args.runs + 1):
        corpora = {}
        for arm in arms:
            d = root / f"run{run}" / arm
            d.mkdir(parents=True, exist_ok=True)
            t = time.time()
            corpora[arm] = run_arm(arm, cfg, d, args.budget, seed=1000 * run,
                                   site=args.site)
            print(f"run {run} {arm:16s} "
                  f"{len({r['input_hash'] for r in corpora[arm].rows.values()}):4d} inputs "
                  f"{time.time()-t:6.0f}s", flush=True)
        bins = fixed_regions(corpora.values(), prop)
        # Equal budget for scoring: the smallest input count any arm achieved.
        common = min(len({r["input_hash"] for r in c.rows.values()})
                     for c in corpora.values())
        for arm, c in corpora.items():
            hashes = sorted({r["input_hash"] for r in c.rows.values()})
            s = score(c, cfg.metrics, prop, bins, keep=set(hashes[:common]))
            s["scored_at"] = common
            s.update(run=run, arm=arm, prop=prop)
            rows.append(s)
            print(f"   {arm:16s} decided {s['decided']:3d}/{s['questions']:3d}"
                  f"  covered {s['covered_bins']}/{s['bins']}"
                  f"  (occupied {s['occupied_bins']})"
                  f"  max {prop}={s['max_prop']:.4g}"
                  f"  @{common} inputs", flush=True)

    out = root / "ablation.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"\nrows written to {out}")


if __name__ == "__main__":
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(REPO / "src"))
    main()
