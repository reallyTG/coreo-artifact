"""jsonpath-plus, last six releases: a latest-release-series subject.

Comparative subject under rule D6 (eval/latest_series_2026-09-30.json): in
the jsonpath_js domain, jsonpath-plus is the most-downloaded implementation
with at least six releases, and these are its last six non-prerelease
versions by publish date, preregistered before any of them was measured:

    10.2.0  2024-11-17      11.0.0  2026-09-24
    10.3.0  2025-02-14      11.0.1  2026-09-25
    10.4.0  2026-02-16      11.1.0  2026-09-25

All six are installed side by side under npm aliases (package.json), with jsep
and its plugins resolving to the same versions as subjects/jsonpath_js.

Everything except the systems comes from the domain subject at run time: the
grammar, the properties and the whole WorkflowConfig are taken from
subjects/jsonpath_js/example.py by calling its workflow() with run_workflow
intercepted, so the domain's frozen grammar and budget apply here unchanged.
eval_dir stays the domain directory, because the framework reads
<eval_dir>/user_def_functions.py as source text. The runner is the
jsonpath_js runner's `plus` path, with the engine name choosing the version.

11.0.0 replaced the public JSONPath.cache object with internal Maps and a
JSONPath.clearCache() method; the runner resets whichever the version has, so
query parsing is inside the timed region for all six. See node_runner.js.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from dataclasses import replace

from core.subprocess_sut import make_subprocess_sut
from core.workflow import run_workflow
import subjects.jsonpath_js.example as domain

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"
NAME = "jsonpath_plus_latest"

# Oldest to newest; must match package.json aliases and the preregistration.
VERSIONS = ("10.2.0", "10.3.0", "10.4.0", "11.0.0", "11.0.1", "11.1.0")


def _engine(version):
    name = "jsonpath_plus_" + version.replace(".", "_")
    # Same K, timeout, suffix and extra metrics as the domain's engines.
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=domain.K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used"))


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
