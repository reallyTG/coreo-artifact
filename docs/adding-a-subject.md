# Adding a subject

A subject is four real artifacts plus a config block. Everything else — input
generation, measurement, the growing corpus, model fitting, targeted
regeneration, plots — comes from the framework.

```
subjects/<name>/
  <name>.fan             the input language: grammar, and any constraints
  user_def_functions.py  input properties (the model's features)
  <the systems>          Python callables, or runners invoked out of process
  example.py             wires them together and sets the budget
```

Start by copying the template:

```bash
cp -r subjects/_template subjects/mysubject
python run.py mysubject --quick
```

There is no registry to edit. `run.py` discovers any `subjects/*/example.py`,
so the copy is runnable immediately; `python run.py --list` shows what it
found. Directories starting with `_` are skipped.

## What makes a good subject

The framework compares **functionally equivalent systems**, so it needs two or
more implementations that compute the same thing. A cost difference is then a
property of the implementation rather than of the task. Two shapes work:

- **Differential** — independent implementations of one spec (four JSON
  parsers, five JSONPath engines, three CSS selector engines). Safe, because
  the engines exist: the comparison cannot fail to materialise.
- **Comparative** — two versions of one system, before and after a documented
  performance change. Stronger as a story, but it needs a real documented
  version pair found first.

The input space has to be describable as a grammar with enough structure to
model. Size alone is a thin feature set; you want shape properties too — the
things that make one implementation diverge from another.

## 1. The grammar

Write the input language as a `.fan` file. 
A few Fandango quirks:

**One production per line.** A `|` alternative continued on the next line is a
syntax error, reported as `no viable alternative at input '|'`, even though it
reads perfectly well to a human. This is wrong:

```
<verb> ::= "filter:" <col>
         | "select:" <col>
```

and this is right:

```
<verb> ::= "filter:" <col> | "select:" <col>
```


### Compound inputs

Plenty of subjects have a two-part input: a pattern and a haystack, a selector
and a document, a query and a table. The harness passes one string, so encode
both halves with a separator the runner splits on:

```
<start> ::= <selector> "\n@@@\n" <doc>
```

Pick a marker neither half's alphabet can produce. Keeping the halves
independent in the grammar is what lets the analysis attribute cost to one or
the other.

### Write the language, not the experiment

Anything that can grow is `*`, `+` or recursion. Put a finite bound in the
grammar only where the specification imposes one -- `<digit>{0,17}` is fair
because that is what an IEEE-754 double round-trips; `<more_member>{0,40}` is
not, because nothing bounds how many members a JSON object may have. A size cap
written into the grammar becomes the ceiling for every axis under it, and the
frontier report will correctly pin the property against it forever.

Generation size comes from `max_repetition`, `max_nodes` and the targeted
requests instead. Those are search settings and can be raised; the grammar is a
claim about the subject and should not move.

The same goes for alternatives. A fixed list of seven text strings or four
class names is a cap wearing different clothes, and it silently disables
whatever axis it stands on: four CSS classes means nearly every selector
matches, so class cardinality -- the thing a matcher's cost turns on -- cannot
vary.

### Nesting

Write nesting as recursion. Unrolling it into explicit levels (`node0`
contains `node1` contains `node2`) keeps depth bandable but caps the depth the
grammar can express, on the axis a nested input's cost most depends on. Depth
under recursion is reached through `max_nodes` and a soft objective rather
than by banding.

**Recursive grammars need `max_repetition` set low in their config.** Breadth
and depth multiply, and a recursive grammar at a high `max_repetition` can
recurse deep enough to exhaust Python's stack inside Fandango's own tree walk.
The `WorkflowConfig` default of 200 is meant for list-shaped grammars.

## 2. Properties

Most properties you do not have to write. `core/grammar_props.py` derives a
`count_<X>` for every non-terminal whose count can vary, works out which
repetition governs it, and computes the bound the language puts on it. What is
left for `user_def_functions.py` is what derivation cannot express: tree
measures like `depth`, and anything computed over the input text rather than
the parse, like `total_string_len`.

Each function there takes a derivation tree and returns a number. `PROPERTIES`
lists which ones are features; everything else is treated as a helper.

If a declared property is exactly a derived count, say so in `ALIASES`:

```python
PROPERTIES = ["depth", "num_pairs", "total_string_len"]
ALIASES = {"num_pairs": "count_member"}
```

That keeps your column name and stops the same quantity entering the loop
twice under two names. Check on sampled inputs that it is really the same
quantity rather than assuming from the name.

Properties should describe work that HAPPENS. A property that counts a
construct the runner skips fits the models against work that never ran.

Include size properties, but spend most of the effort on **shape**: the number
of filters in a query, the nesting depth of a document, the count of
compound selectors in a selector list. Size tells you an input is big. Shape is what
predicts two implementations disagreeing, and that is what the models are for.

## 3. The systems

**In-process** is a plain Python callable taking one input. Fastest to set up,
and right when every system is a Python library.

Return `False` from a SUT that **rejects** the input — a parse error, a
malformed query, anything where it bails instead of doing the work. Rejected
inputs stay in the corpus but are kept out of the models and the request loop,
because an early exit is a different cost population, and fitting one model
across both is fitting a mixture. Any other return value (`None`, the result) counts
as accepted, so a SUT with nothing to say need not say it.

What it receives depends on `input_type`: a `str` for `"string"`, a `list[int]`
for `"int_array"`. Not a derivation tree. The harness converts once, before the
clock starts, so do the same in your own SUT and keep setup out of the timed
call. `str(tree)` can cost far more than the work being measured. Properties
are the exception and still receive the tree,
since they are computed off the clock.

**Out-of-process** covers another language, another version of a package that
cannot coexist in one process, or an existing binary:

```python
from core.subprocess_sut import make_subprocess_sut

node_sut = make_subprocess_sut("jsonpathly", "node", HERE / "runner.js",
                               args=("jsonpathly",), k=20)
```

The contract is one line of `key=value` pairs on stdout. The runner reads the
input file, runs the target K times, prints the numbers. Framework runners
exist for each language:

| language | runner | notes |
|---|---|---|
| Python | `core/bench_runner.py` | full metric set |
| JavaScript | `core/runners/bench.js` | `process.resourceUsage()` covers nearly all of it |

Pass `script=None` for a compiled binary — it takes the input path as its own
first argument, with no interpreter in front.

A system under test whose target is an existing CLI needs no runner in the
target's language at all. A Python runner can launch the
binary and read `getrusage(RUSAGE_CHILDREN)`.

### Keep the systems genuinely equivalent

This is the part that quietly goes wrong. If one backend errors where another
succeeds, or returns a differently-shaped result, you are timing two different
computations. Have each runner emit a result-shape value — `hits`,
`nodes`, `matched` — and check the systems agree on it before trusting any
timing.

Check it by running the runners directly on a few inputs, not by adding the
value to `metrics`. That list drives targeting as well as modelling, so a
column that is not a cost would send the request loop chasing it. Declare such
values in `extra_metrics` instead, where they are captured without being
modelled.

## 4. Choosing K, samples, and metrics

**K is a precision knob, not a semantic one.** Runners report the *median
per-call* time, so different K across systems stays comparable — and it often
must differ. One system can run an input in 42ns and need
K=4000 to clear the clock, while another takes 16ms on the same input and would
stall the campaign at anything above single digits.

Two symptoms tell you K is wrong: a metric of `0` means you are under the clock
floor, and a campaign that will not finish means K is too high for the slowest
system.

**Samples multiply process launches.** Each of `metric_min_n`..`metric_max_n`
is another process. At an interpreter startup of ~250ms, a 300-input corpus at 5
samples is roughly six minutes of startup alone. Prefer a bigger in-process K
and a smaller sample count out of process.

**Only model metrics that are comparable across your systems.** Runtime is
almost always safe. RSS is not, when the systems are different language
runtimes: `ru_maxrss` is bytes on macOS and kilobytes on Linux, and the numbers
mostly reflect each interpreter's baseline footprint anyway. A subject whose
systems share one runtime can model RSS as well.

**A deterministic metric beats a timer where one exists.** An internal work
counter excludes process startup, and being deterministic it needs no
resampling to stabilise.

## 5. Stratify the first sample

```python
stratify={"nt": "<item>", "bands": [(0, 5), (5, 15), (15, 30), (30, 50)]}
```

This rewrites the named repetition once per band, so the initial corpus spans
the size axis instead of clustering wherever the search settles. Do not rely on
the genetic algorithm for that spread. Fandango tends to pick a band's lower
bound, so narrower bands give better spread within each one.

Pass a list to band more than one axis. Every combination of bands is
generated, so the run count is the product and the bands per axis should stay
few:

```python
stratify=[
    {"nt": "<segment>",    "bands": [(1, 4), (4, 8), (8, 16)]},
    {"nt": "<more_value>", "bands": [(0, 10), (10, 100), (100, 400)]},
]
```

A repetition whose upper bound is large is not reachable on the default node
budget: the generator will simply never choose the expensive branch, and you
get a corpus with none of the structure you asked for and no warning. If a
banded axis comes back empty, raise `max_nodes` before suspecting the grammar.

## Property screening before the joint fit

`fit_model_for_metric_and_features` tries one model per assignment of a
complexity class to a feature, so its cost is `6 ** len(features)`: six
properties is 46,656 fits, nine is over ten million. `core/feature_select.py`
therefore chooses which properties enter that fit, dropping those that track no
metric and then those already explained by a more relevant property. Every drop
is printed with its reason. Single-feature plots and fits still cover every
property, so nothing disappears silently.

Three `WorkflowConfig` knobs control it: `max_joint_features` (6),
`feature_corr_threshold` (0.8), `feature_relevance_floor` (0.05). The defaults
are usually right. What is worth reading is the `[select]` output, because it
is a free audit of your property set: two properties that correlate 1.00 are
one property, and a property that scores suspiciously well may be counting
something other than what its name says.

## 6. Run it

```bash
python run.py mysubject --quick    # exploration and analysis only
python run.py mysubject            # adds the targeted request loop
```

Start with `--quick`. It exercises the grammar, the properties and all the
systems without waiting on the request loop, and most setup mistakes surface
there.

Artifacts land in `output/mysubject/`: `corpus.csv` (the accumulating source of
truth), `corpus_inputs/` (one file per unique input), `plots/`,
`summary*.csv`, `metrics_cache.json`, and `frontier.json`. The corpus, the
cache and the frontier ledger persist across runs; everything else is rebuilt.

### Read the grammar frontier

At the end of a run the loop prints the properties it stopped trying to push
past, and `frontier.json` records them:

```
[mysubject] grammar frontier (targeting stopped asking here):
  count_segment: pinned at 24 (asked for [25, 26]); 1 request(s) beyond it returned nothing.
  count_comment: constant at 0 over the corpus; the grammar cannot vary it.
```

A pinned property means every input this grammar can express already sits at or
below that value. Read it two ways.

As a **result caveat**: a null on an axis that needs a larger value is a
statement about the grammar, not about the systems compared. This is the one
place the output says so.

As a **setup bug**: a property you expected to vary and that comes back
constant means the grammar does not reach the construct the property counts,
and the model has been fitting a column of zeros. Before widening the grammar,
check `max_nodes`. It caps the derivation tree independently of any `{n,m}` in
the grammar, and it is the more common culprit for a count that stalls well
short of its written bound.

## Comparing two versions of one system

A version pair is two releases of the same project, and it belongs in **one**
subject with two SUTs, never two subjects, or the two never meet in a single
corpus. Install each release side by side (an npm alias per version, or one
virtualenv per version built by a `build_envs.sh`) and drive every release
through the same runner, so a measured difference cannot be the runner
differing between the two sides. `subjects/jsonpath_plus_latest` and
`subjects/orjson_known` show both layouts.

Two things are easy to get wrong here.

**Check equivalence, not just performance.** Have each runner print a
result-shape value and confirm the builds agree on every input before trusting
any timing. A behavioural change shipped alongside a performance change is the
specific risk a version pair carries.

**A grammar that cannot express the affected inputs reports no difference, and
says nothing about why.** When a pair shows nothing, the grammar is at least as likely to be the
reason as the program.

## Checklist when something looks wrong

| Symptom | Usual cause |
|---|---|
| `no viable alternative at input '\|'` | a production split across lines |
| 0 inputs generated, `KeyError` on summary.csv | the grammar parsed but produced nothing; run it standalone |
| a metric reads `0` | K too low — under the clock floor |
| systems look identical | measurement floor is swamping the difference; raise K |
| one system errors on some inputs | the grammar left the common subset those systems share |
| implausible divergence | check the result-shape metric; you may be timing different computations |
| campaign will not finish | K too high for the slowest system, or too many samples out of process |
