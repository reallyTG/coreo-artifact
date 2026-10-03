"""orjson runner for the latest-release-series subject.

Invoked as:  <envs/<version>/bin/python> py_runner.py <input-file> <k> <k_parse>

subjects/json measures orjson in-process, through core.coreografa_metrics.
Six orjson versions cannot share one interpreter, so here each version runs in
its own venv and this runner reproduces what the in-process harness measures
for json_orjson (subjects/json/user_systems.py), so the numbers mean the same
thing:

  - the system is `for _ in range(K_PARSE): orjson.loads(text)` on the input
    string, with K_PARSE passed in by example.py from the domain's
    user_systems.K_PARSE, so a change there reaches this subject too;
  - runtime_ns is one call of that loop with allocation tracing OFF;
  - memory_peak is the tracemalloc peak over a SEPARATE call, as in
    coreografa_metrics._run_once;
  - an exception anywhere in the loop marks the input rejected (accepted=0)
    and the partial cost is still reported, as the harness does.

Two differences are forced by running out of process. The in-process harness
discards its first sample per input as warm-up within one interpreter; here
each sample is a fresh interpreter, so one untimed call runs first instead.
With k > 1 the reported runtime_ns is the median of k timed calls; example.py
passes k=1 to match the one call per sample the harness makes.

Stdlib plus orjson only, so the per-version venvs need nothing else.
"""
import sys
import time
import tracemalloc
from pathlib import Path
from statistics import median

import orjson

path, k, k_parse = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
text = Path(path).read_text(encoding="utf-8")

rejected = False


def call():
    global rejected
    try:
        for _ in range(k_parse):
            orjson.loads(text)
    except Exception:  # noqa: BLE001 - a rejection, as in _run_once
        rejected = True


call()                                   # warm-up, untimed

times = []
for _ in range(max(1, k)):
    t0 = time.perf_counter_ns()
    call()
    times.append(time.perf_counter_ns() - t0)

tracemalloc.start()
call()
memory_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

print(f"runtime_ns={median(times)} memory_peak={memory_peak} "
      f"accepted={0.0 if rejected else 1.0} version={orjson.__version__}")
