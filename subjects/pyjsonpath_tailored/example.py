"""python-jsonpath 1.3.2 and 2.0.0 on a grammar tailored to the commit's diff (RQ1, tailored setting).

Same two systems, runner and budget as pyjsonpath_known (its envs and
py_runner.py, by path through subjects.pyjsonpath_known.example.SYSTEMS). Only
the grammar and the properties differ: pyjsonpath_tailored.fan is a sub-language
of the frozen jsonpath_py.fan shaped from commit 7ed181a's diff (regex caching
in match()/search(); rationale in its header), and user_def_functions.py adds
`n_doc_nodes` and `n_function_calls`. The expected outcome is null, because
the cached path does not differ between these two versions.

Stratification. The grammar renames the root array's repetition to
`<wide_more_item>` so the number of elements a filter visits can be banded;
Fandango lands on a band's lower bound, so there are three bands. The number
of match()/search() calls per filter (`<and_tail>+`) is left to the GA under
the domain's max_repetition. Explicit `stratify` takes precedence over
auto-stratification in core/workflow.py; auto_stratify is also set False so
the choice is visible here.

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
import subjects.pyjsonpath_known.example as known

HERE = Path(__file__).resolve().parent
NAME = "pyjsonpath_tailored"
FAN = HERE / "pyjsonpath_tailored.fan"

STRATIFY = {"nt": "<wide_more_item>", "bands": [(5, 30), (60, 150), (250, 500)]}


def _udf():
    spec = importlib.util.spec_from_file_location(
        "pyjsonpath_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def workflow(output_dir: Path, quick: bool = False):
    # Budget fields come unchanged from the domain config via pyjsonpath_known.
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
