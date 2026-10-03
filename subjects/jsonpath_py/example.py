"""JSONPath evaluation: four independent Python implementations.

Differential subject within one language, the Python half of the JSONPath
domain:

    ng          jsonpath-ng 1.8.0, ~12.7M downloads/week, PLY-based parser
    pyjsonpath  python-jsonpath 2.2.1, RFC 9535 plus extensions
    rfc9535     jsonpath-rfc9535 1.0.0, RFC 9535, runs the compliance suite
    jpython     jsonpath-python 1.1.6

None of the four is in OSS-Fuzz and none has a performance advisory on record.

Each library gets its own virtualenv under envs/, because python-jsonpath and
jsonpath-python both provide a module named `jsonpath`. The runner compiles
the query outside the timed region and reports compile time separately; see
py_runner.py for why.

The grammar transcribes RFC 9535 (queries) and RFC 8259 under I-JSON
(documents); jsonpath_py.fan's header lists every departure with its class.
jsonpath-ng does not implement much of RFC 9535 filter syntax (`&&`, `||`,
`!`, function extensions, path-to-path comparison) and fails on most generated
inputs; it is kept in and flagged rather than letting it narrow the grammar.
jsonpath-python returns no match for some filters the RFC engines match, and
jsonpath-ng applies slices to an object's values. The runner emits `hits`;
the harness filters disagreeing inputs per engine pair at scoring time, so
check `hits` in metrics_cache.json before quoting a ratio.
"""
from pathlib import Path
import sys

# The RFC 9535 grammar recurses through filters, function arguments and
# nested JSON values; Fandango walks trees recursively.
sys.setrecursionlimit(60000)

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from core.workflow import WorkflowConfig, run_workflow
from core.subprocess_sut import make_subprocess_sut
import subjects.jsonpath_py.user_def_functions as user_def_functions

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "py_runner.py"

# Python process startup is ~30ms, so K stays modest and the sample count low:
# each sample is another interpreter launch.
K = 30
ENGINES = ("ng", "pyjsonpath", "rfc9535", "jpython")


def _engine(name):
    return make_subprocess_sut(name, HERE / "envs" / name / "bin" / "python",
                               RUNNER, args=(name,), k=K, timeout=300,
                               input_suffix=".txt",
                               extra_metrics=("hits", "k_used", "compile_ns"))


SYSTEMS = [_engine(name) for name in ENGINES]


def workflow(output_dir: Path, quick: bool = False):
    config = WorkflowConfig(
        name="jsonpath_py",
        fan_filepath=HERE / "jsonpath_py.fan",
        udf_module=user_def_functions,
        functions=SYSTEMS,
        eval_dir=HERE,
        input_type="string",
        # Runtime only. The four run in separate interpreters with different
        # import sets, so RSS would mostly rank their module footprints.
        metrics=["runtime_ns"],
        do_requests=not quick,
        use_metric_cache=True,
        metric_min_n=3, metric_max_n=6,
        # Auto-stratification instead of one hand-set axis:
        # banding <segment> alone never varies the document (median 7 bytes,
        # zero object keys). Bands for non-recursive sites reach 200; recursive
        # ones stop at grammar_props.RECURSIVE_CEILING.
        stratify_max_repetition=200,
        max_generations=40,
        max_nodes=800,
        max_repetition=10,
        max_iterations=8,
        max_requests=8,
        request_population_size=20,
        request_desired_solutions=10,
        request_max_generations=30,
    )
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / "jsonpath_py")
