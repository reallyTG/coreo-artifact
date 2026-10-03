from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from core.workflow import WorkflowConfig, run_workflow
import subjects.json.user_def_functions as user_def_functions
from subjects.json.user_systems import (
    json_stdlib,
    json_orjson,
    json_ujson,
    json_simplejson,
)

HERE = Path(__file__).resolve().parent


def workflow(output_dir: Path, quick: bool = False):
    config = WorkflowConfig(
        name="json",
        fan_filepath=HERE / "json.fan",
        udf_module=user_def_functions,
        functions=[json_stdlib, json_orjson, json_ujson, json_simplejson],
        eval_dir=HERE,
        input_type="string",
        # runtime + memory: the C-extension engines (orjson/ujson) vs stdlib/
        # simplejson diverge on both, and big-int / deep-nesting inputs push the
        # gap. In-process subject, so these are the standard timing/tracemalloc.
        metrics=["runtime_ns", "memory_peak"],
        do_requests=not quick,
        # Structural-only grammar; measure kept inputs once-to-
        # significance and cache across rounds.
        use_metric_cache=True,
        # Each measurement parses K times (see user_systems.K_PARSE) to lift the
        # sub-µs parse above clock resolution, so a few tight samples suffice.
        metric_min_n=3, metric_max_n=10,
        # Stratify object breadth so the initial sample spans small..large
        # documents (don't rely on GA diversity). The grammar follows
        # RFC 8259, so the root can be any value, and a band sets the member
        # count of every object in the document, not only the root's.
        # Auto-stratification with alternative pruning
        # instead of one hand-set axis, as for JSONPath.
        stratify_max_repetition=200,
        # Bigger/deeper documents than Fandango's default. The RFC grammar
        # spends a `ws` node in every gap between tokens, so part of the
        # node budget goes to whitespace.
        max_nodes=800,
        # Per-request budget: more solutions + generations per targeted request
        # (in-process parsing is cheap, so we can afford a wide search).
        request_population_size=30,
        request_desired_solutions=15,
        request_max_generations=45,
    )
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / "json")
