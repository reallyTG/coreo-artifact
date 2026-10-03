"""Generic Coreografa experiment pipeline.

Each eval's example.py builds a `WorkflowConfig` and calls `run_workflow`.
All artifacts are written under `output_dir` (passed in by run.py).
"""
import inspect
import math
import os
import sys
import time as _time

# Fandango walks derivation trees recursively (deepcopy, invalidate_hash), so a
# recursive grammar under a large node budget exceeds Python's default limit of
# 1000. fuzzer catches the RecursionError and drops the band or seed, so a run
# does not die, it quietly stops producing; uncaught, as in tree deepcopy on
# `json`, it ends the run. Every subject needs the higher limit, so it lives
# here.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 60000))
from dataclasses import dataclass, field
from pathlib import Path

from core.fuzzer import Coreografa
from core import feature_select
from analyzer import Analyzer


@dataclass
class WorkflowConfig:
    name: str                       # eval name, e.g. "json"
    fan_filepath: Path              # grammar (.fan) file
    udf_module: object              # imported user_def_functions module
    functions: list                 # target callables to profile
    eval_dir: Path                  # directory of the eval (for cwd-sensitive targets)
    input_type: str = "string"      # "string" or "int_array"
    metrics: list = field(default_factory=lambda: ["runtime_ns", "memory_peak"])
    population_size: int = 20
    desired_solutions: int = 20
    # Generation caps default to finite values (with best_effort) so a hard-to-
    # satisfy constraint can never hang an evolve indefinitely.
    max_generations: int = 100      # cap Fandango generations per initial evolve
    max_nodes: int = None           # cap on derivation-tree size (None=Fandango default 200)
    do_requests: bool = True        # run the targeted-regeneration loop after exploration
    # Adaptive stop: run targeted iterations until an iteration adds fewer than
    # `saturation_k` NEW unique inputs to the corpus, bounded by max_iterations.
    # The loop is FEEDBACK-driven -- iteration k+1 targets regions found in
    # k -- so many short iterations are worth more than few long ones: a single
    # 25-minute generation produces no feedback at all. The cap is rarely the
    # binding constraint; one runaway request eating the wall budget is, and
    # `max_generation_seconds` bounds that. Saturation stops earlier on most
    # subjects.
    max_iterations: int = 12
    saturation_k: int = 3
    # Which corpus regions each targeted iteration pushes toward. Metric-axis:
    # divergence / extreme / sparse. Property-axis (directly controllable):
    # prop_edge / prop_sparse / prop_beyond (extrapolate past the observed max).
    # `joint` names an unoccupied COMBINATION (an extensive property
    # structurally, an intensive one as an objective); every other kind names a
    # single property.
    targets: tuple = ("divergence", "dominance", "compare", "joint",
                      "discriminate", "prop_beyond", "extreme", "prop_edge",
                      "sparse", "prop_sparse")
    # Request/re-fuzz loop budget (the loop re-fuzzes once per request, so it
    # dominates runtime for grammars that produce large inputs).
    max_requests: int = 10          # cap requests processed
    request_population_size: int = None   # re-fuzz pop size (None = population_size)
    request_desired_solutions: int = 10   # re-fuzz solutions/request
    request_max_generations: int = 20      # re-fuzz generation cap
    # Measure kept inputs once-to-significance via the harness-owned
    # coreografa_metrics cache (samples persist across rounds/runs). Requires a
    # structural (SUT-free) grammar. summary.csv carries means; a stats sidecar
    # carries n/mean/CI.
    use_metric_cache: bool = False
    metric_min_n: int = 5
    metric_max_n: int = 30
    # Wall-clock backstop on ONE generation call, with `generation_stage`
    # generations between clock checks. Every other generation bound is on
    # work as DECLARED (repetition count, node budget, generation cap) and
    # none bounds work as EXPERIENCED: 200k nodes is milliseconds on a flat
    # list grammar and 25 minutes on selectors_js. Generous on purpose --
    # the size bounds are meant to bind first, so runs stay reproducible, and
    # this only fires on a grammar that surprises them. A request it cuts is
    # marked in the request log as not reproducible.
    # Largest corpus input handed to Fandango as a seed. A seed must be PARSED
    # against the grammar, and on an ambiguous recursive grammar that parse is
    # savagely superlinear -- selectors_js parses 526B in 0.08s and does not
    # finish 5376B in 120s. This is a size bound, so it is deterministic and
    # costs no reproducibility, unlike the wall-clock backstop below.
    max_seed_bytes: int = 4096
    max_generation_seconds: int = 300
    generation_stage: int = 5
    # Base seed for Fandango's RNG. None leaves generation unseeded. Set it
    # for an evaluation run: the ablation needs its arms paired on the same
    # randomness to be a fair fight, and an artifact that cannot reproduce its
    # own table is not one.
    random_seed: int = None
    # The metric the measurement stopping rule watches. Must be one the SUTs
    # actually report: a runner emitting its own metric names rather than the
    # framework's has to name one of those here.
    primary_metric: str = "runtime_ns"
    # Range-stratified exploration: structurally band a grammar repetition so the
    # initial sample is guaranteed to span the property axis (don't rely on GA
    # diversity). e.g. {"nt": "<more_member>", "bands": [(0,5),(5,15),(15,30),(30,50)]}
    # A list of such specs bands several axes at once, generating from every
    # combination of their bands; the run count is the product, so keep the
    # bands per axis few.
    stratify: "dict | list" = None
    # The joint model fit costs 6 ** len(features), so the properties entering
    # it are screened and de-duplicated first (see core/feature_select). One
    # set is chosen per subject, pooled over metrics and systems, so every
    # system is modelled on the same properties. Single-feature plots and fits
    # still cover every property.
    # Six, not four: the correlation filter is what should be removing
    # properties. The cap only exists to stop the cost cliff: six is about 16
    # seconds of fitting, seven about 95.
    max_joint_features: int = 6
    feature_corr_threshold: float = 0.8
    feature_relevance_floor: float = 0.05
    # Grammar-derived properties: one `count_<X>` per non-terminal whose count
    # can vary, with the repetition that governs it (see core/grammar_props).
    # A subject's user_def_functions keeps only what derivation cannot express
    # -- ratios, and `depth` -- and may declare
    # ALIASES = {"num_pairs": "count_more_member"} to keep its own column
    # name for a count the grammar also derives.
    derive_properties: bool = True
    # Fandango's `max_repetition` grammar setting: what actually bounds `*` and
    # `+` during generation. It defaults to 20 inside Fandango, so left unset
    # every free repetition is capped at 20 unless a request pushes the search
    # past it. An explicit `{lo,hi}` in the grammar overrides it, which is what
    # a structural request emits.
    max_repetition: int = 200
    # Whether a request may widen a repetition past the bound written in the
    # grammar. A bound like `<x>{0,40}` is part of the language under test, so
    # going past it changes L(G) and any claim resting on those inputs is about
    # a different specification. Off by default: the frontier report says the
    # language is the limit instead. Turn on deliberately, and read the result
    # as being about the widened spec.
    widen_beyond_language: bool = False
    # Fitness an individual must reach before Fandango emits it, for requests
    # carrying a soft objective. 1.0 (Fandango's default) means the running
    # extreme, which is common for a coarse integer property and rare for a
    # near-continuous one. This is a safety valve rather than a tuning knob.
    soft_expected_fitness: float = 0.9
    # Generations a request carrying an objective is allowed, and it gets all of
    # them: such a request asks for more solutions than the run can produce, so
    # only this cap ends it, and the best `request_desired_solutions` are kept.
    # An objective keeps improving with more generations at roughly linear
    # cost, so this trades directly against iteration time and 150 is a
    # compromise, not an optimum.
    soft_max_generations: int = 150
    # Properties the TARGETING loop is allowed to spend requests on, chosen by
    # the same relevance-then-correlation pass as the joint fit but capped
    # tighter. Derivation makes this mandatory rather than optional: json
    # derives 13 counts, most of them rising together with document size, and
    # `prop_beyond`/`prop_edge`/`prop_sparse` fire once per property, so an
    # unselected list spends the whole request budget re-asking for one axis
    # under several names.
    max_loop_features: int = 4
    # Properties the subject DECLARES the loop should target, overriding the
    # selection above. For a question asked in advance -- "does this commit
    # change cost along array width?" -- the axis is part of the question, and
    # selection cannot find it on its own when the difference only shows as a
    # failure: a crash is no measurement, so nothing correlates with it.
    # None (the default) leaves selection in charge.
    loop_properties: tuple = None
    # Hard cap on distinct inputs the corpus may reach, or None for no cap.
    # Exists for budget-controlled comparison: an ablation arm is only
    # interpretable against another if both were allowed the same number of
    # measured inputs, which is the expensive resource.
    max_corpus_inputs: int = None
    # Wall-clock budget for the whole run, or None: a stopping condition beside
    # the iteration budget. It matters that this is INTERNAL: an external
    # timeout kills the process, losing the end-of-run reports and whatever
    # stdout was still buffered, where this stops between units of work, saves
    # the corpus and still prints the frontier and comparison reports.
    max_wall_seconds: int = None
    # Automatic stratification. Used when `stratify` is not set: axes come
    # from the grammar's repetition sites, one per site, banded log-spaced
    # with an explicit zero band, and allocated MARGINALLY (axes x bands, not
    # their product).
    auto_stratify: bool = True
    stratify_bands: int = 5
    # Inputs per stratum, and the invariant of the whole scheme. One proves a
    # region is reachable and seeds the loop there; three survives a rejection
    # (a subject can refuse some of its own inputs) and a degenerate draw.
    stratum_inputs: int = 3
    max_stratify_axes: int = None
    # Ceiling for auto-stratified bands, separate from max_repetition (which
    # bounds FREE repetitions during generation). Exploration spreads each
    # property across a wide range by construction; tying the top band to
    # max_repetition would mean subjects that lower it for distribution reasons
    # (JSONPath, SQL: 10) explore nothing past 10. None bands up to
    # max_repetition.
    stratify_max_repetition: int = None
    # Whether to regenerate a stratum the corpus already covers. Coverage per
    # stratum is the invariant, and a stratum covered is covered however it got
    # that way, so the default is to skip it and spend the wall clock on
    # requests instead. Set True to re-explore regardless -- which is what a
    # grammar edit wants, since coverage recorded against the old language says
    # nothing about the new one.
    explore_when_covered: bool = False


def stratify_bands(stratify):
    specs = [stratify] if isinstance(stratify, dict) else list(stratify)
    return " x ".join(f"{s['nt']} bands={s['bands']}" for s in specs)


def _delete_files(directory: Path):
    for f in directory.iterdir():
        if f.is_file():
            try:
                f.unlink()
            except Exception as e:
                print(f"Error deleting {f}: {e}")


def _declared_properties(udf_module):
    """Map property name -> callable, from user_def_functions.

    If the module declares a `PROPERTIES` list, only those names are used as
    input features (the rest are treated as helpers). Otherwise every function
    defined in the module is used.
    """
    defined = {
        name: fn
        for name, fn in inspect.getmembers(udf_module, inspect.isfunction)
        if fn.__module__ == udf_module.__name__
    }
    declared = getattr(udf_module, "PROPERTIES", None)
    if declared is not None:
        return {name: defined[name] for name in declared}
    return defined


def _custom_properties(udf_module, config=None):
    """Every input property: grammar-derived counts plus declared ones.

    A declared property wins a name clash, and a name listed in the module's
    `ALIASES` ({declared: derived non-terminal property, or a tuple of them})
    suppresses the derived duplicate so the subject keeps its own column. That matters for
    more than tidiness: a corpus column is keyed by name, so emitting
    `count_more_member` beside an existing `num_pairs` would leave every
    accumulated row reading 0 on the new column and fit the models on it.
    """
    declared = _declared_properties(udf_module)
    if config is None or not getattr(config, "derive_properties", False):
        return declared
    from core import grammar_props

    info = grammar_props.analyze(config.fan_filepath)
    derived = grammar_props.derived_properties(info)
    # A value may be one derived name or several. Several is the common case
    # once a list is spelled `<x> <more_x>*`: that derives both `count_x` and
    # `count_more_x`, which differ by exactly one and are the same axis, so a
    # declared property standing in for the pair has to suppress both.
    #
    # Write several as a LIST. The subject's property module is inlined
    # verbatim into every generated target grammar, and Fandango's .fan parser
    # rejects a single-element tuple -- `("count_x",)` is a syntax error there,
    # and the whole grammar then fails to parse rather than that one line.
    for derived_names in getattr(udf_module, "ALIASES", {}).values():
        if isinstance(derived_names, str):
            derived_names = (derived_names,)
        for derived_name in derived_names:
            derived.pop(derived_name, None)
    derived.update(declared)            # declared wins a clash
    return derived


def _property_generators(udf_module):
    """{property name -> fn(text, lo, hi, rng) -> text | None}, from the subject.

    An optional hook for custom properties. It exists because some properties
    cannot be reached by search OR by structure: an intensive property such as
    a ratio has no governing repetition, a hard clause on it gives the GA no
    gradient, and a soft objective plateaus. A direct transformation of an
    existing input reaches the target at once.

    The contract is a TRANSFORM, not a constructor: given an existing input and
    a target range, return an input like it but with the property in range. That
    is what makes it usable -- an intensive property is a ratio over the rest of
    the input, so constructing one from nothing means inventing everything else
    too, while transforming a corpus input preserves its length, alphabet and
    shape and moves only the property asked for.

    A generator cannot widen the language: what it returns is parsed against the
    grammar and dropped if it does not fit. So it is a search aid, an initial
    population that is likely to get the search there, not a way to smuggle in
    inputs the spec forbids.
    """
    return dict(getattr(udf_module, "GENERATORS", {}) or {})


def _region_properties(reg):
    """Property names a region is trying to move."""
    names = set(reg.get("prop_box") or {})
    if reg.get("objective"):
        names.add(reg["objective"][0])
    return names


def _band_props(config, nts):
    """{banded non-terminal -> the corpus column that counts it}.

    `count_<nt>` is the derived name, and the subject may have aliased it to a
    column of its own; that alias is the column the corpus actually carries, so
    resolving it is what lets a band be checked against the corpus at all.
    """
    from core import grammar_props as _gp

    alias_of = {}
    for declared, derived in getattr(config.udf_module, "ALIASES", {}).items():
        for name in ([derived] if isinstance(derived, str) else derived):
            alias_of[name] = declared
    out = {}
    for nt in nts:
        cand = _gp.property_name(nt)
        out[nt] = alias_of.get(cand, cand)
    return out


def _property_sites(udf_module, config):
    """property name -> the repetition that governs it, or None.

    Resolves through ALIASES, so a subject keeping `num_pairs` as its column
    name still gets `<more_member>` as the site to widen for it. An alias naming
    several derived properties takes the site of the first one that HAS a
    governing repetition -- they are the same axis, so any of their sites
    widens it. Usually only one does: for a list spelled `<x> <more_x>*` the
    repetition is `<more_x>`, and `count_x` has no site of its own.
    """
    if not getattr(config, "derive_properties", False):
        return {}
    from core import grammar_props

    info = grammar_props.analyze(config.fan_filepath)
    sites = {}
    for nt in info.counts:
        site = info.governing_site(nt)
        if site is not None:
            sites[grammar_props.property_name(nt)] = site
    for declared_name, derived_names in getattr(udf_module, "ALIASES", {}).items():
        if isinstance(derived_names, str):
            derived_names = [derived_names]
        for derived_name in derived_names:
            if derived_name in sites:
                sites[declared_name] = sites[derived_name]
                break
    return sites


def run_workflow(config: WorkflowConfig, output_dir: Path):
    import time as _time
    started = _time.time()
    deadline = (started + config.max_wall_seconds
                if config.max_wall_seconds else None)
    output_dir = Path(output_dir)

    # The .fan grammars embed imports relative to the eval dir (e.g. `import
    # user_systems`), and some SUTs reference relative resources. Make the eval
    # dir importable and run from it. All output paths below are absolute, so
    # chdir is safe.
    eval_dir = str(config.eval_dir)
    if eval_dir not in sys.path:
        sys.path.insert(0, eval_dir)
    output_dir = output_dir.resolve()
    os.chdir(eval_dir)
    summary_file = output_dir / "summary.csv"
    split_dir = output_dir / "split"
    request_dir = output_dir / "requests"
    input_dir = output_dir / "inputs"
    grammar_dir = output_dir / "grammars"
    figure_dir = output_dir / "plots"
    individual_dir = output_dir / "individual"

    for d in [split_dir, request_dir, input_dir, grammar_dir, figure_dir, individual_dir]:
        d.mkdir(parents=True, exist_ok=True)
        _delete_files(d)

    custom_properties = _custom_properties(config.udf_module, config)
    feature_names = list(custom_properties.keys())
    if config.derive_properties:
        from core import grammar_props
        for line in grammar_props.describe(grammar_props.analyze(config.fan_filepath)):
            print(line)
    print(f"[{config.name}] properties: {feature_names}")

    udf_path = config.eval_dir / "user_def_functions.py"

    coreografa = Coreografa(
        config.functions,
        custom_properties=custom_properties,
        input_type=config.input_type,
        population_size=config.population_size,
        desired_solutions=config.desired_solutions,
        max_generations=config.max_generations,
        max_nodes=config.max_nodes,
        udf_path=udf_path,
        use_metric_cache=config.use_metric_cache,
        min_n=config.metric_min_n,
        max_n=config.metric_max_n,
        primary_metric=config.primary_metric,
        random_seed=config.random_seed,
        generation_budget_s=config.max_generation_seconds,
        generation_stage=config.generation_stage,
    )
    analyzer = Analyzer()

    # Persistent stores (NOT wiped across runs): metric cache + corpus.
    cache_path = output_dir / "metrics_cache.json"
    stats_sidecar = output_dir / "summary_stats.csv"
    if config.use_metric_cache:
        import core.coreografa_metrics as cm
        cm.load(str(cache_path))

    from core.corpus import CorpusStore
    from core import plots as coreo_plots
    corpus = CorpusStore(output_dir, config.metrics, feature_names)
    corpus.load()
    coreografa.corpus = corpus

    report_path = output_dir / "report.md"
    final_lines = []

    def write_report(extra=None):
        """Durable progress report, rewritten at every iteration boundary.

        Without it, everything the loop learns goes to stdout and only at the
        end, so a run cut short -- by a wall budget, a kill, a crash -- leaves
        its corpus on disk and nothing that says what is in it. This is cheap
        (corpus counts and property ranges, no fitting) so it can be rewritten
        every iteration, and the end-of-run analysis is appended to the same
        file when it exists.
        """
        rows = list(corpus.rows.values())
        inputs = {h for _, h in corpus.rows}
        out = [f"# {config.name}", "",
               f"- corpus: {len(rows)} rows, {len(inputs)} inputs, "
               f"{len(config.functions)} systems",
               f"- elapsed: {_time.time() - started:.0f}s"
               + (f" of {config.max_wall_seconds}s budget"
                  if config.max_wall_seconds else ""),
               "", "## property coverage", "",
               "| property | min | max | distinct |", "|---|---|---|---|"]
        for prop in feature_names:
            vals = []
            for r in rows:
                try:
                    v = float(r.get(prop, ""))
                except (TypeError, ValueError):
                    continue
                if v == v:
                    vals.append(v)
            if vals:
                out.append(f"| {prop} | {min(vals):g} | {max(vals):g} "
                           f"| {len(set(vals))} |")
        if extra:
            out += ["", *extra]
        report_path.write_text("\n".join(out) + "\n")

    def checkpoint():
        # Persist the two accumulating stores: corpus rows and measurement
        # samples. Called at every iteration boundary and periodically during
        # measurement itself, so an interrupted run keeps the SUT executions it
        # has already paid for.
        corpus.save()
        if config.use_metric_cache:
            cm.save(str(cache_path))
        # Also refresh the report here, not only at iteration boundaries.
        # Exploration is the longest single phase on most subjects, and a run
        # cut short during it would otherwise leave a corpus on disk with
        # nothing saying what is in it. This fires every `checkpoint_every`
        # inputs.
        try:
            write_report(final_lines)
        except Exception:
            pass          # a report must never be the thing that fails a run

    coreografa.checkpoint = checkpoint
    coreografa.deadline = deadline

    def write_views():
        # corpus.csv is the source of truth; derive the analyzer/plots views.
        corpus.write_summary(summary_file)
        corpus.write_stats(stats_sidecar)
        checkpoint()
        write_report(final_lines)

    def loop_features():
        """The properties this iteration's requests may target.

        Grammar-derived properties make correlation analysis between
        properties mandatory: the derived counts of one subject nearly all
        rise together (json derives 13), and every property-axis region kind
        fires once per property, so an unselected list spends the request
        budget asking for the same axis under several names before reaching a
        second one.

        Re-run every iteration rather than fixed after exploration, because
        relevance is estimated from the corpus and the corpus is what the loop
        is growing: a property that tracks nothing over 40 exploration rows can
        become the one that separates two systems over 400.
        """
        if config.loop_properties:
            unknown = [p for p in config.loop_properties if p not in feature_names]
            if unknown:
                raise ValueError(f"loop_properties names unknown properties: "
                                 f"{', '.join(unknown)}")
            return list(config.loop_properties), [
                f"[select] loop targets declared by the subject: "
                f"{', '.join(config.loop_properties)}"]
        import core.targeting as _t
        settled = _t.explored_properties(corpus, feature_names)
        selected, why = feature_select.select(
            str(summary_file), config.metrics, feature_names,
            max_features=config.max_loop_features,
            corr_threshold=config.feature_corr_threshold,
            relevance_floor=config.feature_relevance_floor,
            protect=[p for p in feature_names if p not in settled])
        return selected or feature_names[:config.max_loop_features], why

    def plot_all():
        # Split the summary on function_name so every fit is per system.
        # Without this the analyzer sees one pooled group and infers a single
        # complexity class over all systems at once, which is not a statement
        # about any of them.
        analyzer.read_csvs([str(summary_file)], metrics=config.metrics,
                           categoricals=["function_name"],
                           input_features=feature_names, ignore=["memory_after"],
                           input_dir=str(input_dir))
        coreo_plots.plot_all_systems(
            str(summary_file), config.metrics, feature_names, str(figure_dir),
            stats_csv=str(stats_sidecar))
        joint_features, why = feature_select.select(
            str(summary_file), config.metrics, list(analyzer.features),
            max_features=config.max_joint_features,
            corr_threshold=config.feature_corr_threshold,
            relevance_floor=config.feature_relevance_floor)
        for line in why:
            print(line)

        for metric in analyzer.metrics:
            for prop in analyzer.features:
                analyzer.plot_metric_vs_feature(metric, prop, output_dir=str(figure_dir))
                analyzer.fit_model_for_metric_and_feature(metric, prop, output_dir=str(figure_dir))
            if len(joint_features) >= 2:
                analyzer.fit_model_for_metric_and_features(
                    metric, features=joint_features, interaction=False,
                    output_dir=str(figure_dir))

    # --- Exploration (iteration 0): broad, range-stratified, SUT-free ---
    coreografa.iteration = 0
    base_size = corpus.size()  # rows already present (prior runs)
    # Keyed by non-terminal, for the band node budgets; `_property_sites` keys
    # by property, which is the wrong key here.
    band_sites = {}
    if config.derive_properties:
        from core import grammar_props as _gp
        band_sites = {s.nt: s for s in _gp.analyze(config.fan_filepath).sites}
    if config.stratify:
        print(f"[{config.name}] range-stratified exploration: "
              f"{stratify_bands(config.stratify)}")
        _specs = ([config.stratify] if isinstance(config.stratify, dict)
                  else list(config.stratify))
        band_props = _band_props(config, [sp["nt"] for sp in _specs])
        coreografa.fuzz_stratified(config.fan_filepath, input_dir=input_dir,
                                   stratify=config.stratify, grammar_dir=grammar_dir,
                                   sites=band_sites, corpus=corpus,
                                   per_stratum=(0 if config.explore_when_covered
                                                else config.stratum_inputs),
                                   band_props=band_props)
    elif config.auto_stratify and band_sites:
        from core import grammar_props as _gp
        axes = _gp.stratify_axes(_gp.analyze(config.fan_filepath),
                                 n_bands=config.stratify_bands,
                                 max_repetition=(config.stratify_max_repetition
                                                 or config.max_repetition),
                                 max_axes=config.max_stratify_axes)
        if axes:
            print(f"[{config.name}] auto-stratified exploration: "
                  + " x ".join(f"{a['nt']}{a['bands']}" for a in axes[:3])
                  + (" ..." if len(axes) > 3 else ""))
            coreografa.fuzz_marginal(
                config.fan_filepath, input_dir=input_dir, axes=axes,
                grammar_dir=grammar_dir, sites=band_sites,
                per_stratum=(0 if config.explore_when_covered
                             else config.stratum_inputs),
                max_repetition=config.max_repetition, corpus=corpus,
                band_props=_band_props(config, [a["nt"] for a in axes]))
        else:
            coreografa.fuzz(config.fan_filepath, input_dir=input_dir,
                            max_repetition=config.max_repetition)
    else:
        # No repetition to band at all: explore through the plain grammar, where
        # free repetitions are subject to `max_repetition` and nothing else.
        coreografa.fuzz(config.fan_filepath, input_dir=input_dir,
                        max_repetition=config.max_repetition)
    write_views()
    print(f"[{config.name}] iter 0 (explore): corpus={corpus.size()} "
          f"(+{corpus.size() - base_size} new this run)")
    # The cap has to bind here too, not only at iteration boundaries.
    # Exploration alone can exceed it -- four stratify bands at 20 solutions is
    # 80 inputs against a budget of 60 -- and a loop that overshoots before its
    # first request makes any budget-controlled comparison meaningless.
    over_budget = (config.max_corpus_inputs is not None
                   and len({h for _, h in corpus.rows}) >= config.max_corpus_inputs)
    if over_budget:
        print(f"[{config.name}] input budget reached during exploration; "
              f"skipping the targeted loop.")

    # --- Adaptive targeted-regeneration loop (stop on saturation) ---
    if config.do_requests and not over_budget:
        prop_sites = _property_sites(config.udf_module, config)
        previous = None
        for iteration in range(1, config.max_iterations + 1):
            if deadline and _time.time() > deadline:
                print(f"[{config.name}] wall-clock budget "
                      f"({config.max_wall_seconds}s) reached before iteration "
                      f"{iteration}; stopping with the corpus intact.")
                break
            coreografa.iteration = iteration
            before = corpus.size()
            targets, why = loop_features()
            if targets != previous:
                for line in why:
                    print(line)
                print(f"[{config.name}] loop targets {len(targets)} of "
                      f"{len(feature_names)} properties: {', '.join(targets)}")
                previous = targets
            undecided_kinds = _request_loop(
                config, coreografa, corpus, udf_path,
                input_dir, grammar_dir, targets, prop_sites, deadline=deadline)
            write_views()  # refresh source-of-truth views from the grown corpus
            added = corpus.size() - before  # genuinely new (function,input) rows
            print(f"[{config.name}] iter {iteration}: corpus={corpus.size()} "
                  f"(+{added} new)")
            if config.max_corpus_inputs is not None:
                distinct = len({h for _, h in corpus.rows})
                if distinct >= config.max_corpus_inputs:
                    print(f"[{config.name}] input budget reached "
                          f"({distinct}/{config.max_corpus_inputs}); stopping.")
                    break
            # The confidence-based stop. Three region kinds exist precisely
            # because something is not yet known: `discriminate`
            # (the data does not pick a complexity class), `compare` (a regional
            # verdict's interval spans the equivalence band) and `dominance` (a
            # verdict is blocked by an undecided metric). When an iteration
            # proposes none of them, there is nothing further the loop could
            # settle, and more inputs would only be more of what it already
            # knows. Saturation stays as the fallback for the case where it
            # cannot get the inputs it asks for.
            # Only when the loop is asking those questions at all. A run whose
            # `targets` excludes all three (a frontier-only run that pushes one
            # declared axis) never proposes them, so the stop would fire after
            # the first iteration with the frontier still moving.
            asks = set(config.targets) & {"discriminate", "compare", "dominance"}
            if asks and not undecided_kinds:
                print(f"[{config.name}] nothing left to decide (no model ties, "
                      f"no undecided comparisons, no blocked dominance); "
                      f"stopping after {iteration} targeted iteration(s).")
                break
            if added < config.saturation_k:
                print(f"[{config.name}] saturated (<{config.saturation_k} new inputs); "
                      f"still open: {', '.join(sorted(undecided_kinds))}; "
                      f"stopping after {iteration} targeted iteration(s).")
                break

    # Properties the loop could not push past. A pinned property means every
    # input this grammar can express already sits at or below that value, so a
    # null result on an axis needing a larger one says the grammar was the
    # limit, not that the systems agree. Nothing else in the output says that.
    from core import compare as _cmp
    for line in _cmp.rejection_report(corpus, feature_names):
        print(line)
        final_lines.append(line)

    import core.targeting as targeting
    pinned = targeting.frontier_report(corpus, feature_names)
    if pinned:
        head = f"[{config.name}] grammar frontier (targeting stopped asking here):"
        print(head)
        final_lines.append("## frontier")
        final_lines.append(head)
        for line in pinned:
            print(line)
            final_lines.append(line)

    # Which system is better, where, and with what confidence. The loop finds
    # where systems diverge; this says whether a difference is real.
    from core import compare as coreo_compare
    # The SELECTED properties, not every one: the derived counts nearly all rise
    # together, so reporting regions over the raw list repeats one finding under
    # several names and marks all of them confounded with each other.
    compare_props, _ = loop_features()
    final_lines.append("## comparison")
    for line in coreo_compare.report(
            [r for r in corpus.rows.values()], config.metrics, compare_props):
        print(line)
        final_lines.append(line)

    # Whether a one-dimensional region says what it appears to. This is the
    # decision point for joint exploration; it is an analysis over the corpus
    # that exists, so it costs no generation and no SUT time.
    if len(compare_props) >= 2:
        from core import interference as _intf
        for line in _intf.report(list(corpus.rows.values()),
                                 config.metrics[:1], compare_props):
            print(line)
            final_lines.append(line)

    # The model fits and plots are the expensive tail: the fit search is
    # `len(complexity_classes) ** len(features)` models per system, which is
    # 46,656 at six properties. They are also the only part of this stage that
    # is not needed to say what the run found -- the reports above are already
    # in `final_lines`.
    #
    # So when the budget is gone, drop them and keep the report. Overrunning
    # here is what turns a graceful stop into a kill: an outer runner allows
    # only a margin past the subject's own ceiling, and a fit search that
    # outlasts it loses the whole end-of-run output, including the reports
    # already computed.
    if deadline is not None and _time.time() > deadline:
        print(f"[{config.name}] past the wall-clock budget; skipping the model "
              f"fits and plots and writing the report. They are a function of "
              f"corpus.csv, which is checkpointed, so the next run recomputes "
              f"them from the same inputs rather than re-measuring.")
    else:
        plot_all()  # final models/plots from the full accumulated corpus

    if config.use_metric_cache:
        cm.save(str(cache_path))
        print(f"[{config.name}] metric cache: {len(cm._CACHE)} entries, "
              f"{cm.exec_count()} SUT executions this run")

    # size() counts (system, input) rows, not inputs, so both are printed.
    print(f"[{config.name}] wall clock: {_time.time() - started:.0f}s"
          + (f" of {config.max_wall_seconds}s budget"
             if config.max_wall_seconds else ""))
    write_report(final_lines)
    print(f"[{config.name}] report -> {report_path}")
    print(f"[{config.name}] done. corpus={corpus.size()} rows "
          f"({len({h for _, h in corpus.rows})} inputs x {len(config.functions)} systems). "
          f"Artifacts in {output_dir}")


def _request_loop(config, coreografa, corpus, udf_path, input_dir, grammar_dir,
                  feature_names, prop_sites=None, deadline=None):
    """Corpus-aware targeted regeneration (the constraint split in practice).

    Pick regions from the corpus (extreme / sparse / divergence), turn each into
    structural `where` clauses + seeds-from-corpus, build a targeted grammar, and
    re-fuzz. Measured inputs are upserted into the corpus by _measure_inputs.
    """
    import core.targeting as targeting
    from core.grammar_emit import build_targeted_grammar

    # Definitions for the grammar-derived properties, so a clause naming one
    # resolves inside the emitted .fan.
    derived_src = ""
    if config.derive_properties:
        from core import grammar_props
        derived_src = grammar_props.derived_source(
            grammar_props.analyze(config.fan_filepath))

    regs = targeting.regions(corpus, config.metrics, feature_names,
                             want=config.targets,
                             grammar_path=config.fan_filepath,
                             sites=prop_sites or {},
                             max_repetition=config.max_repetition,
                             allow_beyond_language=config.widen_beyond_language)
    if not regs:
        print(f"[{config.name}] no target regions (corpus too small).")
        return set()
    # Which of the "we do not know yet" kinds fired. Returned so the caller can
    # stop on confidence rather than only on saturation.
    open_kinds = {r.get("kind") for r in regs
                  if r.get("kind") in ("discriminate", "compare", "dominance")}
    if config.max_requests is not None:
        regs = regs[:config.max_requests]
    print(f"[{config.name}] targeting {len(regs)} regions: "
          f"{', '.join(r['label'] for r in regs)}")

    # Smaller budget per targeted re-fuzz.
    if config.request_population_size is not None:
        coreografa.population_size = config.request_population_size
    if config.request_desired_solutions is not None:
        coreografa.desired_solutions = config.request_desired_solutions
    if config.request_max_generations is not None:
        coreografa.max_generations = config.request_max_generations

    seed_cap = coreografa.desired_solutions

    def _usable_seeds(hashes):
        """Corpus inputs small enough to be worth parsing.

        Fandango must PARSE a string seed against the grammar to build its
        derivation tree, and on an ambiguous recursive grammar that parse is
        savagely superlinear. Measured on selectors_js: 526 bytes parses in
        0.08s and 5376 bytes does not finish in 120s -- ten times the size for
        more than fifteen hundred times the time.

        That can hang a selectors_js run for 25 minutes past its wall budget,
        and no generation budget can catch it: the parse happens before the
        first generation completes, so a clock checked between generations is
        never reached.

        Dropping an oversized seed costs that seed. Keeping it costs the
        iteration, and often the run.
        """
        out, skipped = [], 0
        for h in hashes:
            text = corpus.read_input(h)
            if not text:
                continue
            if config.max_seed_bytes and len(text) > config.max_seed_bytes:
                skipped += 1
                continue
            out.append(text)
        if skipped:
            print(f"  [seeds] skipped {skipped} seed(s) over "
                  f"{config.max_seed_bytes}B; parsing one costs more than the "
                  f"request it would seed")
        return out
    generators = _property_generators(config.udf_module)
    import random as _random
    rng = _random.Random(0)
    for i, reg in enumerate(regs):
        # Between regions, not only inside measurement. The deadline is also
        # checked in `_measure_inputs` and at iteration boundaries, but with
        # only those a region that breaks out on time is followed by the NEXT
        # of ten regions generating from scratch, and the run is killed at the
        # outer ceiling instead of stopping cleanly, losing its end-of-run
        # analysis.
        if deadline is not None and _time.time() > deadline:
            print(f"  [budget] wall-clock reached; skipping the remaining "
                  f"{len(regs) - i} request(s) this iteration.")
            break
        started_region = _time.time()
        before_hashes = {h for _, h in corpus.rows}
        clauses = targeting.where_clauses(reg)
        variant = grammar_dir / f"{config.name}_target_{i}_{reg['label']}.fan"
        variant.write_text(build_targeted_grammar(
            config.fan_filepath, udf_path, clauses,
            rewrites=reg.get("rewrite"), soft_clauses=reg.get("soft"),
            extra_source=derived_src))
        if reg.get("note"):
            print(f"  [{reg['label']}] {reg['note']}")
        budget = dict(max_nodes=reg.get("max_nodes"),
                      max_repetition=reg.get("max_repetition",
                                             config.max_repetition),
                      expected_fitness=(config.soft_expected_fitness
                                        if reg.get("soft") else None),
                      objective=reg.get("objective"),
                      soft_max_generations=config.soft_max_generations)
        # Seeding rule, by what the request is for.
        #
        # A frontier push moves the band past everything the corpus holds, so a
        # corpus seed sits at the old repetition count and cannot parse against
        # the rewritten bound; seeding spends the parse check to discard every
        # seed.
        #
        # A request carrying an OBJECTIVE is the opposite case, and this is what
        # makes progress amortise. Its band stays where the corpus already is,
        # and the inputs that scored best last time are the right place to start
        # from: the next campaign should begin at the extreme the last one
        # reached rather than rediscovering it. Unseeded, every iteration
        # restarts the descent. The corpus is content-addressed and persistent,
        # so this compounds across runs as well as iterations.
        if reg.get("objective"):
            name, direction = reg["objective"]
            # Only inputs that sit inside the band, or they cannot parse against
            # the rewritten bound and the whole seed budget is spent being
            # discarded.
            cand = list(corpus.rows.values())
            within = reg.get("seed_within")
            if within:
                prop, lo, hi = within
                cand = [r for r in cand if lo <= targeting._f(r, prop) <= hi] or cand
            scored = [(targeting._f(r, name), r["input_hash"])
                      for r in cand if name in r]
            scored.sort(reverse=(direction == "maximizing"))
            hashes = list(dict.fromkeys(h for _, h in scored))[:seed_cap]
            seeds = _usable_seeds(hashes)
        elif reg.get("structural"):
            seeds = []
        else:
            seeds = _usable_seeds(reg["seeds"][:seed_cap])
        seeds = [s for s in seeds if s]
        # A subject-supplied generator turns corpus inputs into inputs that
        # already have the property this region wants, which is the only route
        # to a property that neither structure nor search can reach.
        for prop in _region_properties(reg) & set(generators):
            lo, hi = (reg.get("prop_box") or {}).get(prop, (None, None))
            if reg.get("objective") and reg["objective"][0] == prop:
                # An objective names a DIRECTION, not a box. Hand the generator
                # the extreme it is heading for, so it knows which end to aim at.
                lo, hi = ((None, 0.0) if reg["objective"][1] == "minimizing"
                          else (1.0, None))
            made = []
            for src in (seeds or _usable_seeds(reg["seeds"][:seed_cap])):
                if not src:
                    continue
                try:
                    got = generators[prop](src, lo, hi, rng)
                except Exception as e:
                    print(f"  [{reg['label']}] generator for {prop} failed: "
                          f"{type(e).__name__}: {e}")
                    break
                if got:
                    made.extend([got] if isinstance(got, str) else list(got))
            if made:
                print(f"  [{reg['label']}] generator for {prop} produced "
                      f"{len(made)} candidate seed(s)")
                seeds = (seeds or []) + made

        usable = coreografa.parseable_seeds(str(variant), seeds) if seeds else []
        if seeds and len(usable) < len(seeds):
            print(f"  [{reg['label']}] {len(seeds) - len(usable)} of {len(seeds)} "
                  f"seeds do not parse; seeding with {len(usable)}.")
        try:
            coreografa.fuzz(str(variant), input_dir=input_dir,
                            initial_population=usable or None, request_id=f"t{i}",
                            **budget)
        except Exception as e:
            # Seeds may not parse against the (constrained) variant; retry fresh.
            print(f"  [{reg['label']}] seeded re-fuzz failed ({e}); retry without seeds.")
            try:
                coreografa.fuzz(str(variant), input_dir=input_dir,
                                request_id=f"t{i}", **budget)
            except Exception as e2:
                print(f"  [{reg['label']}] re-fuzz failed: {e2}")
        _report_yield(reg, corpus, before_hashes, feature_names, config,
                      _time.time() - started_region,
                      cut=getattr(coreografa, "last_generation_cut", False))
    return open_kinds


def _report_yield(reg, corpus, before_hashes, feature_names, config, elapsed,
                  cut=False):
    """What one request cost and what it returned.

    Three numbers, because a request can fail in three different ways:

    * `new` -- inputs the corpus did not already hold. A request landing where
      the corpus already is adds nothing, and content-addressing makes that
      silent rather than visible.
    * `shapes` -- distinct property signatures among those inputs. This is the
      one worth watching. Asking for eight solutions inside a narrow band
      can return eight inputs that are unique by hash and near-identical in
      substance. Counting inputs hides that completely.
    * `measured` -- of those, the ones carrying a finite primary metric. The
      rest failed or were censored, and were paid for either way.

    Elapsed is here because per-request cost is recorded nowhere else, and its
    spread within one iteration is wide enough to matter: a generator-seeded
    request takes seconds where a structural rewrite can take minutes.
    """
    import core.targeting as targeting

    # A request whose generation hit the wall-clock backstop is not
    # reproducible: a slower machine would have run fewer stages and produced
    # different inputs. Marked here so the run log says WHICH requests lost it.
    mark = " [CUT: generation budget, not reproducible]" if cut else ""
    new = {h for _, h in corpus.rows} - before_hashes
    if not new:
        print(f"  [{reg['label']}] {elapsed:.0f}s: no new inputs{mark}")
        return
    metric = (getattr(config, "primary_metric", None)
              or (config.metrics[0] if config.metrics else None))
    shapes, measured = set(), set()
    for (_, h), row in corpus.rows.items():
        if h not in new:
            continue
        shapes.add(tuple(targeting._f(row, p) for p in feature_names))
        if metric:
            try:
                if math.isfinite(float(row.get(metric, ""))):
                    measured.add(h)
            except (TypeError, ValueError):
                pass
    print(f"  [{reg['label']}] {elapsed:.0f}s: +{len(new)} new input(s), "
          f"{len(shapes)} distinct shape(s), {len(measured)} measured{mark}")
