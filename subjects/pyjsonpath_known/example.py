"""python-jsonpath 1.3.2 vs 2.0.0: a known-pair subject in the jsonpath_py domain.

Two systems, pyjsonpath_1_3_2 and pyjsonpath_2_0_0. Each version has its own
venv (build_envs.sh; freeze/ holds each env's pip freeze). py_runner.py is
the jsonpath_py runner's `pyjsonpath` path; it describes the API and
behaviour differences between the 1.x and 2.x lines.

Everything except the systems comes from the domain subject at run time: the
grammar, the properties and the whole WorkflowConfig are taken from
subjects/jsonpath_py/example.py by calling its workflow() with run_workflow
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
import subjects.jsonpath_py.example as domain

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "py_runner.py"
NAME = "pyjsonpath_known"

# Oldest to newest; must match build_envs.sh.
VERSIONS = ("1.3.2", "2.0.0")


def _engine(version):
    name = "pyjsonpath_" + version.replace(".", "_")
    # Same K, timeout, suffix and extra metrics as the domain's engines.
    return make_subprocess_sut(name, HERE / "envs" / version / "bin" / "python",
                               RUNNER, k=domain.K, timeout=300,
                               input_suffix=".txt",
                               extra_metrics=("hits", "k_used", "compile_ns"))


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
