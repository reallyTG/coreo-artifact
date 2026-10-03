"""jsonpath-python 1.1.0 to 1.1.3: a known-pair subject in the jsonpath_py domain.

Four systems, jpython_1_1_0 ... jpython_1_1_3. Each version has its own venv
(build_envs.sh; freeze/ holds each env's pip freeze). py_runner.py is the
jsonpath_py runner's `jpython` path.

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
NAME = "jpython_known"

# Oldest to newest; must match build_envs.sh.
VERSIONS = ("1.1.0", "1.1.1", "1.1.2", "1.1.3")


def _engine(version):
    name = "jpython_" + version.replace(".", "_")
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
