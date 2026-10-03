"""Persistent, deduped, growing corpus — the source of truth for modeling.

Design:
- Inputs are stored content-addressed, one file per unique input:
  `corpus_inputs/<sha1(canonical_input)>.txt`. Never embed raw input in a CSV
  (grammars may emit newlines/commas/quotes). One file per input is also
  newline-safe and matches how the rest of the pipeline stores inputs.
- `corpus.csv` holds one row per (function_name, input_hash): metric means +
  CI/n, properties, and first/last iteration seen. All CSV-safe scalars.
- `upsert` dedups by input: a NEW input grows the corpus; a SEEN input refreshes
  its stats (its cached samples may have grown -> tighter CI) without
  duplicating. -> the set builds up across iterations/runs.
- Derived views for the existing analyzer/plots: write_summary (clean columns
  the analyzer expects) and write_stats (CI sidecar for error bars).
"""
import csv
import hashlib
from pathlib import Path


def accepted(row):
    """Did the SUT process this input rather than reject it?

    Absent means accepted: a corpus row predating the flag, or a SUT that
    signals nothing (only an explicit `False` return counts as a rejection).
    """
    v = row.get("accepted", 1.0)
    if v in (None, ""):
        return True
    try:
        return float(v) >= 0.5
    except (TypeError, ValueError):
        return True


class CorpusStore:
    def __init__(self, root, metrics, properties):
        self.root = Path(root)
        self.inputs_dir = self.root / "corpus_inputs"
        self.csv_path = self.root / "corpus.csv"
        self.metrics = list(metrics)          # e.g. ["runtime_ns", "memory_peak"]
        self.properties = list(properties)    # e.g. ["length", "depth"]
        self.rows = {}                        # (function_name, input_hash) -> dict
        # Everything a SUT reports beyond `metrics` (result shape such as
        # `hits`, `matched=`, `output_bytes`), stored as `x_<name>` columns.
        # Kept OUT of `metrics` on purpose, since metrics drive targeting. They
        # are what lets scoring check that two systems returned the same answer
        # before their timings are compared.
        self.extras = []
        self.inputs_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _hash(text):
        return hashlib.sha1(text.encode("utf-8", "surrogatepass")).hexdigest()

    def load(self):
        if not self.csv_path.exists():
            return
        with open(self.csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for c in reader.fieldnames or ():
                if c.startswith("x_") and c not in self.extras:
                    self.extras.append(c)
            for r in reader:
                self.rows[(r["function_name"], r["input_hash"])] = self._migrate(r)

    def _migrate(self, row):
        """Fill columns a row predates.

        The corpus is meant to outlive changes to a subject, so it accumulates
        rows written when the metric list was shorter. DictReader
        hands those back as None, `save` writes them as empty cells, and the
        analyzer then calls float("") and takes the run down. An absent
        measurement is NaN by the same rule `upsert` uses for a censored one:
        the row keeps its properties and stays out of the models. An absent
        property is 0, matching `upsert`.
        """
        for m in self.metrics:
            if row.get(m) in (None, ""):
                row[m] = float("nan")
                row[f"{m}_n"] = 0
                row[f"{m}_std"] = 0
                row[f"{m}_ci_lo"] = float("nan")
                row[f"{m}_ci_hi"] = float("nan")
        for p in self.properties:
            if row.get(p) in (None, ""):
                row[p] = 0
        # Rows written before acceptance was recorded. Treated as accepted,
        # which is right for every subject whose SUTs never reject.
        if row.get("accepted") in (None, ""):
            row["accepted"] = 1.0
        return row

    def upsert(self, function_name, input_text, properties, metric_stats, iteration,
               raw_text=None):
        """metric_stats: {metric_name: {"n","mean","ci"(lo,hi),"std"}}. Returns True if new.

        `input_text` is the canonical key (stripped, so it stays stable across
        rounds) and is what the hash is taken over. `raw_text`, when given, is
        the exact generated input and is what gets stored. The two differ
        whenever the language includes leading or trailing whitespace: the
        stripped form may not parse, so a stripped file could not be re-used
        as a re-fuzz seed.
        """
        h = self._hash(input_text)
        fpath = self.inputs_dir / f"{h}.txt"
        stored = input_text if raw_text is None else raw_text
        # Rewrite when the content differs, so a corpus written before this
        # distinction existed migrates in place as its inputs are re-measured.
        if (not fpath.exists()
                or fpath.read_text(encoding="utf-8", errors="surrogatepass") != stored):
            fpath.write_text(stored, encoding="utf-8", errors="surrogatepass")
        key = (function_name, h)
        existing = self.rows.get(key)
        row = existing or {
            "function_name": function_name, "input_hash": h,
            "first_seen_iter": iteration,
        }
        row["last_measured_iter"] = iteration
        # Did the SUT process this input, or reject it? Rejected inputs stay in
        # the corpus (the cost of the error path is real, and re-generating them
        # would be wasteful) but are kept out of the models and the targeting by
        # `write_summary` and `core.targeting`. Absent means accepted, which is
        # what a SUT that signals nothing means.
        acc = metric_stats.get("accepted", {})
        row["accepted"] = 1.0 if acc.get("mean", 1.0) >= 0.5 else 0.0
        for p in self.properties:
            row[p] = properties.get(p, 0)
        for m in self.metrics:
            s = metric_stats.get(m, {})
            # No samples means no measurement — every run of this input was
            # censored or failed. Recording 0 would file the most expensive
            # inputs as the cheapest; NaN keeps the row (and its properties) in
            # the corpus while keeping it out of the models and the targeting.
            mean = s.get("mean", float("nan"))
            ci = s.get("ci", (mean, mean))
            row[m] = mean
            row[f"{m}_n"] = s.get("n", 0)
            row[f"{m}_std"] = s.get("std", 0)
            row[f"{m}_ci_lo"] = ci[0]
            row[f"{m}_ci_hi"] = ci[1]
        for name, s in metric_stats.items():
            if name in self.metrics or name == "accepted" or not isinstance(s, dict):
                continue
            col = f"x_{name}"
            if col not in self.extras:
                self.extras.append(col)
            # Median: a result shape is deterministic per input, and the median
            # is robust to one odd sample if it is not.
            row[col] = s.get("median", s.get("mean", float("nan")))
        self.rows[key] = row
        return existing is None

    def set_properties(self, input_hash, properties):
        """Overwrite the property columns of every row for one input.

        Properties are a function of the input, not of a run, so a new property
        can be filled in for an existing corpus without re-executing anything.
        `upsert` cannot do this: it rewrites the metric columns too, and the
        caller would have to reconstruct metric_stats it does not have.

        Returns the number of rows updated.
        """
        n = 0
        for (_, h), row in self.rows.items():
            if h != input_hash:
                continue
            for p in self.properties:
                row[p] = properties.get(p, row.get(p, 0))
            n += 1
        return n

    def _fieldnames(self):
        fns = ["function_name", "input_hash", "first_seen_iter", "last_measured_iter",
               "accepted"]
        fns += list(self.properties)
        for m in self.metrics:
            fns += [m, f"{m}_n", f"{m}_std", f"{m}_ci_lo", f"{m}_ci_hi"]
        fns += list(self.extras)
        return fns

    def save(self):
        with open(self.csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=self._fieldnames(), extrasaction="ignore")
            w.writeheader()
            for row in self.rows.values():
                w.writerow(row)

    def size(self):
        return len(self.rows)

    def read_input(self, input_hash):
        p = self.inputs_dir / f"{input_hash}.txt"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="surrogatepass")
        return None

    def count_added_at(self, iteration):
        return sum(1 for r in self.rows.values()
                   if int(r.get("first_seen_iter", -1)) == iteration)

    # --- derived views for the existing analyzer/plots ---
    def write_summary(self, summary_path):
        """Clean view the analyzer expects: function_name, input_id, metrics, properties.
        input_id = input_hash. memory_after kept (ignored by analyzer) for column compatibility.

        Rejected inputs are excluded. A SUT that rejects an input exits early
        and does different work, so its cost belongs to a different population;
        mixing the two is fitting a mixture.
        """
        fields = ["function_name", "input_id", "memory_after"] + self.metrics + self.properties
        with open(summary_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(fields)
            for row in self.rows.values():
                if not accepted(row):
                    continue
                w.writerow([row["function_name"], row["input_hash"], 0]
                           + [row.get(m, 0) for m in self.metrics]
                           + [row.get(p, 0) for p in self.properties])

    def write_stats(self, stats_path):
        fields = ["function_name", "input_id", "metric", "n", "mean", "std", "ci_lo", "ci_hi"]
        with open(stats_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(fields)
            for row in self.rows.values():
                for m in self.metrics:
                    w.writerow([row["function_name"], row["input_hash"], m,
                                row.get(f"{m}_n", 0), row.get(m, 0),
                                row.get(f"{m}_std", 0),
                                row.get(f"{m}_ci_lo", 0), row.get(f"{m}_ci_hi", 0)])
