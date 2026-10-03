"""JSONPath evaluation: five independent JavaScript implementations.

Differential subject within one language. All five answer the same question, which
nodes of this document this query selects, on one Node build, so a cost
difference belongs to the implementation and not to the runtime:

    plus        jsonpath-plus     Goessner dialect, own safe JS evaluator
    dchester    jsonpath          Goessner dialect, static-eval filters
    jsonpathly  jsonpathly        claims RFC 9535
    rfc9535     jsonpath-rfc9535  RFC 9535, passes the compliance suite
    p3          json-p3           RFC 9535, runs the compliance suite

None of the five is in OSS-Fuzz, and none has a performance advisory on record.

The grammar transcribes RFC 9535 (queries) and RFC 8259 under I-JSON
(documents); jsonpath_js.fan's header lists every departure with its class.
The Goessner-dialect engines (jsonpath-plus, jsonpath) reject or silently
mis-evaluate part of that language, so result counts do not agree on every
input: the runner emits `hits`, and the harness filters disagreeing inputs per
engine pair at scoring time. Check `hits` before quoting a ratio.
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
import subjects.jsonpath_js.user_def_functions as user_def_functions

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"

K = 50
ENGINES = ("plus", "dchester", "jsonpathly", "rfc9535", "p3")


def _engine(name):
    # The runner caps its own repetitions at a 5s budget, so the timeout only
    # fires when a single call runs past it.
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=K,
                               timeout=300, input_suffix=".txt",
                               extra_metrics=("hits", "k_used"))


SYSTEMS = [_engine(name) for name in ENGINES]


def workflow(output_dir: Path, quick: bool = False):
    config = WorkflowConfig(
        name="jsonpath_js",
        fan_filepath=HERE / "jsonpath_js.fan",
        udf_module=user_def_functions,
        functions=SYSTEMS,
        eval_dir=HERE,
        input_type="string",
        # All five share one Node process model, so RSS is comparable, and a
        # query whose result set explodes shows there before it shows in time.
        metrics=["runtime_ns", "rss"],
        do_requests=not quick,
        use_metric_cache=True,
        metric_min_n=3, metric_max_n=8,
        # Auto-stratification instead of one hand-set axis:
        # banding <segment> alone never varies the document (median 7 bytes,
        # zero object keys). Bands for non-recursive sites reach 200; recursive
        # ones stop at grammar_props.RECURSIVE_CEILING.
        stratify_max_repetition=200,
        max_generations=40,
        max_nodes=800,
        # Every size in the grammar is a free `*` or `+`, and Fandango draws a
        # repetition count close to uniformly up to this cap. At the default
        # 200 nearly every generated query names a key no document has and
        # selects nothing. Exploration starts small; growth past the cap is
        # the request loop's job, through structural rewrites of the specific
        # repetition a property depends on.
        max_repetition=10,
        # Frontier expansion roughly doubles a count per iteration, so reaching
        # thousands of elements from tens takes more than the default 5.
        max_iterations=10,
        max_requests=8,
        request_population_size=20,
        request_desired_solutions=10,
        request_max_generations=30,
    )
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / "jsonpath_js")
