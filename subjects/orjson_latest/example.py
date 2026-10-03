"""orjson, last six releases: a latest-release-series subject.

Comparative subject under rule D6 (eval/latest_series_2026-09-30.json): in
the json domain (stdlib excluded), orjson is the most-downloaded
implementation with at least six releases, and these are its last six
non-prerelease versions by publish date, preregistered before any of them was
measured:

    3.11.5  2025-12-06      3.11.8  2026-03-31
    3.11.6  2026-01-29      3.11.9  2026-05-06
    3.11.7  2026-02-02      3.12.0  2026-08-14

subjects/json runs its parsers in-process. One interpreter cannot hold six
orjson builds, so each version has its own venv (build_envs.sh; freeze/ holds
each env's pip freeze) and py_runner.py reproduces the in-process measurement
for json_orjson: the same K_PARSE loop, runtime with tracing off, memory_peak
from a separate traced call, and `accepted`. See py_runner.py for the two
differences running out of process forces.

Everything except the systems comes from the domain subject at run time: the
grammar, the properties and the whole WorkflowConfig are taken from
subjects/json/example.py by calling its workflow() with run_workflow
intercepted, so the domain's frozen grammar and budget apply here unchanged.
eval_dir stays the domain directory, because the framework reads
<eval_dir>/user_def_functions.py as source text.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from dataclasses import replace

from core.subprocess_sut import make_subprocess_sut
from core.workflow import run_workflow
import subjects.json.example as domain
from subjects.json.user_systems import K_PARSE

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "py_runner.py"
NAME = "orjson_latest"

# Oldest to newest; must match build_envs.sh and the preregistration.
VERSIONS = ("3.11.5", "3.11.6", "3.11.7", "3.11.8", "3.11.9", "3.12.0")


def _engine(version):
    name = "orjson_" + version.replace(".", "_")
    # k=1: one timed call of the K_PARSE loop per sample, as the in-process
    # harness makes. The timeout only fires on a pathological input.
    return make_subprocess_sut(name, HERE / "envs" / version / "bin" / "python",
                               RUNNER, args=(K_PARSE,), k=1, timeout=300,
                               input_suffix=".json",
                               wanted=("runtime_ns", "memory_peak", "accepted"))


SYSTEMS = [_engine(v) for v in VERSIONS]


def domain_config(quick=False):
    """The domain subject's WorkflowConfig, captured without running it."""
    captured = {}
    original = domain.run_workflow
    domain.run_workflow = lambda config, output_dir: captured.setdefault("c", config)
    try:
        domain.workflow(REPO_ROOT / "output" / NAME, quick=quick)
    finally:
        domain.run_workflow = original
    return captured["c"]


def workflow(output_dir: Path, quick: bool = False):
    config = replace(domain_config(quick), name=NAME, functions=SYSTEMS)
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
