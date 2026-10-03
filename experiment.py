#!/usr/bin/env python3
"""Run an evaluation experiment and leave something a table can be built from.

    python experiment.py rq1 --runs 3
    python experiment.py rq1 --subjects orjson_known,sql_js --runs 5
    python experiment.py score --results results/rq1/20260921-1400

`run.py` continues a subject's live corpus and is read by a person. This is
the EXPERIMENT run, and the differences are the ones that make a number
citable:

* Corpora start EMPTY. The corpus is persistent by design, and a subject
  carrying rows from earlier runs is not a starting state anyone can
  reproduce.
* Every run is SEEDED, so the table can be regenerated rather than re-rolled.
* A run can be REPEATED (`--runs`), each repetition with its own seed, and
  the score is then "detected in k of N runs".
* Output is machine-readable. `scores.csv` is what the tables read.

Each experiment writes results/<name>/<timestamp>/ holding meta.json (the git
SHA, the seeds, the command), run<k>/<subject>/ corpora, logs/, and scores.
"""
import argparse
import csv
import datetime
import json
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from core import manifest, score as scoring          # noqa: E402

# Seeds are derived from this, so an experiment re-run with the same --runs
# reproduces the same generation. Change it only to draw a genuinely new
# sample, and say so in the note that reports the numbers.
BASE_SEED = 20260921

# Minutes per subject before it is abandoned. A timeout is not destructive:
# the workflow checkpoints its corpus, so the run is scored on what it reached.
# Per-subject overrides of the default; none are needed for the subjects here.
BUDGET_MIN = {}
DEFAULT_BUDGET_MIN = 60
GRACE_SECONDS = 180


def git_state():
    def q(*a):
        try:
            return subprocess.run(a, cwd=REPO, capture_output=True,
                                  text=True, timeout=10).stdout.strip()
        except Exception:
            return ""
    return {"sha": q("git", "rev-parse", "HEAD"),
            "branch": q("git", "rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": bool(q("git", "status", "--porcelain"))}


def run_subject(subject, out_dir, log_path, seed, timeout_s, quick):
    """One subject, one run, into a fresh directory."""
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    graceful = max(60, timeout_s - GRACE_SECONDS)
    cmd = [sys.executable, "-u", "run.py", subject,
           f"--seed={seed}",
           f"--output-dir={out_dir}",
           f"--max-wall-seconds={graceful}"] + (["--quick"] if quick else [])
    started = time.time()
    with open(log_path, "w") as fh:
        fh.write(f"$ {' '.join(cmd)}\n\n")
        fh.flush()
        try:
            rc = subprocess.run(cmd, cwd=REPO, stdout=fh,
                                stderr=subprocess.STDOUT,
                                timeout=timeout_s).returncode
            status = "ok" if rc == 0 else f"exit {rc}"
        except subprocess.TimeoutExpired:
            status = f"TIMEOUT after {timeout_s // 60}m"
        except Exception as exc:
            status = f"{type(exc).__name__}: {exc}"
    return status, round(time.time() - started)


def corpus_inputs(out_dir):
    p = out_dir / "corpus.csv"
    if not p.exists():
        return 0
    with open(p, newline="") as fh:
        return len({r["input_hash"] for r in csv.DictReader(fh)})


def cmd_rq1(args):
    subs = pick_subjects(args)
    root = new_results_dir("rq1", args.tag)
    meta = {"experiment": "rq1", "git": git_state(),
            "command": " ".join(sys.argv), "base_seed": BASE_SEED,
            "runs": args.runs, "first_run": args.first_run,
            "uniform_budget": args.uniform_budget, "quick": args.quick,
            "subjects": [s["name"] for s in subs],
            "started": datetime.datetime.now().isoformat(timespec="seconds")}
    (root / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"results -> {root}")
    print(f"{len(subs)} subjects x {args.runs} runs, fresh corpora, "
          f"seeds {BASE_SEED}+run\n")

    ledger = []
    for run in range(args.first_run, args.first_run + args.runs):
        seed = BASE_SEED + run
        for s in subs:
            name = s["name"]
            out_dir = root / f"run{run}" / name
            if (out_dir / "corpus.csv").exists():
                print(f"  run{run} {name:<16} already present, skipping")
                continue
            budget = 60 * (args.timeout if args.uniform_budget
                           else BUDGET_MIN.get(name, args.timeout))
            print(f"  run{run} {name:<16} seed={seed} "
                  f"ceiling={budget // 60}m ... ", end="", flush=True)
            status, secs = run_subject(
                name, out_dir, root / "logs" / f"run{run}-{name}.log",
                seed, budget, args.quick)
            n = corpus_inputs(out_dir)
            print(f"{status} in {secs}s, {n} inputs")
            ledger.append({"run": run, "subject": name, "seed": seed,
                           "status": status, "secs": secs, "inputs": n})
            write_rows(root / "runs.csv", ledger)

    score_results(root, args.first_run + args.runs - 1)


def cmd_score(args):
    root = pathlib.Path(args.results)
    if not root.is_dir():
        sys.exit(f"no such results directory: {root}")
    runs = len([d for d in root.iterdir()
                if d.is_dir() and d.name.startswith("run")])
    score_results(root, max(runs, 1))


def score_results(root, runs):
    """Score every run in a results directory and aggregate across them."""
    all_rows = []
    for run in range(1, runs + 1):
        run_dir = root / f"run{run}"
        if not run_dir.is_dir():
            continue
        for s in manifest.SUBJECTS:
            if not s.get("rqs"):        # synthetic fixtures answer no RQ
                continue
            rows, why = scoring.score_subject(
                s, manifest.corpus_dir_for(s, run_dir))
            for r in rows:
                r["run"] = run
            all_rows.extend(rows)
    if not all_rows:
        print("\nnothing to score yet")
        return

    write_rows(root / "scores.csv", all_rows)

    # Per run, reduce to one outcome per subject; then count across runs. The
    # headline is "detected in k of N", which is what makes a claim from
    # repeated runs rather than from the run that happened to work.
    per_run = {}
    for run in range(1, runs + 1):
        for r in scoring.roll_up([x for x in all_rows if x["run"] == run]):
            per_run.setdefault(r["subject"], []).append(r)

    print(f"\n{'subject':<20}{'rqs':<12}{'blind':<7}{'expected':<12}"
          f"{'outcome':<17}{'explanation':<24}{'runs':>7}")
    print("-" * 99)
    agg = []
    for name in sorted(per_run):
        rs = per_run[name]
        counts = {}
        for r in rs:
            counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
        top = max(counts, key=lambda k: counts[k])
        first = rs[0]
        blind = {True: "yes", False: "no", None: "?"}[first["blind"]]
        rqs = ",".join(manifest.BY_NAME[name].get("rqs") or ())
        expl = first.get("explanation") or "-"
        print(f"{name:<20}{rqs[:11]:<12}{blind:<7}"
              f"{str(first['expected'])[:11]:<12}{top:<17}{expl[:23]:<24}"
              f"{counts[top]:>3}/{len(rs)}")
        agg.append({"subject": name, "rqs": rqs,
                    "category": first["category"],
                    "language": first["language"], "blind": first["blind"],
                    "expected": first["expected"], "outcome": top,
                    "explanation": first.get("explanation", ""),
                    "k": counts[top], "n": len(rs),
                    "outcomes": json.dumps(counts)})
    write_rows(root / "scores_aggregate.csv", agg)
    print(f"\n{root / 'scores.csv'}\n{root / 'scores_aggregate.csv'}")


def write_rows(path, rows):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def new_results_dir(name, tag=None):
    # Two batches started in the same minute would otherwise share a directory.
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M") + (f"-{tag}" if tag else "")
    root = REPO / "results" / name / stamp
    root.mkdir(parents=True, exist_ok=True)
    return root


def pick_subjects(args):
    if args.subjects:
        want = set(args.subjects.split(","))
        subs = [s for s in manifest.SUBJECTS if s["name"] in want]
        missing = want - {s["name"] for s in subs}
        if missing:
            sys.exit(f"not in the manifest: {', '.join(sorted(missing))}")
        return subs
    return manifest.subjects(include_synthetic=args.all,
                             include_cross_language=args.all)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("rq1", help="fresh-corpus runs over the benchmark")
    p1.add_argument("--runs", type=int, default=3)
    p1.add_argument("--subjects", default=None)
    p1.add_argument("--timeout", type=int, default=DEFAULT_BUDGET_MIN,
                    help="minutes per subject (default 60); subjects with a "
                         "known-larger cost have their own ceiling")
    p1.add_argument("--first-run", type=int, default=1,
                    help="index of the first run; seeds are BASE_SEED+run, so "
                         "--first-run 2 --runs 2 adds runs 2 and 3 to an existing run 1")
    p1.add_argument("--uniform-budget", action="store_true",
                    help="apply --timeout to every subject, ignoring the "
                         "per-subject ceilings in BUDGET_MIN")
    p1.add_argument("--tag", default=None,
                    help="suffix for the results directory name")
    p1.add_argument("--quick", action="store_true",
                    help="exploration only, no targeted loop. Useful to time "
                         "the pipeline; NOT a result, since the loop is what "
                         "the paper claims")
    p1.add_argument("--all", action="store_true",
                    help="include subjects the manifest marks synthetic")
    p1.set_defaults(func=cmd_rq1)

    p3 = sub.add_parser("score", help="rescore an existing results directory")
    p3.add_argument("--results", required=True)
    p3.set_defaults(func=cmd_score)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
