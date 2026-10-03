"""Out-of-process, self-measuring systems under test.

Run a SUT in its own process —
a different interpreter / venv / version / language — that measures itself and
prints `key=value` metric lines on stdout. The returned callable is a normal
SUT for the harness; because it returns a metrics dict, coreografa_metrics uses
those self-reported values instead of timing it in-process (see _run_once).

This is how we compare two versions of the same package that can't coexist in
one process, and the path toward non-Python targets.
"""
import os
import subprocess
import tempfile

from core.bench_runner import STANDARD_METRICS


def make_subprocess_sut(name, exe, script=None, args=(), k=1, timeout=180,
                        wanted=None, extra_metrics=(), input_suffix=".txt"):
    """Return a SUT callable that runs `exe [script] <input-file> k *args`.

    `exe` is any executable: a Python interpreter, `node`, or a compiled
    runner. `script` is the interpreter's script argument and is omitted
    entirely when None, which is what a compiled target wants — it receives
    the input path as its own first argument.

    The runner is expected to print metric lines like `runtime_ns=123 rss=456`
    (a core.bench_runner-based runner prints all of STANDARD_METRICS). The
    callable writes the input to a temp file, runs the runner, parses the
    metrics, and returns the subset in `wanted`.

    `wanted` defaults to STANDARD_METRICS, so any bench_runner-based subject
    captures every framework metric with no extra config. Pass `extra_metrics`
    to also capture case-study-specific keys a runner emits (e.g. output_bytes)
    without having to restate the standard set. Non-numeric tokens (e.g.
    `version=63.0`) simply aren't in the allowlist and are ignored.
    """
    exe = str(exe)
    prefix = [exe] if script is None else [exe, str(script)]
    wanted = set(wanted if wanted is not None else STANDARD_METRICS) | set(extra_metrics)

    def sut(input_value):
        with tempfile.NamedTemporaryFile("w", suffix=input_suffix,
                                         delete=False, encoding="utf-8") as f:
            f.write(str(input_value))
            path = f.name
        try:
            proc = subprocess.run(
                [*prefix, path, str(k), *map(str, args)],
                capture_output=True, text=True, timeout=timeout)
            metrics = {}
            for line in proc.stdout.splitlines():
                for tok in line.split():
                    if "=" in tok:
                        key, _, val = tok.partition("=")
                        if key in wanted:
                            try:
                                metrics[key] = float(val)
                            except ValueError:
                                pass
            return metrics
        except subprocess.TimeoutExpired:
            return {}
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass

    sut.__name__ = name
    # Tells coreografa_metrics that an empty return means "this run failed",
    # not "measure it in-process instead". Without it, a crashed or
    # timed-out runner is silently recorded as a very slow system.
    sut.self_reporting = True
    return sut
