"""python-jsonpath runner for the pyjsonpath_known known-pair subject.

Invoked as:  <envs/<version>/bin/python> py_runner.py <input-file> <k>

Mirrors the `pyjsonpath` path of subjects/jsonpath_py/py_runner.py and is kept
identical to it in everything that decides what is observed: the input is
`query \\n@@@\\n document`, json.loads and the query compile (jsonpath.compile)
are outside the timed region with compile time reported as compile_ns, the
measured operation is len(compiled.findall(doc)), the first call is the fail-fast warm-up and
the estimate for the 5s repetition budget, failures go to a ledger
(JSONPATH_PY_LEDGER redirects it), and `hits` is the result-shape check. The
version is whichever python-jsonpath the invoking venv holds; `version` is printed for
the record and ignored by the harness.

1.3.2 and 2.0.0 both expose jsonpath.compile() returning an object whose
findall() returns a list, so one code path serves both. Internally 2.0.0 is a
different implementation (new segments.py, lru_cache.py, a starts_with()
function, and a shared regex base class for match()/search()), so a query one
version rejects lands in the ledger for that version only. 2.0.0 adds an
optional `strict` extra (regex, iregexp-check); it is not installed, matching
the domain's pyjsonpath env, so 2.0.0's match()/search() use the stdlib `re`
module. 1.3.2 has no such extra and always uses `re`.
"""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from core import bench_runner

LEDGER = pathlib.Path(os.environ.get("JSONPATH_PY_LEDGER") or
                      pathlib.Path(__file__).resolve().parents[2] / "output" / "pyjsonpath_known" / "runner_failures.jsonl")

path, k = sys.argv[1], int(sys.argv[2])
text = pathlib.Path(path).read_text(encoding="utf-8")
query, _, raw = text.partition("\n@@@\n")
doc = json.loads(raw)

import time
from importlib.metadata import version as _dist_version

import jsonpath as pj

engine = "pyjsonpath_" + _dist_version("python-jsonpath").replace(".", "_")

t0 = time.perf_counter_ns()
compiled = pj.compile(query)
compile_ns = time.perf_counter_ns() - t0
run = lambda: len(compiled.findall(doc))

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
print(" ".join(f"{key}={value}" for key, value in metrics.items()), f"version={engine}")
