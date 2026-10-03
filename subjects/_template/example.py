"""Skeleton subject. Copy this directory, rename it, fill in the TODOs.

    cp -r subjects/_template subjects/mysubject

Directories starting with "_" are skipped by run.py's discovery, so this
template never shows up as a runnable subject. Once copied and renamed, the new
directory is picked up automatically — there is no registry to edit.

A subject is four real artifacts plus this config:

    <name>.fan              the input language (grammar + any constraints)
    user_def_functions.py   input properties, the model's features
    the systems under test  callables, or runners invoked out of process
    example.py              this file: wires them together

See docs/adding-a-subject.md for the full walkthrough.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from core.workflow import WorkflowConfig, run_workflow
import subjects._template.user_def_functions as user_def_functions  # TODO rename

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Systems under test.
#
# Two or more implementations that compute the same thing, so that a difference
# in cost is a property of the implementation rather than of the task. Either:
#
#   * in-process — plain Python callables taking one input, fastest to set up;
#   * out-of-process — another language, another version, or another binary:
#
#       from core.subprocess_sut import make_subprocess_sut
#       sut = make_subprocess_sut("name", "node", HERE / "runner.js", k=20)
#
#     Pass script=None for a compiled binary, which takes the input path as its
#     own first argument. See subjects/jsonpath_js (Node)
#     and subjects/orjson_known (one Python virtualenv per version).
# ---------------------------------------------------------------------------

def system_a(input_value):
    """TODO: replace with the real system under test."""
    return sum(len(str(input_value).split(",")) for _ in range(1))


def system_b(input_value):
    """TODO: a second implementation of the same computation."""
    return len(str(input_value).split(","))


def workflow(output_dir: Path, quick: bool = False):
    config = WorkflowConfig(
        name="_template",                      # TODO rename
        fan_filepath=HERE / "template.fan",    # TODO rename
        udf_module=user_def_functions,
        functions=[system_a, system_b],
        eval_dir=HERE,
        # "string" passes the derivation tree through; "int_array" parses the
        # input as a comma-separated integer list first.
        input_type="string",
        # Which measured columns get modelled and targeted. Out-of-process
        # runners report their own metric names; see core/bench_runner.py for
        # the standard set.
        metrics=["runtime_ns", "memory_peak"],
        do_requests=not quick,
        # Measure kept inputs once-to-significance, caching across runs.
        use_metric_cache=True,
        metric_min_n=3, metric_max_n=10,
        # Band a grammar repetition so the first sample spans the size axis
        # instead of clustering wherever the search happens to settle. Name a
        # non-terminal that appears as <nt>{lo,hi} in the grammar.
        stratify={"nt": "<item>", "bands": [(0, 5), (5, 15), (15, 30), (30, 50)]},
        max_generations=40,
        max_nodes=600,
        max_requests=8,
        request_population_size=20,
        request_desired_solutions=10,
        request_max_generations=30,
    )
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / "_template")
