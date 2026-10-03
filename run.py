#!/usr/bin/env python3
"""Coreografa experiment runner.

Usage:
    python run.py <subject> [--quick]
    python run.py --list

Subjects are directories under `subjects/`; each one holding an `example.py`
that defines `workflow(output_dir, quick=False)` is runnable, so adding a
subject needs no edit to this file. Artifacts are written to output/<subject>/.

  --quick        Skip the targeted request loop. Runs only the initial
                 (stratified) exploration plus analysis: summary, plots,
                 fitted models. Much faster, and the right first run for a
                 new subject.
  --output-dir=P Write artifacts here instead of output/<subject>/. An
                 evaluation run points this at a fresh directory, because the
                 corpus is persistent by design: a subject whose corpus holds
                 months of development rows is not a clean starting state for
                 a measured run.
  --seed=N       Base seed for Fandango's RNG, making the run reproducible.
  --list         List discovered subjects and exit.
"""
import importlib
import os
import sys
from pathlib import Path

# numpy/scipy/statsmodels link OpenBLAS, which otherwise starts one thread per
# core. The analyzer's matrices are tiny, so those threads add no speedup: on a
# 48-thread machine they tripled CPU time for identical wall time and output.
# Must be set before numpy is first imported. setdefault keeps any explicit
# override from the caller's environment.
for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_var, "1")

REPO_ROOT = Path(__file__).resolve().parent
SUBJECTS_DIR = REPO_ROOT / "subjects"

sys.path.insert(0, str(REPO_ROOT))            # subjects.*
sys.path.insert(0, str(REPO_ROOT / "src"))    # core.*, analyzer


def discover():
    """Map subject name -> module path, for every subjects/*/example.py.

    Directories starting with "_" are skipped, so `subjects/_template/` can
    hold the skeleton without appearing as a runnable subject.
    """
    found = {}
    if not SUBJECTS_DIR.is_dir():
        return found
    for d in sorted(SUBJECTS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith(("_", ".")) and (d / "example.py").is_file():
            found[d.name] = f"subjects.{d.name}.example"
    return found


def main():
    subjects = discover()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    if "--list" in flags:
        print("Subjects in subjects/:")
        for name in subjects:
            print(f"  {name}")
        return

    wall = seed = out_override = None
    for f in list(flags):
        if f.startswith("--max-wall-seconds="):
            wall = int(f.split("=", 1)[1])
            flags.discard(f)
        elif f.startswith("--seed="):
            seed = int(f.split("=", 1)[1])
            flags.discard(f)
        elif f.startswith("--output-dir="):
            out_override = f.split("=", 1)[1]
            flags.discard(f)

    name = args[0] if args else None
    if name not in subjects:
        if name is not None:
            print(f"Unknown subject: {name}\n")
        print(f"Usage: python run.py [{' | '.join(subjects)}] "
              f"[--quick] [--max-wall-seconds=N] [--seed=N] "
              f"[--output-dir=PATH]")
        sys.exit(1)

    output_dir = (Path(out_override) if out_override
                  else REPO_ROOT / "output" / name)
    output_dir.mkdir(parents=True, exist_ok=True)
    mod = importlib.import_module(subjects[name])
    if wall is not None or seed is not None:
        # Override the subject's own budget for this invocation. A caller that
        # wants a graceful stop can then say so without editing the
        # subject, and without resorting to a kill that loses the reports.
        import core.workflow as _wf
        real = _wf.run_workflow

        def _capped(config, out_dir, *a, **k):
            if wall is not None:
                config.max_wall_seconds = wall
            if seed is not None:
                config.random_seed = seed
            return real(config, out_dir, *a, **k)

        _wf.run_workflow = _capped
        mod_real = getattr(mod, "run_workflow", None)
        if mod_real is not None:
            mod.run_workflow = _capped
    mod.workflow(output_dir, quick="--quick" in flags)


if __name__ == "__main__":
    main()
