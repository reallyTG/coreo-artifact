"""jsonpath-python 1.1.0 to 1.1.3 on a grammar tailored to the commits' diffs (RQ1, tailored setting).

Same four systems, runner and budget as jpython_known (its envs and
py_runner.py, by path through subjects.jpython_known.example.SYSTEMS). Only the
grammar and the properties differ: jpython_tailored.fan is a sub-language of the
frozen jsonpath_py.fan shaped from the three commits' diffs (rationale in its
header), and user_def_functions.py adds `n_object_keys` and `max_value_bytes`.

Stratification. The grammar renames the two repetitions the commits care
about so they can be banded explicitly: `<wide_more_member>` (root object width,
per-key cost of 61152d7 and 3054ca4) and `<more_leaf>` (length of the arrays
under root keys, i.e. the size of each matched value, cost of 70b0103).
Fandango lands on a band's lower bound, so each axis gets three bands; the
product is nine strata. The lowest <more_leaf> band starts at 0, so it is not
forced through and keeps leaf and small-object values in the mix. Explicit
`stratify` takes precedence over auto-stratification in core/workflow.py;
auto_stratify is also set False so the choice is visible here.

Any pair this subject detects counts as detected after tailoring, not blind.
"""
from dataclasses import replace
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

import importlib.util

from core.workflow import run_workflow
import subjects.jpython_known.example as known

HERE = Path(__file__).resolve().parent
NAME = "jpython_tailored"
FAN = HERE / "jpython_tailored.fan"

STRATIFY = [
    {"nt": "<wide_more_member>", "bands": [(1, 10), (30, 80), (150, 300)]},
    {"nt": "<more_leaf>", "bands": [(0, 3), (10, 30), (60, 120)]},
]


def _udf():
    spec = importlib.util.spec_from_file_location(
        "jpython_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def workflow(output_dir: Path, quick: bool = False):
    # Budget fields come unchanged from the domain config via jpython_known.
    config = replace(known.domain_config(quick), name=NAME,
                     functions=known.SYSTEMS, udf_module=_udf(),
                     fan_filepath=FAN, eval_dir=HERE,
                     stratify=STRATIFY, auto_stratify=False,
                     # Uniform tailored-setting rule: max_nodes may be raised up
                     # to the framework ceiling so shaped strata are realised;
                     # at the domain's 800 every stratum collapses to
                     # near-identical minimal inputs. Measurement unchanged.
                     max_nodes=8000)
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
