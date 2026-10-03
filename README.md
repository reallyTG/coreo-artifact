# Coreógrafa

Coreógrafa uses a grammar-based fuzzer as a comparative profiler. It takes an
executable specification of an input language, generates inputs from it,
measures two or more systems that compute the same thing, and fits models that
relate properties of the input to the cost of running it. It then rewrites the
specification to target the regions that need more data (where the systems
diverge, where cost is extreme, where the corpus is thin) and repeats.

This repository is the anonymized artifact for the submission. It holds the
tool, every subject in the evaluation, the data behind the subject selection,
and the bugs found.

## Where things are

| Path | Contents |
|---|---|
| `src/core/` | The tool. `workflow.py` is the loop; `fuzzer.py` generates and measures; `corpus.py` stores; `compare.py` decides which system is cheaper and where; `targeting.py` writes the next requests; `score.py` applies the detection rule |
| `src/core/manifest.py` | The labelled benchmark: each subject's category, systems, expected verdict, and whether its grammar was written before the diff was read |
| `src/core/runners/` | Measurement runners for systems outside Python |
| `subjects/` | One directory per subject. [subjects/README.md](subjects/README.md) lists all of them by group, with what each compares and what it needs |
| `eval/known_pairs/` | The mining funnel: one CSV per library with every candidate commit and the reason it was kept or dropped, plus the notes that summarise the counts |
| `eval/latest_series_2026-09-30.json` | The preregistered latest release series |
| `results/rq1/` | The corpora of the 25 runs the paper reports: 17 on specification grammars and 8 on tailored grammars (`*-tailored-*`), without the regenerable plots |
| `findings/` | Bugs found, one directory each with a proof of concept. [findings/README.md](findings/README.md) |
| `experiment.py` | The evaluation driver: empty corpus, seeded, machine-readable scores |
| `run.py` | Runs one subject interactively, continuing its corpus |
| `tools/` | Scripts that draw the paper's figures from a results directory |
| `docs/adding-a-subject.md` | How to write a new subject |

## Quick start

Python 3.12 or newer is required.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py --list
.venv/bin/python run.py json --quick      # exploration only, no other setup
```

Output lands in `output/json/`. [RUNNING.md](RUNNING.md) gives the setup
for every other subject and describes the output files.

## From the paper to the repository

| In the paper | Here |
|---|---|
| The four input languages and their five grammars (JSONPath has one per implementation language) | `subjects/json`, `jsonpath_js`, `jsonpath_py`, `selectors_js`, `sql_js`; each `.fan` file is the grammar, and the `*_known` and `*_latest` subjects of a domain reuse it |
| Mined known pairs | `subjects/*_known` (blind grammar) and `subjects/*_tailored` (grammar shaped by the diff); selection data in `eval/known_pairs/` |
| Latest release series | `subjects/*_latest`; preregistration in `eval/latest_series_2026-09-30.json` |
| Competing implementations | `subjects/json`, `jsonpath_js`, `jsonpath_py`, `selectors_js`, `sql_js` |
| The detection rule and verdicts | `src/core/score.py`, `src/core/compare.py` |
| Expected verdicts and mechanisms | `src/core/manifest.py` |
| Bugs found | `findings/` |
| Tables of RQ1 and RQ2 | `.venv/bin/python experiment.py score --results results/rq1/<directory>` rescoring the shipped corpora |
| Figures | `tools/fig_*.py` read the corpora in `results/rq1/` and write to `figures/` |
| Motivating Example: what generation without the loop reaches | `.venv/bin/python tools/ablation_reach.py` scores the arm corpora in `output/_ablate_jsonpath_plus/`; `src/core/ablate.py` regenerates them (command in the script's docstring). At this 100-input budget the ladder shows reach, not decisions: the guided arm does not decide its regions at this budget |

## Reproducing an evaluation run

Set up the subject first (see [RUNNING.md](RUNNING.md)). All commands run from
the repository root.

```bash
# one run of one subject: empty corpus, seeded, 60-minute budget
.venv/bin/python experiment.py rq1 --runs 1 --first-run 1 \
    --uniform-budget --timeout 60 --subjects jsonpath_plus_latest

# rescore an existing results directory without re-running it
.venv/bin/python experiment.py score --results results/rq1/<directory>
```

Each run writes `results/rq1/<timestamp>/` with `meta.json` (commit, seeds,
command), the corpus, the requests of each iteration, and `scores.csv`.
Generation is seeded, so a rerun produces the same exploration inputs. Timings
depend on the machine, so the verdicts and the regions they name are the
reproducible quantity, and absolute runtimes are not.

## How the loop works

1. **Explore.** Generate inputs from the grammar, stratified so the first
   sample spans the size axis.
2. **Measure.** Run each system on each kept input, sampling to significance.
   Generation never runs the systems under test. Measurement is cached, so
   samples accumulate across runs.
3. **Accumulate.** Upsert into a content-addressed corpus. A repeated input
   tightens its confidence interval and does not add a row.
4. **Model.** Fit input properties against measured cost, per system.
5. **Target.** Rewrite the grammar to aim at divergent, extreme, or
   under-sampled regions, and generate again.
6. **Stop** when an iteration stops finding new inputs or the budget runs out.

## Adding a subject

A subject is a grammar, the systems under test, property functions, and an
`example.py`.

```bash
cp -r subjects/_template subjects/mysubject
.venv/bin/python run.py mysubject --quick
```

Systems can be in-process Python callables or anything reachable as a process:
another language, another version of a package, or an existing binary. The
contract is one line of `key=value` metrics on stdout, and `src/core/runners/`
provides the measurement code for Python and JavaScript. The
walkthrough is in [docs/adding-a-subject.md](docs/adding-a-subject.md).

## Anonymization

Author names, machine paths, and the details of how findings reached their
maintainers have been removed, and the commit history has been replaced by
snapshot commits.
