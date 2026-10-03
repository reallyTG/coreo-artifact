"""Re-measure a subject's existing corpus without re-fuzzing.

    python src/core/remeasure.py <subject> [--dry-run]

The corpus stores its inputs content-addressed under `corpus_inputs/`, and the
properties on each row are computed from the input rather than from a run. So
when a measurement changes -- a harness bug is fixed, a metric is added, a
machine changes -- the inputs and properties are still good and only the metric
columns need redoing. Re-fuzzing to get them back would generate a different
corpus and lose the accumulation.

It also covers rows that are NaN on every metric because a system failed when
they were added, which nothing else regenerates.

Only subjects whose inputs can be rebuilt from stored text without the grammar
are supported, which is every `int_array` subject and every subject whose SUTs
take the input text directly.
"""
import argparse
import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_config(subject):
    """The subject's WorkflowConfig, without running its workflow.

    A subject's example.py exposes `workflow(output_dir, quick)`, which builds
    the config and immediately runs it; there is no accessor for the config
    alone. Rather than add one to all eleven subjects, intercept the call.
    """
    import core.workflow as wf

    captured = {}

    def capture(config, output_dir, *a, **k):
        captured["config"] = config
        return None

    real, wf.run_workflow = wf.run_workflow, capture
    try:
        mod = importlib.import_module(f"subjects.{subject}.example")
        # Some subjects import run_workflow by name at module scope, so patch
        # the binding they actually call through as well.
        mod_real = getattr(mod, "run_workflow", None)
        if mod_real is not None:
            mod.run_workflow = capture
        try:
            mod.workflow(REPO_ROOT / "output" / subject)
        finally:
            if mod_real is not None:
                mod.run_workflow = mod_real
    finally:
        wf.run_workflow = real
    if "config" not in captured:
        raise SystemExit(f"{subject}: workflow() did not call run_workflow()")
    return captured["config"]


def remeasure(subject, dry_run=False):
    from core.corpus import CorpusStore
    from core.fuzzer import Coreografa
    import core.coreografa_metrics as cm
    import core.workflow as wf_module

    config = _load_config(subject)
    output_dir = REPO_ROOT / "output" / subject
    # The same derivation run_workflow uses, so the corpus columns line up.
    custom_properties = wf_module._custom_properties(config.udf_module, config)
    properties = list(custom_properties)
    corpus = CorpusStore(output_dir, config.metrics, properties)
    corpus.load()
    if not corpus.size():
        raise SystemExit(f"{subject}: corpus is empty, nothing to re-measure")

    # A fresh cache. Loading the old one would hand back the very samples this
    # is meant to replace.
    cm.reset()
    cache_path = output_dir / "metrics_cache.json"

    # Only the converter is wanted; nothing here generates or evolves.
    conv = Coreografa(functions_to_execute=[], custom_properties={},
                      input_type=config.input_type).converter_fan_output
    fns = {f.__name__: f for f in config.functions}

    # One row per (system, input); the input only needs converting once.
    by_hash = {}
    for (fn_name, h), row in corpus.rows.items():
        by_hash.setdefault(h, {"row": row, "systems": []})["systems"].append(fn_name)

    print(f"{subject}: {len(by_hash)} inputs x {len(fns)} systems "
          f"= {corpus.size()} rows")
    if dry_run:
        return

    done = skipped = 0
    for i, (h, item) in enumerate(sorted(by_hash.items()), 1):
        raw = corpus.read_input(h)
        if raw is None:
            skipped += len(item["systems"])
            continue
        key = raw.strip()
        _, eval_input = conv(key)
        if eval_input is None or (isinstance(eval_input, list) and not eval_input):
            skipped += len(item["systems"])
            continue
        props = {p: _num(item["row"].get(p)) for p in properties}
        for fn_name in item["systems"]:
            fn = fns.get(fn_name)
            if fn is None:              # a system the subject no longer defines
                skipped += 1
                continue
            stats = cm.measure(eval_input, fn_name, fn, key=key, mode="rigorous",
                               min_n=config.metric_min_n, max_n=config.metric_max_n,
                               primary_metric=config.primary_metric)
            corpus.upsert(fn_name, key, props, stats,
                          int(_num(item["row"].get("last_measured_iter")) or 0),
                          raw_text=raw)
            done += 1
        if i % 25 == 0:
            corpus.save()
            cm.save(str(cache_path))
            print(f"  {i}/{len(by_hash)} inputs, {done} rows, "
                  f"{cm.exec_count()} executions")

    corpus.save()
    cm.save(str(cache_path))
    corpus.write_summary(output_dir / "summary.csv")
    corpus.write_stats(output_dir / "summary_stats.csv")
    print(f"{subject}: re-measured {done} rows, skipped {skipped}, "
          f"{cm.exec_count()} SUT executions")


def reproperty(subject, dry_run=False):
    """Recompute every property on an existing corpus, without running a SUT.

    Needed whenever the property set changes, which adding grammar-derived
    properties does for every subject at once. `CorpusStore._migrate` fills an
    absent column with 0, so without this the historical rows would enter the
    models claiming `count_text = 0` -- silently, and for the majority of the
    corpus in most subjects.

    Properties are computed from a derivation tree, and the corpus stores input
    text, so each input is parsed back against the grammar. An input the
    current grammar cannot parse keeps its old properties and is reported: that
    is a grammar edit having outrun the corpus, and guessing at it would be
    worse than saying so.
    """
    from fandango.api import parse
    from core.corpus import CorpusStore
    import core.workflow as wf_module

    config = _load_config(subject)
    output_dir = REPO_ROOT / "output" / subject
    custom_properties = wf_module._custom_properties(config.udf_module, config)
    properties = list(custom_properties)
    corpus = CorpusStore(output_dir, config.metrics, properties)
    corpus.load()
    if not corpus.size():
        raise SystemExit(f"{subject}: corpus is empty, nothing to re-property")

    with open(config.fan_filepath) as fh:
        grammar, _ = parse(fh, use_stdlib=False)

    hashes = sorted({h for _, h in corpus.rows})
    print(f"{subject}: {len(hashes)} inputs, {len(properties)} properties "
          f"({', '.join(properties)})")
    if dry_run:
        return

    done = unparsed = 0
    for i, h in enumerate(hashes, 1):
        raw = corpus.read_input(h)
        if raw is None:
            unparsed += 1
            continue
        tree = grammar.parse(raw) or grammar.parse(raw.strip())
        if tree is None:
            unparsed += 1
            continue
        values = {}
        for name, fn in custom_properties.items():
            try:
                values[name] = fn(tree)
            except Exception:
                values[name] = 0
        done += corpus.set_properties(h, values)
        if i % 100 == 0:
            corpus.save()
            print(f"  {i}/{len(hashes)} inputs")

    corpus.save()
    corpus.write_summary(output_dir / "summary.csv")
    corpus.write_stats(output_dir / "summary_stats.csv")
    print(f"{subject}: updated {done} rows; {unparsed} of {len(hashes)} inputs "
          f"could not be parsed and kept their old properties")


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("subjects", nargs="+")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be re-measured and exit")
    ap.add_argument("--properties", action="store_true",
                    help="recompute properties only; no SUT executions")
    args = ap.parse_args()
    for s in args.subjects:
        if args.properties:
            reproperty(s, dry_run=args.dry_run)
        else:
            remeasure(s, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.path.insert(0, str(REPO_ROOT / "src"))
    main()
