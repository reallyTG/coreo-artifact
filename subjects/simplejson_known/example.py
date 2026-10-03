"""simplejson 3.20.2 vs 4.0.0: a known-pair subject in the json domain.

Two systems, simplejson_3_20_2 and simplejson_4_0_0. py_runner.py is
subjects/orjson_latest's runner with orjson.loads replaced by
simplejson.loads, plus a guard that exits if the C speedups
(simplejson._speedups) are missing, so the pair always compares the two C
decoders and never C against simplejson's pure-Python fallback.

subjects/json runs its parsers in-process. One interpreter cannot hold
several builds of one package, so each version has its own venv
(build_envs.sh; freeze/ holds each env's pip freeze) and py_runner.py
reproduces the in-process measurement: the same K_PARSE loop, runtime with
tracing off, memory_peak from a separate traced call, and `accepted`.

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
NAME = "simplejson_known"

# Oldest to newest; must match build_envs.sh.
VERSIONS = ("3.20.2", "4.0.0")


def _engine(version):
    name = "simplejson_" + version.replace(".", "_")
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
