from pathlib import Path
from fandango.evolution.algorithm import Fandango
from fandango.api import parse
import tracemalloc
import time
import csv


class Coreografa:

    def __init__(self, functions_to_execute: list, custom_properties: dict,
                 non_terminals=None, input_type="string",
                 population_size=20, desired_solutions=20, max_generations=None,
                 max_nodes=None, udf_path=None, use_metric_cache=False,
                 min_n=5, max_n=30, primary_metric="runtime_ns",
                 random_seed=None, generation_budget_s=None,
                 generation_stage=5):
        """
        functions_to_execute: list of callables to profile
        custom_properties: dict mapping property name -> callable(derivation_tree) -> value
        input_type: "string" (pass DerivationTree directly) or "int_array" (parse CSV integers)
        max_generations: cap on Fandango generations per evolve (None = unbounded)
        udf_path: path to user_def_functions.py, needed for re-fuzzing with constraints
        use_metric_cache: measure kept inputs once-to-significance via
                          the harness-owned coreografa_metrics cache (samples persist
                          across rounds). Requires a structural (SUT-free) grammar.
        min_n/max_n: sample bounds for the rigorous measurement stopping rule.
        primary_metric: the metric the stopping rule watches. Must be one the
                        SUTs actually report — a self-reporting runner that
                        emits its own metric names has to name one of them
                        here.
        random_seed: base seed for Fandango's RNG, or None to leave it unseeded.

                     A seeded run is reproducible, and the ablation's arms can
                     be paired; unseeded, each arm is an independent draw,
                     which is the wrong footing for the comparison the
                     ablation exists to make. Every `evolve` in a run takes
                     `random_seed + n` for its own n, so the run as a whole
                     is reproducible while no two evolves share a stream.
        """
        self.fns = functions_to_execute
        self.collected_metrics = []
        self.collected_props = []
        self.collected_stats = []
        self.custom_properties = custom_properties
        self.non_terminals = non_terminals
        self.input_type = input_type
        self.population_size = population_size
        self.desired_solutions = desired_solutions
        self.max_generations = max_generations
        self.max_nodes = max_nodes
        self.udf_path = Path(udf_path) if udf_path else None
        self.use_metric_cache = use_metric_cache
        self.min_n = min_n
        self.max_n = max_n
        self.primary_metric = primary_metric
        self.random_seed = random_seed
        self._evolves = 0        # bumped per evolve, to offset the base seed
        # Wall-clock backstop on ONE generation call, and the stage size the
        # clock is checked between. None disables it.
        self.generation_budget_s = generation_budget_s
        self.generation_stage = generation_stage
        self.last_generation_cut = False
        self.corpus = None       # optional CorpusStore; set by the workflow
        self.iteration = 0       # current loop iteration (recorded in the corpus)
        # Mid-measurement durability. The workflow sets `checkpoint` to a
        # callable that persists the corpus and the metric cache. Exploration
        # measures every input before the workflow regains control, so without
        # this an interrupted run discards every SUT execution it paid for.
        self.checkpoint = None
        self.checkpoint_every = 25
        # Optional wall-clock deadline (a time.time() value). Measurement is
        # where a run spends most of its time, so a budget that is only checked
        # at iteration boundaries can overrun it by a whole measurement round.
        self.deadline = None

    def converter_fan_output(self, solution):
        if self.input_type == "int_array":
            input_str = str(solution).strip()
            clean = []
            for x in input_str.split(","):
                try:
                    clean.append(int(x.strip()))
                except (ValueError, TypeError):
                    pass
            if clean:
                # Keep the grammar's own text (e.g. "1, 2, 3") as the saved file
                # content so it round-trips as a seed; eval_input is the parsed
                # int list. (Re-joining without spaces breaks seed re-parsing.)
                return input_str, clean
            return "", []
        else:
            # The STRING, not the tree. A SUT that receives the tree has to call
            # str(tree) itself, and for an in-process subject that conversion
            # then sits inside the timed region, where tree stringification can
            # cost far more than the parse being measured. Converting once here
            # also means it happens once per input rather than once per
            # measurement sample, which an out-of-process subject would pay
            # too (str(input_value) on every subprocess launch).
            text = str(solution)
            return text, text

    def generate_inputs(self, grammar_filepath, input_dir: Path,
                        initial_population=None, request_id=None,
                        max_nodes=None, max_repetition=None,
                        expected_fitness=None, objective=None,
                        soft_max_generations=None):
        if grammar_filepath is None:
            print("[ERROR] No grammar file path provided to generate_inputs()")
            return []

        input_dir = Path(input_dir)
        input_dir.mkdir(parents=True, exist_ok=True)
        inputs = []

        try:
            with open(grammar_filepath, "r") as file:
                grammar, constraints = parse(file, use_stdlib=False)
        except FileNotFoundError as e:
            print(f"[ERROR] File Not Found: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] Unexpected issue while parsing grammar: {e}")
            return []

        # `max_repetition` is a GRAMMAR setting, default 20, and it is what
        # bounds `*` and `+` during generation -- not max_nodes. Raising
        # max_nodes does not lengthen a free `*`; raising max_repetition does.
        # Left unset, every `*`/`+` axis is silently capped at 20 whenever a
        # request does not push the search past it.
        # An explicit `{lo,hi}` in the grammar overrides this, which is why a
        # structural rewrite does not need it.
        if max_repetition is not None:
            grammar.set_max_repetition(int(max_repetition))

        fandango_kwargs = dict(population_size=self.population_size,
                               initial_population=initial_population,
                               best_effort=True)
        # Seeded only when asked for, so an unseeded run leaves Fandango's RNG
        # untouched.
        if self.random_seed is not None:
            fandango_kwargs["random_seed"] = self.random_seed + self._evolves
        self._evolves += 1
        # ...and `max_repetitions` (plural) is what stops Fandango raising it
        # again behind us. Its AdaptiveTuner adds 50% to max_repetition on
        # every generation where fitness improvement stalls or population
        # diversity drops, up to an internal ceiling of 1000, and writes the
        # result back onto the grammar. So the setting above is an opening bid
        # under `evolve`, not a bound.
        #
        # That escalation cannot help the requests it fires on. A `joint` or a
        # rung-2 `beyond` pins its target axis with an explicit `{lo,hi}`, so
        # widening reaches only the axes the request did NOT ask about, while
        # the objective stays indifferent to them. It adds generation cost
        # with no gain on the thing requested.
        #
        # Escalation stays available, deliberately: `_structural_beyond` raises
        # `max_repetition` per rung, and the cap follows it, so the reach is
        # set by the rung that asked for it rather than by a stall.
        if max_repetition is not None:
            fandango_kwargs["max_repetitions"] = int(max_repetition)
        # Fandango emits an individual only once its fitness reaches
        # `expected_fitness` (default 1.0), which under a soft objective means
        # the running extreme. Exposed per request so an objective over a
        # near-continuous property, where few individuals tie at the extreme,
        # can lower the bar. (A soft-objective request that returns nothing
        # is more often short of node budget than held back by this.)
        if expected_fitness is not None:
            fandango_kwargs["expected_fitness"] = expected_fitness
        nodes = self.max_nodes if max_nodes is None else max_nodes
        if nodes is not None:
            # Fandango's default max_nodes (200) caps tree size; raise it so
            # larger inputs (and extrapolation past the observed max) are reachable.
            fandango_kwargs["max_nodes"] = nodes


        # A soft objective needs the generation budget actually spent. `evolve`
        # returns as soon as `desired_solutions` individuals qualify, and under
        # an objective the earliest individuals qualify by definition -- they
        # are the running extreme, and the call returns having never left the
        # first few generations. So ask for more solutions than it can
        # produce, cap by generations, and keep the best.
        if objective:
            want, gens = 10 ** 9, (soft_max_generations or self.max_generations)
        else:
            want, gens = self.desired_solutions, self.max_generations

        # STAGED, so the generation budget can be bounded in TIME as well as in
        # generations. Every other bound here is on work as DECLARED -- the
        # repetition count, the node budget, the generation cap -- and none of
        # them bounds work as EXPERIENCED: 200k nodes is milliseconds on a
        # flat list grammar and 25 minutes on selectors_js, which nests through
        # <child>* in three element types. Without a bound inside generation
        # a selectors_js request can run 25 minutes past a 1500s wall budget,
        # because the workflow checks the clock at iteration boundaries and
        # during measurement, never inside generation.
        #
        # Fandango has no time-based stop (no time/budget/seconds parameter
        # anywhere in `evolve`) and its solution_callback only fires when a
        # solution is produced, which is exactly what does not happen during a
        # hang. So the budget is imposed from outside, by running SHORT stages
        # and checking the clock between them, each seeded from the last --
        # the shape the `joint` region kind uses across iterations.
        #
        # Staging rather than truncating matters for soft objectives. `evolve`
        # returns its running extreme first, so cutting one long call short
        # would hand back the EARLY extreme. Seeding each stage from the last
        # lets the objective keep improving and takes best-so-far, so the
        # budget is a checkpoint interval and not a guillotine.
        #
        # KNOWN LIMIT: this bounds the overrun to ONE stage, not to zero. A
        # single pathological generation still runs to completion; only
        # subprocess isolation would fix that, and it would cost the in-process
        # metric cache.
        budget = self.generation_budget_s
        deadline = (time.time() + budget) if budget else None
        stage_gens = max(1, min(self.generation_stage, gens or self.generation_stage))

        # Solutions ACCUMULATE across stages rather than each stage replacing
        # the last. Replacing loses ground whenever a stage happens to return
        # fewer individuals than the one before it, which is ordinary GA
        # noise. Keyed by rendered string, so a solution rediscovered in a
        # later stage is not counted twice.
        #
        # Capped because a soft objective asks for 10**9 solutions and would
        # otherwise grow without bound across stages. Well above anything
        # measurement consumes: the caller keeps `desired_solutions` of these
        # and measuring is what costs.
        seen = {}
        ACCUMULATOR_CAP = 5000
        carry, spent = initial_population, 0
        self.last_generation_cut = False
        while True:
            kwargs = dict(fandango_kwargs, initial_population=carry or None)
            try:
                out = Fandango(grammar, constraints, **kwargs).evolve(
                    desired_solutions=want, max_generations=stage_gens)
            except RecursionError:
                # A recursive grammar with a generous node budget can nest
                # deeper than Python's stack survives, inside Fandango's own
                # tree walk. One band blowing up should cost that band, not
                # the run.
                print(f"[WARNING] recursion limit hit generating from "
                      f"{grammar_filepath}; lower max_repetition or max_nodes "
                      f"for this grammar.")
                return []
            for sol in (out or []):
                if len(seen) >= ACCUMULATOR_CAP:
                    break
                seen.setdefault(str(sol), sol)
            fan_output = list(seen.values())
            spent += stage_gens
            if gens is not None and spent >= gens:
                break
            if not objective and len(fan_output) >= (want or 0):
                break                      # hard request satisfied; stop early
            if deadline is not None and time.time() >= deadline:
                # Reproducibility is LOST for this request when this fires: a
                # slower machine would have run fewer stages and produced
                # different inputs. Said out loud, and recorded per request, so
                # it is known which rows lost it rather than assuming none did.
                self.last_generation_cut = True
                print(f"[budget] generation cut at {budget}s after {spent} "
                      f"generations ({len(fan_output)} solutions); this "
                      f"request is not reproducible")
                break
            if not out:
                break                      # nothing came back; more stages will not help
            carry = out

        if not fan_output:
            print("[WARNING] Fandango did not generate any valid inputs.")
            return []

        if objective:
            name, direction = objective
            fn = self.custom_properties.get(name)
            if fn is not None:
                def score(sol):
                    try:
                        return float(fn(sol))
                    except Exception:
                        return float("inf")
                ranked = sorted(fan_output, key=score,
                                reverse=(direction == "maximizing"))
                # Evenly spaced over the better half, not the top k. The top k
                # are near-duplicates from one lineage, all at the same property
                # value, which is one data point measured ten times. The half
                # that matters is the one the corpus does not already cover,
                # and spreading across it gives the fit a range instead of a
                # spike while still keeping the extreme.
                k = self.desired_solutions
                pool = ranked[:max(k, len(ranked) // 2)]
                if len(pool) <= k:
                    kept = pool
                else:
                    step = (len(pool) - 1) / (k - 1) if k > 1 else 1
                    kept = [pool[round(i * step)] for i in range(k)]
                print(f"  [soft] {direction} {name}: {len(ranked)} candidates, "
                      f"best={score(ranked[0]):.4g}, keeping {len(kept)} spanning "
                      f"{score(kept[0]):.4g}..{score(kept[-1]):.4g}")
                fan_output = kept

        for i, solution in enumerate(fan_output, start=1):
            input_id = f"{request_id}_{i}" if request_id else str(i)
            file_content, eval_input = self.converter_fan_output(solution)
            if not file_content and self.input_type == "int_array":
                print(f"[WARNING] Empty int_array content for {input_id}, skipping.")
                continue
            filename = input_dir / f"input_{input_id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(file_content + "\n")
            inputs.append((input_id, solution, eval_input))
        return inputs

    def collect_metrics(self, eval_input, fn, key=None):
        if self.use_metric_cache:
            # Rigorous, cached, statistical measurement of a kept
            # input. Samples persist across rounds (keyed by `key`), so recurring
            # seeds are not re-measured. Summary uses the mean; full stats go to
            # the sidecar.
            import core.coreografa_metrics as cm
            stats = cm.measure(eval_input, fn.__name__, fn, key=key,
                               mode="rigorous", min_n=self.min_n, max_n=self.max_n,
                               primary_metric=self.primary_metric)
            rt = stats.get("runtime_ns", {})
            mem = stats.get("memory_peak", {})
            return {
                "run-time": rt.get("mean", 0),
                "memory_after": 0,
                "memory_peak": mem.get("mean", 0),
                "_stats": stats,
            }
        # Default path: a single inline measurement.
        # Copy list inputs so an in-place SUT (e.g. an in-place sort) can't
        # mutate the shared input and skew the next function's measurement.
        # Timing and memory in separate executions, for the reason spelled out
        # in core.coreografa_metrics._run_once: timing with tracemalloc active
        # charges the SUT an overhead that grows with input size.
        def fresh():
            return list(eval_input) if isinstance(eval_input, list) else eval_input

        start_time = time.perf_counter_ns()
        try:
            fn(fresh())
        except Exception as e:
            print(f"Error running {fn.__name__} on input: {e}")
            return {"run-time": 0, "memory_after": 0, "memory_peak": 0}
        end_time = time.perf_counter_ns()

        tracemalloc.start()
        try:
            fn(fresh())
        except Exception:
            pass
        memory_consumed = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            "run-time": end_time - start_time,
            "memory_after": memory_consumed[0],
            "memory_peak": memory_consumed[1],
        }

    def collect_properties(self, solution):
        props = {}
        for prop_name, func in self.custom_properties.items():
            try:
                props[prop_name] = func(solution)
            except Exception as e:
                print(f"[ERROR] Property '{prop_name}' failed: {e}")
                props[prop_name] = 0
        return props

    def parseable_seeds(self, grammar_filepath, seeds):
        """The subset of `seeds` that this grammar can parse.

        Fandango rejects the entire initial population if any one member fails
        to parse, so a single stale seed turns a seeded re-fuzz into an unseeded
        one. Checking each seed first keeps the rest. `Grammar.parse` returns
        None rather than raising, so this costs one grammar parse plus one input
        parse per seed.
        """
        if not seeds:
            return []
        try:
            with open(grammar_filepath, "r") as file:
                grammar, _ = parse(file, use_stdlib=False)
        except Exception as e:
            print(f"[WARNING] Could not parse grammar to check seeds: {e}")
            return []
        usable = []
        for s in seeds:
            try:
                if grammar.parse(s) is not None:
                    usable.append(s)
            except RecursionError:
                # Fandango's parser deepcopies its table per character, so a
                # deep seed can exhaust the stack INSIDE the parse, even after
                # the generation guard has caught the same error in the same
                # region. A seed that cannot be parsed is a seed to drop, never
                # a reason to end a run.
                print("[WARNING] recursion limit hit parsing a seed; "
                      "dropping it.")
        return usable

    def fuzz(self, grammar_filepath, input_dir: Path,
             initial_population=None, request_id=None, non_terminals=None,
             max_nodes=None, max_repetition=None, expected_fitness=None,
             objective=None, soft_max_generations=None):
        inputs_to_run = self.generate_inputs(
            grammar_filepath, input_dir,
            initial_population=initial_population,
            request_id=request_id,
            max_nodes=max_nodes, max_repetition=max_repetition,
            expected_fitness=expected_fitness, objective=objective,
            soft_max_generations=soft_max_generations,
        )
        self._measure_inputs(inputs_to_run)

    def _band_covered(self, corpus, band_props, nt, lo, hi, per_stratum):
        """True when the corpus already holds `per_stratum` inputs in this band.

        Coverage per stratum is the invariant, and a stratum the corpus covers
        is covered however it got that way, so regenerating it buys nothing and
        is paid for out of the same wall clock as the targeted requests.

        `band_props` maps the banded non-terminal to the corpus column that
        counts it, and the CALLER builds it, because resolving the name needs
        the subject's ALIASES. Deriving it from `sites` does not work: one site
        governs many non-terminals, so `<row>` resolves to `count_cell` as
        readily as to `count_row`, and a `<row>{1,25}` band checked against a
        cell count is checked against the wrong numbers.
        """
        if corpus is None or per_stratum <= 0 or not band_props:
            return False
        prop = (band_props or {}).get(nt)
        if prop is None:
            return False                # unmapped axis: cannot check, so generate
        seen = set()
        for (_, h), row in corpus.rows.items():
            try:
                v = float(row.get(prop, ""))
            except (TypeError, ValueError):
                continue
            if lo <= v <= hi:
                seen.add(h)
                if len(seen) >= per_stratum:
                    return True
        return False

    def fuzz_marginal(self, base_grammar_filepath, input_dir: Path, axes,
                      grammar_dir: Path, sites=None, per_stratum=3,
                      max_repetition=None, corpus=None, band_props=None):
        """Band one axis at a time, every other axis left free.

        The product over axes is what `fuzz_stratified` does, and it is
        infeasible past two or three: jsonpath_js has eight axes, so the product
        is tens of thousands of generation runs. Marginal allocation is LINEAR
        -- axes x bands -- and guarantees spread on every axis while saying
        nothing about combinations, which is the right division of labour
        because combinations are what the loop's `joint` requests are for.

        `per_stratum` inputs per band, not a budget divided across bands. A
        divided budget silently gives some strata nothing when there are more
        strata than inputs, which is the empty region stratification exists to
        prevent. Coverage per stratum is the invariant; if the total is
        unaffordable the answer is fewer bands or fewer axes, never fewer than
        `per_stratum` in a band that is being sampled at all.

        Bands that come back empty are reported. A band the grammar cannot fill
        is a fact about the language, the same kind the frontier report makes.
        """
        from core.grammar_emit import rewrite_repetition
        grammar_dir = Path(grammar_dir)
        grammar_dir.mkdir(parents=True, exist_ok=True)
        base_text = Path(base_grammar_filepath).read_text()
        saved = self.desired_solutions
        self.desired_solutions = per_stratum
        all_inputs, empty = [], []
        try:
            for ai, axis in enumerate(axes):
                nt = axis["nt"]
                for bi, (lo, hi) in enumerate(axis["bands"]):
                    if self._band_covered(corpus, band_props, nt, lo, hi,
                                          per_stratum):
                        print(f"  [explore] band {nt.strip('<>')}{lo}-{hi}: "
                              f"covered (>={per_stratum} inputs in the corpus); "
                              f"skipping")
                        continue
                    variant_text = rewrite_repetition(base_text, nt, lo, hi)
                    label = f"{nt.strip('<>')}{lo}-{hi}"
                    path = (grammar_dir /
                            f"{self._eval_name(base_grammar_filepath)}_m{ai}_{bi}_{label}.fan")
                    path.write_text(variant_text)
                    nodes = self.max_nodes
                    if sites and nt in sites:
                        from core.targeting import _node_budget
                        nodes = max(nodes or 0, _node_budget(sites[nt], hi))
                    got = self.generate_inputs(str(path), input_dir,
                                               request_id=f"m{ai}_{bi}",
                                               max_nodes=nodes,
                                               max_repetition=max_repetition)
                    if not got:
                        empty.append(label)
                    all_inputs.extend(got)
            print(f"  [explore] {len(axes)} axes, "
                  f"{sum(len(a['bands']) for a in axes)} strata, "
                  f"{per_stratum}/stratum -> {len(all_inputs)} inputs")
            if empty:
                print(f"  [explore] {len(empty)} stratum/strata produced "
                      f"nothing: {', '.join(empty[:6])}"
                      + (" ..." if len(empty) > 6 else ""))
        finally:
            self.desired_solutions = saved
        self._measure_inputs(all_inputs)

    def fuzz_stratified(self, base_grammar_filepath, input_dir: Path,
                        stratify, grammar_dir: Path, sites=None,
                        corpus=None, per_stratum=0, band_props=None):
        """Range-stratified exploration: structurally band one or more
        repetitions in the grammar so generated inputs are guaranteed to span
        the property axes, rather than relying on the GA's diversity.

        stratify is either one spec or a list of them:

            {"nt": "<more_member>", "bands": [(lo, hi), ...]}
            [{"nt": "<more_member>", "bands": [...]},
             {"nt": "<more_value>", "bands": [...]}]

        For each band we rewrite the repetition on `<nt>` to `<nt>{lo,hi}`,
        generate from that variant, and union the results. With several specs we
        generate from every combination of their bands, because a subject can
        have two independent cost axes and banding only one leaves the other to
        chance. The cost is multiplicative: three specs of four bands is 64
        generation runs, so keep the band count per axis small.

        `<nt>{n,m}`, `<nt>*` and `<nt>+` are all rewritable, so a subject
        grammar does not need to write a cap to make an axis bandable. A cap
        written for that purpose becomes the axis's ceiling, and `prop_beyond`
        pins against it forever. With `*` and `+` handled, the grammar states
        the language and the ranges live in `stratify` (exploration), the
        targeted `where` clauses (regeneration) and `max_nodes` (the one real
        budget), which is where an experiment parameter belongs.

        Right-recursion (`<text> ::= <text_char> <text>`) is also unbounded
        repetition but is not a repetition operator, so it stays unbandable.
        Write those as `<text_char>+` to band them.

        Given a `corpus` and a `per_stratum` count, a band already holding that
        many measured inputs is SKIPPED. Coverage per stratum is the invariant,
        and a stratum the corpus already covers is covered however it got that
        way -- regenerating it buys nothing and is paid for out of the same
        wall clock as the targeted requests.

        That matters once a corpus is warm: re-measuring fresh exploration
        inputs on every run can take most of the wall budget and leave no room
        for the later targeted requests.
        """
        import itertools
        from core.grammar_emit import rewrite_repetition
        grammar_dir = Path(grammar_dir)
        grammar_dir.mkdir(parents=True, exist_ok=True)
        base_text = Path(base_grammar_filepath).read_text()
        specs = [stratify] if isinstance(stratify, dict) else list(stratify)

        combos = itertools.product(
            *[[(spec["nt"], lo, hi) for lo, hi in spec["bands"]] for spec in specs])

        # Every axis of a combo has to be covered for the combo to be, and an
        # axis this subject cannot map is treated as uncovered so the band is
        # still generated. `_band_covered` carries the rest, including why
        # `band_props` comes from the caller.
        def already_covered(combo):
            if not all(nt in (band_props or {}) for nt, _, _ in combo):
                return False
            return all(self._band_covered(corpus, band_props, nt, lo, hi,
                                          per_stratum)
                       for nt, lo, hi in combo)

        all_inputs = []
        for bi, combo in enumerate(combos):
            if already_covered(combo):
                label = "_".join(f"{nt.strip('<>')}{lo}-{hi}"
                                 for nt, lo, hi in combo)
                print(f"  [explore] band {label}: covered "
                      f"(>={per_stratum} inputs in the corpus); skipping")
                continue
            variant_text = base_text
            for nt, lo, hi in combo:
                variant_text = rewrite_repetition(variant_text, nt, lo, hi)
            label = "_".join(f"{nt.strip('<>')}{lo}-{hi}" for nt, lo, hi in combo)
            variant_path = grammar_dir / f"{self._eval_name(base_grammar_filepath)}_band{bi}_{label}.fan"
            variant_path.write_text(variant_text)
            # Per band, not per run. A band setting the repetition to 200 needs a
            # node budget to match, or Fandango honours the count and takes the
            # cheapest derivation for every element, so a 200-element band at
            # 200 nodes yields near-identical elements and measures nothing.
            # Wider bands need more, and the narrow bands in the same spec
            # should not pay for it.
            nodes = self.max_nodes
            if sites:
                from core.targeting import _node_budget
                need = max((_node_budget(s, hi) for nt, lo, hi in combo
                            if (s := sites.get(nt)) is not None), default=0)
                if need > (nodes or 0):
                    nodes = need
            band_inputs = self.generate_inputs(
                str(variant_path), input_dir, request_id=f"b{bi}",
                max_nodes=nodes)
            print(f"  [explore] band {label}: {len(band_inputs)} inputs "
                  f"(max_nodes={nodes})")
            all_inputs.extend(band_inputs)
        self._measure_inputs(all_inputs)

    @staticmethod
    def _eval_name(path):
        return Path(path).stem

    def _measure_inputs(self, inputs_to_run):
        self.collected_metrics = []
        self.collected_props = []
        self.collected_stats = []
        for done, (input_id, solution, eval_input) in enumerate(inputs_to_run, 1):
            props = self.collect_properties(solution)
            key = str(solution).strip()  # canonical input -> stable cache key across rounds
            raw = str(solution)          # exact input: what the corpus stores as a seed
            for fn in self.fns:
                try:
                    metrics = self.collect_metrics(eval_input, fn, key=key)
                except Exception as e:
                    print(f"[ERROR] Failed to collect metrics for input {input_id}: {e}")
                    continue
                metrics["input_id"] = input_id
                metrics["function_name"] = fn.__name__
                stats = metrics.pop("_stats", None)
                if stats is not None:
                    self.collected_stats.append(
                        {"function_name": fn.__name__, "input_id": input_id,
                         "stats": stats})
                self.collected_metrics.append(metrics)
                self.collected_props.append(props)
                if self.corpus is not None:
                    self.corpus.upsert(fn.__name__, key, props,
                                       self._corpus_stats(metrics, stats),
                                       self.iteration, raw_text=raw)
            if self.checkpoint is not None and done % self.checkpoint_every == 0:
                self.checkpoint()
            if self.deadline is not None and time.time() > self.deadline:
                print(f"[WARNING] wall-clock budget reached after {done} of "
                      f"{len(inputs_to_run)} inputs; keeping what is measured.")
                if self.checkpoint is not None:
                    self.checkpoint()
                break

    def _corpus_stats(self, metrics, stats):
        """Normalize to {metric_name: {n,mean,std,ci}} for the corpus.
        Uses rigorous stats when available; else a single-sample fallback."""
        if stats is not None:
            return stats
        rt = metrics.get("run-time", 0)
        mem = metrics.get("memory_peak", 0)
        return {
            "runtime_ns": {"n": 1, "mean": rt, "std": 0, "ci": (rt, rt)},
            "memory_peak": {"n": 1, "mean": mem, "std": 0, "ci": (mem, mem)},
        }

    def write_summary(self, summary_path):
        summary_path = Path(summary_path)
        if not self.collected_metrics or not self.collected_props:
            print("[WARNING] No data to write to summary.")
            return
        prop_keys = list(self.collected_props[0].keys())
        fields = ["function_name", "input_id", "runtime_ns", "memory_after", "memory_peak"] + prop_keys
        with open(summary_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for metric, props in zip(self.collected_metrics, self.collected_props):
                if not isinstance(metric, dict) or not isinstance(props, dict):
                    continue
                row = [
                    metric.get("function_name", ""),
                    metric.get("input_id", ""),
                    metric.get("run-time", 0),
                    metric.get("memory_after", 0),
                    metric.get("memory_peak", 0),
                ] + [props.get(k, 0) for k in prop_keys]
                writer.writerow(row)

    def write_stats_sidecar(self, sidecar_path):
        """Write the full statistical object per (input, system, metric).

        summary.csv keeps single (mean) values for the analyzer; this sidecar
        carries n / mean / std / CI so modeling can be uncertainty-aware.
        """
        if not self.collected_stats:
            return
        sidecar_path = Path(sidecar_path)
        fields = ["function_name", "input_id", "metric", "n", "mean", "std",
                  "ci_lo", "ci_hi", "rel_margin"]
        with open(sidecar_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            for row in self.collected_stats:
                for metric, s in row["stats"].items():
                    ci = s.get("ci", (0, 0))
                    writer.writerow([
                        row["function_name"], row["input_id"], metric,
                        s.get("n", 0), s.get("mean", 0), s.get("std", 0),
                        ci[0], ci[1], s.get("rel_margin", 0),
                    ])

    def split_summary_by_function(self, main_summary_path, output_dir: Path):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(main_summary_path, "r") as infile:
            reader = csv.reader(infile)
            header = next(reader)
            function_groups = {}
            for row in reader:
                if not row:
                    continue
                function_groups.setdefault(row[0], []).append(row)
        for fn_name, rows in function_groups.items():
            out_file = output_dir / f"{fn_name}_summary.csv"
            with open(out_file, "w", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(rows)
            print(f"Wrote {len(rows)} rows for {fn_name} -> {out_file}")
