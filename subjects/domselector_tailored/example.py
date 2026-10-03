"""@asamuzakjp/dom-selector 8.2.4 to 9.2.2 on a grammar tailored to the commits' diffs (RQ1, tailored setting).

Same nine releases and the same installs as domselector_known (node_modules is
a symlink to subjects/domselector_known/node_modules). What differs:

- grammar: domselector_tailored.fan, a sub-language of the frozen
  subjects/selectors_js/selectors_js.fan shaped from the diffs of the mined
  pairs (bare unspaced `[name]`, attribute-led compounds with '=' matching,
  child-indexed pseudo-classes, and a wide body: 20 to 2000 sibling elements,
  all carrying a title attribute). The rationale and the rule-by-rule diff
  against the spec grammar are in the .fan header.
- runner: this directory's node_runner.js, the domselector_known runner with
  runtime_ns untouched plus one declared second metric, fresh_ns (median per
  query on a new DOMSelector instance in the warm process: cold engine caches,
  warm JIT). 8.2.5's nthIndexCache fix (#286) is only visible that way.
- metrics: ["runtime_ns", "fresh_ns"].
- exploration: the sibling count (<more_node>) is banded explicitly, five
  narrow log-spaced bands from 20 to 2000 children, instead of auto-
  stratification (whose ceiling, stratify_max_repetition=200, would cap the
  width axis at 200). Narrow bands because Fandango lands on a band's lower
  bound. Generation check: band 700-1999 at the framework's band node budget
  (30,000) produces 701-child, 33 KB documents in about 2 s per input.

Every other WorkflowConfig field comes from the domain subject
(subjects/selectors_js/example.py) via domselector_known.domain_config, as for
the blind subjects. Not blind by construction; reported beside the blind
verdicts. The failure ledger honours SELECTORS_JS_LEDGER.
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
import subjects.domselector_known.example as known

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"
NAME = "domselector_tailored"
VERSIONS = known.VERSIONS

# Sibling-count bands for exploration: (lo, hi) repetitions of <more_node>,
# so 20..2000 children of <body> in total.
SIBLING_BANDS = [(19, 49), (49, 149), (149, 399), (399, 999), (999, 1999)]


def _engine(version):
    name = "domselector_" + version.replace(".", "_")
    # Same K, timeout and suffix as domselector_known, plus fresh_ns.
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=known.domain.K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used", "fresh_ns", "k_fresh"))


SYSTEMS = [_engine(v) for v in VERSIONS]


def _udf():
    spec = importlib.util.spec_from_file_location(
        "domselector_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def config(quick=False):
    return replace(known.domain_config(quick), name=NAME, functions=SYSTEMS,
                   udf_module=_udf(),
                   fan_filepath=HERE / "domselector_tailored.fan", eval_dir=HERE,
                   metrics=["runtime_ns", "fresh_ns"],
                   stratify={"nt": "<more_node>", "bands": SIBLING_BANDS})


def workflow(output_dir: Path, quick: bool = False):
    run_workflow(config(quick), output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
