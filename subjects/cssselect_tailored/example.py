"""css-select 5.1.0 and 5.2.0 on a grammar tailored to the commit's diff (RQ1, tailored setting).

Same two releases and installs as css_select_known (node_modules is a symlink
to subjects/css_select_known/node_modules); this directory's node_runner.js is
that runner with only the default failure-ledger path changed. The grammar,
cssselect_tailored.fan, is a sub-language of the frozen selectors_js.fan shaped
from #1025 (5.2.0 caches descendant-relative :has() results per subtree): every
complex selector's subject compound carries a :has(), and every <div> nests a
further <div> spine unless it holds non-div content only, so documents are
deep. The header has the rationale and the rule-by-rule diff. Measured by hand,
5.2.0 is the slower release on :has-heavy inputs (#1033 makes compilation
slower and compilation is inside the timed call); the tailored loop reports
what it finds.

One budget field differs from the domain subject, for document depth:
max_nodes 4000 (domain 1200). Depth here is budget-driven (a recursive spine,
not a repetition). At 1200 nodes generated documents reach depth 3-13
(median 5.5); at 4000 they reach 3-15 (median 8), at about 0.2 s per input.
Every other WorkflowConfig field, including auto-stratification, comes from
the domain subject via css_select_known.domain_config. Not blind by
construction. The failure ledger honours SELECTORS_JS_LEDGER.
"""
from dataclasses import replace
from pathlib import Path
import importlib.util
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from core.subprocess_sut import make_subprocess_sut
from core.workflow import run_workflow
import subjects.css_select_known.example as known

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"
NAME = "cssselect_tailored"
VERSIONS = known.VERSIONS


def _engine(version):
    name = "css_select_" + version.replace(".", "_")
    # Same K, timeout, suffix and extra metrics as css_select_known.
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=known.domain.K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used"))


SYSTEMS = [_engine(v) for v in VERSIONS]


def _udf():
    spec = importlib.util.spec_from_file_location(
        "cssselect_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def config(quick=False):
    return replace(known.domain_config(quick), name=NAME, functions=SYSTEMS,
                   udf_module=_udf(),
                   fan_filepath=HERE / "cssselect_tailored.fan", eval_dir=HERE,
                   max_nodes=4000)


def workflow(output_dir: Path, quick: bool = False):
    run_workflow(config(quick), output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
