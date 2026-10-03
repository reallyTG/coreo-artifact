"""SQL parsing: three JavaScript parsers over one PostgreSQL statement.

Differential subject within one language:

    pgsql       pgsql-ast-parser, nearley, PostgreSQL only
    cst         sql-parser-cst, Peggy, keeps comments and whitespace
    formatter   sql-formatter, nearley; parses and re-prints

None is in OSS-Fuzz and none has a security advisory, but each has
maintainer-accepted slow-parse or hang issues.

node-sql-parser (PEG.js) is left out: it rejects 27 of 100 generated
statements the other three accept, so including it would compare dialect
coverage instead of parsing cost.

sql-formatter also prints, which is more work than parsing alone, so read it
as a third data point rather than a like-for-like ranking.

The grammar transcribes PostgreSQL 18's SELECT synopsis and value-expression
chapter rule by rule; its header lists every departure with a class. It is
not narrowed to the subset all three engines accept: only constructs some
engine rejects outright (>= 95% of probe statements) are left out. On 200 generated statements all three accept 24 (12%): pgsql-ast-parser
rejects 158, sql-parser-cst 76, sql-formatter 0, and pglast (libpg_query 18)
accepts 500 of 500. Disagreeing inputs are dropped per engine pair at scoring
time, so pairs with pgsql-ast-parser are scored on a thin subset.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

# Statements nest through <select> and <expr>, and Fandango parses seeds
# recursively; the default limit drops long seeds mid-run.
sys.setrecursionlimit(60000)

from core.workflow import WorkflowConfig, run_workflow
from core.subprocess_sut import make_subprocess_sut
import subjects.sql_js.user_def_functions as user_def_functions

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "node_runner.js"

K = 30
ENGINES = ("pgsql", "cst", "formatter")


def _engine(name):
    return make_subprocess_sut(name, "node", RUNNER, args=(name,), k=K,
                               timeout=300, input_suffix=".sql",
                               extra_metrics=("nodes", "k_used"))


SYSTEMS = [_engine(name) for name in ENGINES]


def workflow(output_dir: Path, quick: bool = False):
    config = WorkflowConfig(
        name="sql_js",
        fan_filepath=HERE / "sql_js.fan",
        udf_module=user_def_functions,
        functions=SYSTEMS,
        eval_dir=HERE,
        input_type="string",
        metrics=["runtime_ns", "rss"],
        do_requests=not quick,
        use_metric_cache=True,
        metric_min_n=3, metric_max_n=8,
        # Band the select list, the axis every statement has.
        # Auto-stratification with alternative pruning
        # instead of one hand-set axis, as for JSONPath.
        stratify_max_repetition=200,
        # The joint fit tries 6**features models per system per metric, which is
        # 46,656 at the default cap of six, and that exhausts memory. Four
        # features is 1,296, and single-feature fits still cover every property.
        max_joint_features=4,
        max_generations=40,
        max_nodes=1200,
        # Seeding off: Fandango's parser takes over 60s per statement on this
        # grammar, and a request parses its seeds before generating, outside
        # every time budget. Any seed longer than 1 byte is skipped, so
        # requests generate from scratch.
        max_seed_bytes=1,
        max_repetition=10,
        max_iterations=8,
        max_requests=8,
        request_population_size=30,
        request_desired_solutions=15,
        request_max_generations=45,
    )
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / "sql_js")
