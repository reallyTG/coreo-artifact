"""JSONPath runner for four Python implementations.

Invoked as:  <env python> py_runner.py <input-file> <k> <engine>
where engine is one of: ng | pyjsonpath | rfc9535 | jpython

    ng          jsonpath-ng 1.8.0 (with its `ext` parser), ~12.7M downloads/wk
    pyjsonpath  python-jsonpath 2.2.1, RFC 9535 plus extensions
    rfc9535     jsonpath-rfc9535 1.0.0, RFC 9535, runs the compliance suite
    jpython     jsonpath-python 1.1.6

Each library gets its own virtualenv under envs/, because python-jsonpath and
jsonpath-python both install a module named `jsonpath` and cannot coexist.

json.loads and query compilation are both outside the timed region; see the
comment at the engine table below for why compilation is excluded.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from core import bench_runner

# JSONPATH_PY_LEDGER redirects it, so a scratch run with --output-dir stays out of output/.
import os
LEDGER = pathlib.Path(os.environ.get("JSONPATH_PY_LEDGER") or
                      pathlib.Path(__file__).resolve().parents[2] / "output" / "jsonpath_py" / "runner_failures.jsonl")

path, k, engine = sys.argv[1], int(sys.argv[2]), sys.argv[3]
text = pathlib.Path(path).read_text(encoding="utf-8")
query, _, raw = text.partition("\n@@@\n")
doc = json.loads(raw)

# The query is compiled once, outside the timed region, and only evaluation is
# measured. jsonpath-ng has no one-shot API and its PLY-based parser costs
# about 55ms per call on a trivial query, roughly a thousand times its
# evaluation cost, so timing parse+evaluate would compare parsers and hide
# every difference in matching. Compile time is reported separately as
# compile_ns.
import time

if engine == "ng":
    import jsonpath_ng.ext as ng
    t0 = time.perf_counter_ns()
    compiled = ng.parse(query)
    compile_ns = time.perf_counter_ns() - t0
    run = lambda: len(compiled.find(doc))
elif engine == "pyjsonpath":
    import jsonpath as pj
    t0 = time.perf_counter_ns()
    compiled = pj.compile(query)
    compile_ns = time.perf_counter_ns() - t0
    run = lambda: len(compiled.findall(doc))
elif engine == "rfc9535":
    import jsonpath_rfc9535 as r9
    t0 = time.perf_counter_ns()
    compiled = r9.compile(query)
    compile_ns = time.perf_counter_ns() - t0
    run = lambda: len(compiled.find(doc))
elif engine == "jpython":
    from jsonpath import JSONPath
    t0 = time.perf_counter_ns()
    compiled = JSONPath(query)
    compile_ns = time.perf_counter_ns() - t0
    run = lambda: len(compiled.parse(doc) or [])
else:
    print(f"unknown engine: {engine}", file=sys.stderr)
    sys.exit(2)

try:
    t0 = time.perf_counter_ns()
    hits = run()                      # fail fast; doubles as warm-up
    first_ns = time.perf_counter_ns() - t0
except Exception as exc:              # noqa: BLE001 - any library error is a finding
    import hashlib
    try:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a") as fh:
            fh.write(json.dumps({
                "engine": engine,
                "sha1": hashlib.sha1(text.encode()).hexdigest(),
                "error": type(exc).__name__,
                "message": str(exc)[:300],
                "query": query,
                "doc_bytes": len(raw),
            }) + "\n")
    except OSError:
        pass
    print(f"query failed: {exc}", file=sys.stderr)
    sys.exit(3)

# Cap repetitions at a time budget, so a slow input is measured rather than
# killed by the subprocess timeout.
BUDGET_NS = 5e9
k_eff = max(1, min(k, int(BUDGET_NS / max(first_ns, 1))))
metrics = bench_runner.run(run, k=k_eff, warmup=0)
metrics.update(hits=hits, k_used=k_eff, compile_ns=compile_ns)
print(" ".join(f"{key}={value}" for key, value in metrics.items()))
