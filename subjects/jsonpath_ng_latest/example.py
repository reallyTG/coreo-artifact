"""jsonpath-ng, last six releases: a latest-release-series subject.

Comparative subject under rule D6 (eval/latest_series_2026-09-30.json): in
the jsonpath_py domain, jsonpath-ng is the most-downloaded implementation
with at least six releases, and these are its last six non-prerelease
versions by publish date, preregistered before any of them was measured:

    1.5.2  2020-09-07      1.6.1  2024-01-11
    1.5.3  2021-07-05      1.7.0  2024-10-11
    1.6.0  2023-09-13      1.8.0  2026-02-24

Each version has its own venv (build_envs.sh; freeze/ holds each env's pip
freeze). py_runner.py is the jsonpath_py runner's `ng` path.

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
NAME = "jsonpath_ng_latest"

# Oldest to newest; must match build_envs.sh and the preregistration.
VERSIONS = ("1.5.2", "1.5.3", "1.6.0", "1.6.1", "1.7.0", "1.8.0")


def _engine(version):
    name = "jsonpath_ng_" + version.replace(".", "_")
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
