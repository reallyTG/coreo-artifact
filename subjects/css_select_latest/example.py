"""css-select, last six releases: a latest-release-series subject.

Comparative subject under rule D6 (eval/latest_series_2026-09-30.json): in
the selectors_js domain, css-select is the most-downloaded implementation
with at least six releases, and these are its last six non-prerelease
versions by publish date, preregistered before any of them was measured:

    5.1.0  2022-04-27      5.2.2  2025-06-28
    5.2.0  2025-06-28      6.0.0  2025-06-29
    5.2.1  2025-06-28      7.0.0  2026-03-22

5.2.1 is a broken publish: its registry tarball holds 19 files against 108
for 5.2.0 and 116 for 5.2.2, lib/index.js requires ./compile.js which is not
in it, and require('css-select@5.2.1') throws MODULE_NOT_FOUND. It cannot
return a result on any input, so it is listed in VERSIONS (the
preregistration is unchanged) but left out of SYSTEMS by BROKEN below, which
leaves five systems and the pairs 5.2.0->5.2.2 in place of 5.2.0->5.2.1 and
5.2.1->5.2.2. Emptying BROKEN restores all six.

All six are installed side by side under npm aliases (package.json); parse5
and parse5-htmlparser2-tree-adapter are pinned to subjects/selectors_js, and
7.0.0's own dependencies resolve to the same versions as there. The runner is
the selectors_js runner's `cssselect` path, with the engine name choosing the
version.

Everything except the systems comes from the domain subject at run time: the
grammar, the properties and the whole WorkflowConfig are taken from
subjects/selectors_js/example.py by calling its workflow() with run_workflow
intercepted, so the domain's frozen grammar and budget apply here unchanged.
eval_dir stays the domain directory, because the framework reads
<eval_dir>/user_def_functions.py as source text. Importing the domain module
also applies its sys.setrecursionlimit(60000), which its grammar needs.
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
NAME = "css_select_latest"

# Oldest to newest; must match package.json aliases and the preregistration.
VERSIONS = ("5.1.0", "5.2.0", "5.2.1", "5.2.2", "6.0.0", "7.0.0")
BROKEN = {"5.2.1": "registry tarball lacks lib/compile.js; require() throws"}


def _engine(version):
    name = "css_select_" + version.replace(".", "_")
    # Same K, timeout, suffix and extra metrics as the domain's engines.
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=domain.K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used"))


SYSTEMS = [_engine(v) for v in VERSIONS if v not in BROKEN]


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
