"""CSS selector matching: three JavaScript selector engines over one document.

Differential subject within one language. The engines are the ones behind
jsdom and the browsers' polyfills, and nwsapi is present in two releases:

    nwsapi        nwsapi 2.2.27, current release after its 2026 rewrite
    nwsapi_prev   nwsapi 2.2.25, the release before it
    domselector   @asamuzakjp/dom-selector 9.1.4, jsdom 30's engine
    cssselect     css-select 7.0.0 over a parse5 tree, what cheerio assembles

The nwsapi pair makes this subject a differential and a version comparison
at once: the two releases serve as a control that should compare equivalent.

Document parsing is outside the timed region; selector parsing is inside it.

The grammar transcribes Selectors Level 4 §18 on the selector side and a
declared subset of HTML syntax on the document side; its header carries the
deviations table and the per-construct probe behind each omission.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

# Fandango parses seeds and builds derivation trees recursively, and this
# grammar nests documents through <flow_content>. At the default limit the
# loop drops seeds with 'recursion limit hit parsing a seed' and saturates
# after two iterations. 20000 is still too low; generation succeeds at 60000.
sys.setrecursionlimit(60000)

from core.workflow import WorkflowConfig, run_workflow
from core.subprocess_sut import make_subprocess_sut
import subjects.selectors_js.user_def_functions as user_def_functions

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"

K = 30
ENGINES = ("nwsapi", "nwsapi_prev", "domselector", "cssselect")


def _engine(name):
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used"))


SYSTEMS = [_engine(name) for name in ENGINES]


def workflow(output_dir: Path, quick: bool = False):
    config = WorkflowConfig(
        name="selectors_js",
        fan_filepath=HERE / "selectors_js.fan",
        udf_module=user_def_functions,
        functions=SYSTEMS,
        eval_dir=HERE,
        input_type="string",
        # One Node build for all five, so RSS is comparable. Document parsing
        # is excluded from the timed region but not from the process, so RSS
        # carries the jsdom baseline for four of the five; read it as a
        # within-engine signal rather than a ranking.
        metrics=["runtime_ns", "rss"],
        do_requests=not quick,
        use_metric_cache=True,
        metric_min_n=3, metric_max_n=8,
        # Band the document's top-level node count, the axis the selector has
        # to walk. The selector axis grows through requests.
        # Auto-stratification with alternative pruning
        # instead of one hand-set axis, as for JSONPath.
        stratify_max_repetition=200,
        # The joint fit tries 6**features models per system per metric, which is
        # 46,656 at the default cap of six, and that exhausts memory. Four
        # features is 1,296, and single-feature fits still cover every property.
        max_joint_features=4,
        max_generations=40,
        max_nodes=1200,
        # Free repetitions are drawn near-uniformly up to this, so keep
        # exploration moderate and let structural requests do the widening.
        max_repetition=12,
        max_iterations=6,
        # Kept modest: population 30 exhausts memory, since each candidate
        # is a multi-KB document tree.
        request_population_size=20,
        request_desired_solutions=10,
        request_max_generations=30,
        max_requests=8,
    )
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / "selectors_js")
