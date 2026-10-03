"""simplejson runner for the simplejson known-pair subject.

Invoked as:  <envs/<version>/bin/python> py_runner.py <input-file> <k> <k_parse>

A copy of subjects/orjson_latest/py_runner.py with orjson.loads replaced by
simplejson.loads; everything that decides what is observed is unchanged (the
K_PARSE loop over the input string, runtime_ns from an untraced call,
memory_peak from a separate traced call, `accepted`, one untimed warm-up
call). See that file for the out-of-process differences from the in-process
json_simplejson system in subjects/json/user_systems.py.

simplejson falls back to pure Python silently when its C extension is
missing, which would turn a version comparison into a C-versus-Python one.
The runner therefore imports simplejson._speedups explicitly and exits with
status 2 if it is absent, and checks that the decoder actually uses the C
scanner.

Stdlib plus simplejson only, so the per-version venvs need nothing else.
"""
import sys
import time
import tracemalloc
from pathlib import Path
from statistics import median

import simplejson
try:
    import simplejson._speedups  # noqa: F401
except ImportError as exc:
    print(f"simplejson C speedups missing: {exc}", file=sys.stderr)
    sys.exit(2)
if simplejson.scanner.c_make_scanner is None:
    print("simplejson decoder is not using the C scanner", file=sys.stderr)
    sys.exit(2)

path, k, k_parse = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
text = Path(path).read_text(encoding="utf-8")

rejected = False


def call():
    global rejected
    try:
        for _ in range(k_parse):
            simplejson.loads(text)
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
      f"accepted={0.0 if rejected else 1.0} version={simplejson.__version__}")
