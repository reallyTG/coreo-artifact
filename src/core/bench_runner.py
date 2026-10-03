"""Framework-side measurement for out-of-process, self-measuring SUTs.

A subprocess SUT (see core/subprocess_sut) runs a target K times in its own
process and prints `key=value` metric lines on stdout; coreografa_metrics then
trusts those self-reported values instead of timing in-process. This module owns
that measurement so individual runners don't reimplement it: a case-study runner
supplies only *what* to run (a zero-arg callable) and reads its own input, and
`report` computes runtime, memory, OS resource usage, and the RSS trajectory
(the memory-leak signal) and prints the standard line.

Why the K loop lives in the runner and not here: a memory leak only accumulates
*within one process*, so the repetition must happen inside a single interpreter.
Everything around the loop, though, is generic and belongs to the framework.

Stdlib only, so version-isolated venvs can import it with nothing installed. The
stdout `key=value` protocol is the contract between a runner and the harness;
this helper is the convenience path for Python runners. Case-study-specific, artifact-shaped metrics (e.g. output byte size,
page count) are passed in via `extra_fn` rather than baked in here.
"""
import resource
import time
import tracemalloc
from statistics import median, pstdev

# The metrics `report` always emits. subprocess_sut captures these by default,
# so adding one here makes it flow to the corpus for every subprocess subject
# without touching any case study. config.metrics then selects which to use.
STANDARD_METRICS = (
    "runtime_ns",         # median per-call wall time
    "runtime_spread_ns",  # population stdev of per-call time (instability)
    "tracemalloc_peak",   # peak Python-level allocation (misses C-level leaks)
    "rss",                # peak resident set at end (OS high-water mark)
    "rss_growth",         # RSS(last) - RSS(first): leak magnitude over K calls
    "rss_slope",          # least-squares RSS growth per call (leak rate)
    "utime_ns",           # user CPU time over the K calls
    "stime_ns",           # system CPU time (syscall/allocation heavy paths)
    "minflt",             # minor page faults (memory-churn proxy)
    "majflt",             # major page faults (swap pressure)
)


def _maxrss():
    # ru_maxrss is a *peak-over-lifetime* high-water mark, not current RSS
    # (getrusage exposes no current-RSS field). Units differ by OS: bytes on
    # macOS, kilobytes on Linux. Callers compare within a subject, so the unit
    # is consistent per run; we do not normalize it here.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def _slope(ys):
    """Least-squares slope of ys against index 0..n-1 (0.0 if <2 points)."""
    n = len(ys)
    if n < 2:
        return 0.0
    xbar = (n - 1) / 2.0
    ybar = sum(ys) / n
    num = sum((i - xbar) * (y - ybar) for i, y in enumerate(ys))
    den = sum((i - xbar) ** 2 for i in range(n))
    return num / den if den else 0.0


def run(callable_once, k=1, warmup=1):
    """Run `callable_once` k times (after `warmup` discarded calls) and return a
    dict of the STANDARD_METRICS. The callable takes no args and its return
    value is ignored — it exists purely to be measured."""
    for _ in range(warmup):
        callable_once()  # pay one-time init so it doesn't skew the measured K

    # Baseline resource counters *after* warm-up, so deltas cover only the K
    # measured calls (not import/init costs).
    ru0 = resource.getrusage(resource.RUSAGE_SELF)
    times = []
    rss_trace = []
    # Timed calls run WITHOUT tracemalloc. It hooks the allocator at a cost
    # that grows with allocations, so timing under it measures allocation
    # volume as much as work: it hid jsonpath-python 1.1.1's 1.25-1.35x gain
    # (measured 1.00x) and invented a 1.2x python-jsonpath 2.0.0 gain. The
    # in-process path separates the two for the same reason
    # (coreografa_metrics._run_once). tracemalloc's own bookkeeping also
    # inflates rss/rss_growth, measured here too.
    for _ in range(k):
        t = time.perf_counter_ns()
        callable_once()
        times.append(time.perf_counter_ns() - t)
        rss_trace.append(_maxrss())
    ru1 = resource.getrusage(resource.RUSAGE_SELF)
    # Allocation peak from one separate, traced call.
    tracemalloc.start()
    callable_once()
    tm_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return {
        "runtime_ns": median(sorted(times)),
        "runtime_spread_ns": pstdev(times) if len(times) > 1 else 0.0,
        "tracemalloc_peak": tm_peak,
        "rss": rss_trace[-1],
        "rss_growth": rss_trace[-1] - rss_trace[0],
        "rss_slope": _slope(rss_trace),
        "utime_ns": int((ru1.ru_utime - ru0.ru_utime) * 1e9),
        "stime_ns": int((ru1.ru_stime - ru0.ru_stime) * 1e9),
        "minflt": ru1.ru_minflt - ru0.ru_minflt,
        "majflt": ru1.ru_majflt - ru0.ru_majflt,
    }


def report(callable_once, k=1, warmup=1, extra_fn=None):
    """Measure and print the standard `key=value` metric line on stdout.

    `extra_fn`, if given, is called *after* the run and its dict is merged in —
    use it for case-study-specific metrics that depend on side effects of the
    run (e.g. the size of an output file the callable produced)."""
    metrics = run(callable_once, k=k, warmup=warmup)
    if extra_fn is not None:
        metrics.update(extra_fn())
    print(" ".join(f"{key}={val}" for key, val in metrics.items()))
    return metrics
