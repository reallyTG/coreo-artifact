"""nwsapi 2.2.21 to 2.2.27 on a grammar tailored to the commits' diffs (RQ1, tailored setting).

Same seven releases and installs as nwsapi_known (node_modules is a symlink to
subjects/nwsapi_known/node_modules); this directory's node_runner.js is that
runner with only the default failure-ledger path changed. What differs is the
grammar, nwsapi_tailored.fan:

- declared widening toward the specification: CSS escapes (\\61 .. \\64,
  optionally zero-padded) are admitted in the selector half's ids, classes,
  ident attribute values and attribute-value strings. The frozen spec grammar
  excludes escapes by a class-3 vocabulary choice; Selectors-4 allows them.
  Motivation: 2.2.22 (3d8f8d2) removes per-resolver escape normalisation,
  which only escaped selectors reach.
- documents bounded below at 20 top-level subtrees (<more_node>{19,399}), the
  shared larger-document shape of the tailored selector subjects.
- everything else is the spec grammar unchanged. The other nwsapi pairs get no
  tailoring beyond the document shape (measured by hand, their named commits
  show no effect or an inverted one).

Two budget fields differ from the domain subject, both for document width:
- stratify: the top-level node count (<more_node>) is banded explicitly,
  20-50, 50-100, 100-200, 200-400 children of <body>. Auto-stratification
  would band <more_node> only up to the recursive-site ceiling (it produces
  the degenerate bands 19..24 on this grammar), and explicit `stratify`
  replaces auto-stratification, so the selector-side axes (escape and
  identifier lengths) are left to free generation and the targeted loop.
- max_nodes 8000 (domain 1200): the band node budget for a recursive site is
  max(max_nodes, 4000), and at 4000 a 200-child body comes out as about 4 KB
  of bare elements; at 8000 it is about 7 KB with content (about 0.3 s per
  input).
Every other WorkflowConfig field comes from the domain subject via
nwsapi_known.domain_config. Not blind by construction. The failure ledger
honours SELECTORS_JS_LEDGER.
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
import subjects.nwsapi_known.example as known

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"
NAME = "nwsapi_tailored"
VERSIONS = known.VERSIONS

# Top-level node-count bands for exploration: (lo, hi) repetitions of
# <more_node>, so 20..400 children of <body>.
NODE_BANDS = [(19, 49), (49, 99), (99, 199), (199, 399)]


def _engine(version):
    name = "nwsapi_" + version.replace(".", "_")
    # Same K, timeout, suffix and extra metrics as nwsapi_known.
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=known.domain.K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used"))


SYSTEMS = [_engine(v) for v in VERSIONS]


def _udf():
    spec = importlib.util.spec_from_file_location(
        "nwsapi_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def config(quick=False):
    return replace(known.domain_config(quick), name=NAME, functions=SYSTEMS,
                   udf_module=_udf(),
                   fan_filepath=HERE / "nwsapi_tailored.fan", eval_dir=HERE,
                   stratify={"nt": "<more_node>", "bands": NODE_BANDS},
                   max_nodes=8000)


def workflow(output_dir: Path, quick: bool = False):
    run_workflow(config(quick), output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
