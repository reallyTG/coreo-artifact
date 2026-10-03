"""orjson 3.10.1 to 3.10.6 on a grammar tailored to the commits' diffs (RQ1, tailored setting).

Same six systems, runner and budget as orjson_known (its venvs and
py_runner.py, by path, through orjson_known.SYSTEMS). The grammar is
orjson_tailored.fan, a sub-language of the frozen subjects/json/json.fan
written from the 3.10.2 commits (a1a2ed9 yyjson population rewrite, fcbd9a4
key cache 1024 -> 2048) and the 3.10.6 commits (c369ea4 PyUnicode creation
rewrite, 9382058 xxh3 key hash): one flat key-dense object of short names and
scalar values, string content restricted to ASCII, Latin-1, and ASCII with one
BMP char. The header of the .fan gives the rationale and the sub-language
argument. One grammar covers both pairs because both changes are per member
name / per decoded string of the same object shape; 3.10.3 -> 3.10.4 is not
targeted and is expected to stay null.

Exploration is stratified on the root object's width (`<more_member>`) in
four bands, 25-60, 60-200, 200-800 and 800-2000 members, so the sample spans
the range where the population rewrite applies and crosses the old 1024-slot
key cache. Everything else in the WorkflowConfig, budget included, is the
domain's, unchanged. Any pair detected here counts as detected after
tailoring, not blind.
"""
from dataclasses import replace
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

import importlib.util

from core.workflow import run_workflow
import subjects.orjson_known.example as known

HERE = Path(__file__).resolve().parent
NAME = "orjson_tailored"

# Member counts are 1 + repetitions of <more_member>.
STRATIFY = {"nt": "<more_member>",
            "bands": [(24, 59), (59, 199), (199, 799), (799, 1999)]}


def _udf():
    spec = importlib.util.spec_from_file_location(
        "orjson_tailored_udf", HERE / "user_def_functions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def workflow(output_dir: Path, quick: bool = False):
    config = replace(known.domain_config(quick), name=NAME,
                     functions=known.SYSTEMS, udf_module=_udf(),
                     fan_filepath=HERE / "orjson_tailored.fan", eval_dir=HERE,
                     stratify=STRATIFY)
    run_workflow(config, output_dir)


if __name__ == "__main__":
    workflow(REPO_ROOT / "output" / NAME)
