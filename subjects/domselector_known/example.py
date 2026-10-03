"""@asamuzakjp/dom-selector 8.2.4 to 9.2.2: a known-pair subject.

Nine @asamuzakjp/dom-selector releases in the selectors_js domain, installed
side by side under npm aliases (package.json) with jsdom pinned to the
domain's 30.1.0. The transitive tree resolves to the same versions as
subjects/selectors_js, with one exception: 9.2.1 and 9.2.2 require
lru-cache ^11.5.3, so each gets a nested 11.5.3 while the root stays at the
domain's 11.5.2. All nine export the same class API, new DOMSelector(window),
so the runner is the selectors_js runner's `domselector` path unchanged apart
from the engine name choosing the version.

Everything except the systems comes from the domain subject at run time: the
grammar, the properties and the whole WorkflowConfig are taken from
subjects/selectors_js/example.py by calling its workflow() with run_workflow
intercepted, so the domain's frozen grammar and budget apply here unchanged.
eval_dir stays the domain directory, because the framework reads
<eval_dir>/user_def_functions.py as source text. Importing the domain module
also applies its sys.setrecursionlimit(60000), which its grammar needs. The
failure ledger honours the domain's SELECTORS_JS_LEDGER override.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from dataclasses import replace

from core.subprocess_sut import make_subprocess_sut
from core.workflow import run_workflow
import subjects.selectors_js.example as domain

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"
NAME = "domselector_known"

# Oldest to newest; must match the package.json aliases.
VERSIONS = ('8.2.4', '8.2.5', '9.0.3', '9.0.4', '9.1.0', '9.1.1', '9.1.2', '9.2.1', '9.2.2')


def _engine(version):
    name = "domselector_" + version.replace(".", "_")
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
