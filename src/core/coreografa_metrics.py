"""Harness-owned metric cache: every (sut, input) metric is a statistical object.

Key design points:
- Module-level cache -> a `sys.modules` singleton, so it PERSISTS across every
  Fandango parse / evolve / request-loop round in one process. A `.fan` metric
  function can `import coreografa_metrics` and share this exact cache. Optional
  disk persistence (save/load) extends it across separate runs.
- Each (sut_name, input_key, metric) maps to a SAMPLE LIST, not a scalar.
- `measure(..., mode="filter")` ensures one cheap sample (for per-candidate
  constraint filtering during generation). `mode="rigorous"` re-executes until a
  relative-precision stopping rule is met (for KEPT inputs / the summary).
- `_EXEC_COUNT` instruments how many times the SUT actually ran.
"""
import json
import math
import time
import tracemalloc
from statistics import mean, median, pstdev, stdev

from scipy import stats

# Process-wide singletons (the whole point: shared across parses/rounds).
# (sut_name, input_key) -> {metric_name: [samples...]}
_CACHE: dict = {}

# Wall-clock cap on sampling ONE input on ONE system.
# Sampling continues until the CI stopping rule is met or this much time has
# passed, whichever comes first, and the input keeps what was measured. Inputs
# that cost milliseconds never reach it. Without it one expensive input can
# hold a run far past its budget, because the run's wall budget is only checked
# between inputs.
MAX_SECONDS_PER_INPUT = 60
_EXEC_COUNT = 0


def reset():
    global _CACHE, _EXEC_COUNT
    _CACHE = {}
    _EXEC_COUNT = 0


def exec_count() -> int:
    return _EXEC_COUNT


def _run_once(input_value, sut_callable, trace_memory=True) -> dict:
    """Execute the SUT, returning one observation of each metric.

    Runtime and memory are measured in SEPARATE executions.
    tracemalloc hooks the allocator and its cost per operation is not constant:
    it rises with the amount of live traced memory, which rises with input size,
    which is the axis every model here is fitted against. Timing under it makes
    cost appear to grow faster with input size than the system's own work does,
    and the inferred complexity class follows the measurement.

    The second execution costs one extra run, so `trace_memory` lets the caller
    skip it. Memory peak is deterministic for a given input where runtime is
    not, so a handful of memory samples is as good as thirty, and the timing
    stopping rule is what actually decides how many samples an input gets.
    Self-reporting SUTs are exempt entirely: their own runner reports both
    numbers, so a second subprocess launch would buy nothing.
    """
    global _EXEC_COUNT

    def fresh():
        # Copy list inputs so an in-place SUT can't mutate them across samples.
        return list(input_value) if isinstance(input_value, list) else input_value

    rejected = False

    def call(arg):
        nonlocal rejected
        try:
            return sut_callable(arg)
        except Exception:
            # A SUT that raises did not process the input either; that is the
            # same early exit as an explicit rejection, and costs the same
            # partial work.
            rejected = True
            return None

    self_reporting = getattr(sut_callable, "self_reporting", False)

    # Timing pass, allocation tracing OFF.
    t0 = time.perf_counter_ns()
    result = call(fresh())
    rt = time.perf_counter_ns() - t0
    _EXEC_COUNT += 1

    # A SUT that REJECTS an input is doing different work from one that
    # processes it, and its cost belongs to a different population. Fitting one
    # model across both is fitting a mixture.
    #
    # Only an explicit `False` counts. A SUT returning None (json) or an empty
    # list is not signalling anything, and `bool([])` must not be read as a
    # rejection.
    if result is False:
        rejected = True

    # Self-reporting SUTs (out-of-process targets that measure themselves)
    # return a metrics dict; trust it. In-process timing is discarded for these,
    # since it would just be subprocess and round-trip overhead.
    if isinstance(result, dict) and result:
        return {k: float(v) for k, v in result.items()}
    # A self-reporting SUT that reported nothing FAILED -- it crashed, timed
    # out, or rejected the input. Falling through would silently record the cost
    # of *launching the failed subprocess* as though it were the system's
    # runtime, which reads as "this system is very slow" and quietly poisons the
    # corpus. Return no observation and let the caller decide how many failures
    # to tolerate.
    if self_reporting:
        return {}

    accepted = 0.0 if rejected else 1.0
    if not trace_memory:
        return {"runtime_ns": rt, "accepted": accepted}

    # Memory pass, allocation tracing ON, on a second execution.
    tracemalloc.start()
    call(fresh())
    mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    _EXEC_COUNT += 1

    return {"runtime_ns": rt, "memory_peak": mem, "accepted": accepted}


def _ci_halfwidth(samples, alpha) -> float:
    """Half-width of the (1-alpha) t confidence interval for the mean."""
    n = len(samples)
    if n < 2:
        return float("inf")
    s = stdev(samples)
    if s == 0:
        return 0.0
    tcrit = stats.t.ppf(1 - alpha / 2, n - 1)
    return tcrit * s / math.sqrt(n)


def _stats(samples_by_metric, warmup, primary_metric):
    out = {}
    for m, raw in samples_by_metric.items():
        eff = raw[warmup:] if len(raw) > warmup else raw
        if not eff:
            continue
        mu = mean(eff)
        hw = _ci_halfwidth(eff, 0.05)
        out[m] = {
            "n": len(eff),
            "mean": mu,
            "median": median(eff),
            "std": stdev(eff) if len(eff) > 1 else 0.0,
            "ci": (mu - hw, mu + hw),
            "rel_margin": (hw / mu) if mu else float("inf"),
            "samples": list(eff),
        }
    return out


def measure(input_value, sut_name, sut_callable, *, key=None,
            mode="rigorous", alpha=0.05, rel_margin=0.05,
            min_n=5, max_n=30, warmup=1, primary_metric="runtime_ns"):
    """Return statistics for running sut_callable on input_value.

    Samples persist in the module cache keyed by (sut_name, key). `key` defaults
    to str(input_value) so the SAME input reuses samples across rounds/runs.

    mode="filter":   ensure >=1 post-warmup sample, return current estimate (cheap).
    mode="rigorous": top up samples until the relative-CI stopping rule on
                     `primary_metric` is met, bounded by max_n.
    """
    if key is None:
        key = str(input_value)
    entry = _CACHE.setdefault((sut_name, key), {})

    def n_primary():
        return len(entry.get(primary_metric, []))

    started = time.time()

    def over_time():
        # Only once something usable exists: the cap bounds refinement, it
        # does not turn a slow input into an unmeasured one.
        return (time.time() - started > MAX_SECONDS_PER_INPUT
                and n_primary() >= 1)

    # A self-reporting SUT that fails returns no observation, so a loop waiting
    # for one would spin forever. Give up on an input after a few consecutive
    # failures and leave it unmeasured for this system.
    MAX_FAILURES = 3
    failures = 0

    # A self-reporting SUT that never emits `primary_metric` leaves n_primary()
    # at zero forever, so the rigorous stopping rule below can never fire and
    # the loop samples endlessly. That is a configuration error, not a flaky
    # measurement, so give up after a couple of confirming samples and say what
    # to fix.
    MAX_MISSING = 2
    missing = 0
    last_keys = ()

    # A censored run reports the affected metric as NaN rather than 0, so it
    # cannot masquerade as a cheap input. Censoring is a property of the input
    # (a solver hitting its ceiling), not measurement noise, so re-running only
    # spends the ceiling again: one such sample is enough.
    MAX_CENSORED = 1
    censored = 0

    # How many traced executions an input gets. Memory peak does not vary
    # between runs of the same deterministic input, so this is about confirming
    # that rather than estimating a mean.
    MEMORY_SAMPLES = 3

    def add_sample():
        nonlocal failures, missing, censored, last_keys
        # Memory is deterministic per input; a few samples settle it, while
        # runtime keeps sampling until its CI rule is met.
        trace = len(entry.get("memory_peak", [])) < MEMORY_SAMPLES
        obs = _run_once(input_value, sut_callable, trace_memory=trace)
        if not obs:
            failures += 1
            return
        failures = 0
        last_keys = tuple(sorted(obs))
        if primary_metric not in obs:
            missing += 1
        elif not math.isfinite(obs[primary_metric]):
            censored += 1
        for m, v in obs.items():
            if not math.isfinite(v):
                continue      # no observation: keep NaN out of means and CIs
            entry.setdefault(m, []).append(v)

    if mode == "filter":
        while (n_primary() < warmup + 1 and failures < MAX_FAILURES
               and censored < MAX_CENSORED and not over_time()):
            add_sample()
    else:  # rigorous
        while (failures < MAX_FAILURES and missing < MAX_MISSING
               and censored < MAX_CENSORED):
            n_eff = max(0, n_primary() - warmup)
            if n_primary() >= warmup + max_n:
                break
            if over_time():
                print(f"[metrics] {sut_name}: {MAX_SECONDS_PER_INPUT}s per-input "
                      f"cap reached after {n_primary()} sample(s); keeping them")
                break
            if n_eff >= min_n:
                eff = entry[primary_metric][warmup:]
                hw = _ci_halfwidth(eff, alpha)
                mu = mean(eff)
                if hw == 0 or (mu > 0 and hw <= rel_margin * mu):
                    break
            add_sample()

    if failures >= MAX_FAILURES and n_primary() == 0:
        print(f"[metrics] {sut_name}: no measurement after {MAX_FAILURES} failed "
              f"attempts; leaving this input unmeasured")
    if censored >= MAX_CENSORED and n_primary() == 0:
        print(f"[metrics] {sut_name}: '{primary_metric}' censored for this "
              f"input; recorded as NaN rather than zero.")
    if missing >= MAX_MISSING:
        print(f"[metrics] {sut_name}: reports {list(last_keys)} but not "
              f"'{primary_metric}', so the stopping rule can never be met. Set "
              f"WorkflowConfig(primary_metric=...) to one of the reported keys.")

    return _stats(entry, warmup, primary_metric)


def save(path):
    serializable = {f"{k[0]}\t{k[1]}": v for k, v in _CACHE.items()}
    with open(path, "w") as f:
        json.dump(serializable, f)


def load(path):
    global _CACHE
    try:
        with open(path) as f:
            raw = json.load(f)
    except FileNotFoundError:
        return
    for k, v in raw.items():
        sut, key = k.split("\t", 1)
        _CACHE[(sut, key)] = v
