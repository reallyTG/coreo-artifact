# Running Coreógrafa

All commands run from the repository root.

## Environment

The tool needs **Python 3.12 or newer**, because `numpy==2.5.1` and
`scipy==1.18.0` in `requirements.txt` require it.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Fandango is pinned to 1.1.1. Released versions are not drop-in compatible with
each other, so install it into this virtualenv and not into a shared one.

Subjects that measure systems outside Python need those toolchains. The
versions below are the ones the evaluation ran on.

| Toolchain | Version used | Needed by |
|---|---|---|
| Python | 3.12.1 | everything |
| Node | 26.5.0 | every JavaScript subject |

## Per-subject setup

[subjects/README.md](subjects/README.md) names the setup of every subject. It
is one of the following.

**No setup.** `json` runs from `requirements.txt` alone.

**JavaScript subjects.** Each has a `package.json` that pins the versions it
compares.

```bash
(cd subjects/jsonpath_plus_latest && npm install)
```

**Python version subjects.** Each has a `build_envs.sh` that builds one
virtualenv per compared version under `subjects/<name>/envs/`.

```bash
bash subjects/orjson_known/build_envs.sh
```

A `*_tailored` subject reuses the environments of its `*_known` or `*_latest`
counterpart, so build that one.

## Commands

```bash
.venv/bin/python run.py --list                 # every subject found
.venv/bin/python run.py <subject> --quick      # exploration and analysis only
.venv/bin/python run.py <subject>              # the full loop, continuing its corpus
.venv/bin/python experiment.py rq1 --subjects <a,b> --runs 1 --uniform-budget --timeout 60
.venv/bin/python experiment.py score --results results/rq1/<directory>
```

`run.py` continues the subject's corpus in `output/<subject>/`. `experiment.py`
starts from an empty corpus in `results/`, seeds every run, and writes
`scores.csv`; it is what the paper's numbers come from. `--timeout` is the
budget in minutes.

`run.py` pins numpy's BLAS to one thread before anything imports numpy,
because the analyzer's matrices are too small to gain from threads. Export
`OPENBLAS_NUM_THREADS` yourself to override it.

## Output

`run.py` writes to `output/<subject>/`, and `experiment.py` writes the same
files under `results/<name>/<timestamp>/run<k>/<subject>/`.

| File | Contents |
|---|---|
| `corpus.csv` | One row per (system, input): properties and measured metrics |
| `corpus_inputs/` | One file per unique input, content-addressed |
| `metrics_cache.json` | Raw measurement samples |
| `summary.csv`, `summary_stats.csv` | Per-run snapshot of the corpus, and the same with n, mean and confidence intervals |
| `report.md` | The comparison: verdict per region, with intervals |
| `requests/`, `grammars/` | The targeting requests of each iteration and the rewritten grammars that realise them |
| `plots/` | Metric against property, fitted models, per-system intervals |

An experiment directory also holds `meta.json` (commit, seeds, command),
`logs/`, `scores.csv` and `scores_aggregate.csv`.

## Tests

```bash
.venv/bin/pip install pytest
.venv/bin/python -m pytest
```

## Bounding resources

A system under test is called with no memory bound of its own, and one
generated input can cost far more than a typical one. On Linux with systemd,
`./run_safe.sh <subject> [args]` runs `run.py` in a scope with a memory
ceiling (default 8G), one core, a wall-clock timeout and `nice`, each
overridable by environment variable (`MEM_MAX=16G ./run_safe.sh sql_js`).
`experiment.py` applies a 60-second cap per input measurement.
