"""simplejson 3.20.2 and 4.0.0 on a grammar tailored to the commit's diff (RQ1, tailored setting).

Same two systems, runner and budget as simplejson_known (its venvs and
py_runner.py, by path, through simplejson_known.SYSTEMS). The grammar is
simplejson_tailored.fan, a sub-language of the frozen subjects/json/json.fan
written from e2e5f0b (#369: interning a member name through the scanner's memo
dict takes one PyDict_SetDefault instead of GetItemWithError + SetItem): one
flat object of many short ASCII names with cheap scalar values, so the
per-name memo operation is as large a share of the parse as the language
allows. The header of the .fan gives the rationale and the sub-language
argument. The commit saves one dict probe per name, so the expected effect is
a few percent; a pair that stays below the detection band here is a valid
outcome.

Exploration is stratified on the root object's width (`<more_member>`) in
four bands, 25-100, 100-500, 500-2000 and 2000-3000 members. Everything else
in the WorkflowConfig, budget included, is the domain's, unchanged. Any pair
detected here counts as detected after tailoring, not blind.
"""
from dataclasses import replace
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

import importlib.util

from core.workflow import run_workflow
import subjects.simplejson_known.example as known

HERE = Path(__file__).resolve().parent
NAME = "simplejson_tailored"

# Member counts are 1 + repetitions of <more_member>.
STRATIFY = {"nt": "<more_member>",
            "bands": [(24, 99), (99, 499), (499, 1999), (1999, 2999)]}


def _udf():
    spec = importlib.util.spec_from_file_location(
        "simplejson_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def workflow(output_dir: Path, quick: bool = False):
    config = replace(known.domain_config(quick), name=NAME,
                     functions=known.SYSTEMS, udf_module=_udf(),
                     fan_filepath=HERE / "simplejson_tailored.fan", eval_dir=HERE,
                     stratify=STRATIFY)
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
