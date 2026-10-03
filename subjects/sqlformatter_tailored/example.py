"""sql-formatter 15.8.2 and 15.9.0 on a grammar tailored to the commit's diff (RQ1, tailored setting).

The commit is 6c21ff5 (PR #963), the fix for quadratic expression lists.

Systems: the same two installed versions and the same runner as
sql_formatter_latest, by path (subjects/sql_formatter_latest/node_runner.js;
node resolves the `sql_formatter_<v>` aliases from that file's own directory),
so the SUT names are sql_formatter_15_8_2 and sql_formatter_15_9_0 there too.
Measurement, K, timeout and every budget field come from the domain config
(subjects/sql_js/example.py, captured through sql_formatter_latest's
domain_config()), unchanged except what the tailoring needs:

  fan_filepath / udf_module / eval_dir   the tailored grammar and its properties
  stratify     one axis, the flat list's repetition <more_el>, in six bands.
               The spec budget (max_repetition=10, max_nodes=1200) keeps lists
               under ~90 items, where the two versions differ by under 1.05x;
               the fix's effect is 1.16x at 300, 2.08x at 1,000, 4.0x at 3,000.
               The top band stays at 3,000: 15.8.2 runs out of heap in-process
               near 10,000 items (issue #840). Fandango lands near a band's
               lower bound once the node budget binds, so six narrow bands.
               Measured landing (20 inputs per band): 52-96,
               158-248, 304-484, 637-800, 1201, 2401 items.
  max_nodes    30,000 (spec: 1200), the framework's ceiling
               (core.targeting.MAX_STRUCTURAL_NODES). The per-band budget the
               framework derives for this grammar is 4,000, at which every
               band from 400 up lands exactly on its lower bound, operands
               shrink to one character and no IN-list statement is drawn.
               At 30,000 the bands up to 900 spread and both statement kinds
               appear up to 1,200; the 2,400 band is still budget-bound
               (select lists of 2,401 short operands only).

Any pair this subject detects counts as detected after tailoring, not blind.
"""
from dataclasses import replace
from pathlib import Path
import importlib.util
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer

from core.workflow import run_workflow
import subjects.sql_formatter_latest.example as latest

HERE = Path(__file__).resolve().parent
NAME = "sqlformatter_tailored"

# The pair under study, oldest first; engines exactly as sql_formatter_latest builds them.
VERSIONS = ("15.8.2", "15.9.0")
SYSTEMS = [latest._engine(v) for v in VERSIONS]

STRATIFY = {"nt": "<more_el>",
            "bands": [(50, 100), (150, 250), (300, 500), (600, 900),
                      (1200, 1800), (2400, 3000)]}


def _udf():
    spec = importlib.util.spec_from_file_location(
        "sqlformatter_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def workflow(output_dir: Path, quick: bool = False):
    config = replace(latest.domain_config(quick), name=NAME, functions=SYSTEMS,
                     fan_filepath=HERE / "sqlformatter_tailored.fan",
                     udf_module=_udf(), eval_dir=HERE, stratify=STRATIFY,
                     max_nodes=30000)
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
