"""Score a run against the manifest: did the loop find what was there?

    python src/core/score.py                      # every benchmark subject
    python src/core/score.py --subjects json,jsonpath_js
    python src/core/score.py --results results/rq1/<run>
    python src/core/score.py --csv out.csv        # machine-readable rows

Scoring reads `corpus.csv` and recomputes verdicts through `core.compare`. It
does not parse `report.md`, and it does not need the run that produced the
corpus to still be around: the corpus is the source of truth and is
checkpointed, so a rescore under a changed rule costs no SUT time. That
separation is deliberate -- the detection rule is a claim about the method, and
a claim that can only be evaluated by re-running the method is not falsifiable
cheaply.

THE RULE:

  detected            at least one REGIONAL verdict is non-equivalent, in the
                      direction the manifest expects.
  wrong_direction     non-equivalent regions exist, all pointing the other way.
  missed              every region came back equivalent, undecided, or had too
                      few paired inputs.
  false_positive      a negative control produced a non-equivalent region.
  correct_negative    a negative control produced none.
  partial             a `tradeoff` subject moved in one direction only.
  reported            an implementation set with no known ordering found a
                      difference; true by construction, not scored as a hit.
  no_difference       the same, having found none.

Regions come from `compare.by_region` over the SELECTED properties, not every
derived property, matching what a run reports. Scoring over all of them would
count one finding several times under different names and inflate detection.
"""
import argparse
import csv
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from core import compare as coreo_compare          # noqa: E402
from core import feature_select, manifest          # noqa: E402

# Columns that are bookkeeping rather than a property or a metric.
BOOKKEEPING = {"function_name", "input_hash", "first_seen_iter",
               "last_measured_iter", "accepted"}
# Suffixes the harness writes beside each metric.
STAT_SUFFIXES = ("_n", "_std", "_ci_lo", "_ci_hi")

DECIDED = ("a_faster", "b_faster")

# When the manifest claims NO property explains a pair (`explains = ()`), the
# signature of that is an effect present across the board rather than
# concentrated: a leak that costs the same on every document decides most bins
# of every property. Below this share of decided regions the effect is
# localised after all, which would contradict the claim and is worth seeing.
UNIFORM_SHARE = 0.75


def explanation(subject, decided, n_regions, selected=(), groups=None):
    """Does the property the loop surfaces match the mechanism in the diff?

    Detection is a verdict about WHETHER two systems differ; explanation is
    about WHERE, and whether that where corresponds to what the commit
    actually changed.

    Returns (outcome, evidence).
    """
    explains = subject.get("explains", None)
    if explains is None:
        return "", ""
    props = {r["prop"] for r in decided}
    if not decided:
        return "nothing_to_explain", ""
    if explains == ():
        share = len(decided) / n_regions if n_regions else 0.0
        if share >= UNIFORM_SHARE:
            return "uniform_as_claimed", f"{len(decided)}/{n_regions} regions"
        return "localised_unexpectedly", ",".join(sorted(props))
    hit = sorted(props & set(explains))
    if hit:
        return "explained", ",".join(hit)
    # A kept property that absorbed an explaining one at |rho| >= the
    # redundancy threshold IS the explanation, named by a different member of
    # the same group. The data cannot separate them, so "failed to explain"
    # understates the result and "explained" overstates it.
    groups = groups or {}
    for prop in sorted(props):
        shared = sorted(set(groups.get(prop, ())) & set(explains))
        if shared:
            return "explained_by_proxy", f"{prop} stands for {','.join(shared)}"
    # Two failures that look the same in a table and are not the same problem.
    # If the explaining property never entered the feature set, the fault is in
    # SELECTION and no amount of targeting would have found it. If it was
    # selected but no region decided on it, selection did its job and the
    # discrimination is what failed. They point at different code.
    if not set(explains) & set(selected):
        return "not_selected", ",".join(sorted(set(explains) - set(selected)))
    return "selected_not_decisive", ",".join(sorted(props))


def read_corpus(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def split_columns(fieldnames):
    """(metrics, properties) inferred from the corpus header.

    A metric is a column the harness wrote statistics beside, which is what
    distinguishes `runtime_ns` (has `runtime_ns_n`) from `n_cols` (does not).
    Reading it off the header rather than importing the subject keeps scoring
    free of every subject's import side effects, such as launching Node.
    """
    # `x_` columns are result shape (hits, matched), not properties.
    cols = [c for c in fieldnames if c not in BOOKKEEPING
            and not c.startswith("x_")]
    stats = set()
    metrics = []
    for c in cols:
        if any(c + s in fieldnames for s in STAT_SUFFIXES):
            metrics.append(c)
    for m in metrics:
        for s in STAT_SUFFIXES:
            stats.add(m + s)
    props = [c for c in cols if c not in metrics and c not in stats]
    return metrics, props


# Result-shape columns checked before two systems' timings are compared, when
# the manifest does not name them. A subject whose runner emits none of these is
# scored unfiltered and says so ("shape_checked": no).
DEFAULT_SHAPE = ("hits", "matched", "result_rows", "sat")


def agreeing_rows(rows, a, b, shape_cols):
    """Rows of `a` and `b` restricted to inputs where both gave the same answer.

    An input enters the (a, b) comparison only if both systems succeeded AND
    returned the same result shape. Timing a wrong answer against a right one
    is meaningless, and dropping the input only for this pair keeps it as
    evidence for every pair that does agree. Returns
    (rows, n_shared, n_disagree). An input one system failed on is already
    missing from `compare.paired`, so only the shape check is applied here.
    """
    if not shape_cols:
        return rows, None, 0
    by = {}
    for r in rows:
        if r["function_name"] in (a, b):
            by.setdefault(r["input_hash"], {})[r["function_name"]] = r
    bad = set()
    shared = 0
    for h, d in by.items():
        if a in d and b in d:
            shared += 1
            for c in shape_cols:
                va, vb = d[a].get(c, ""), d[b].get(c, "")
                if va in ("", None) or vb in ("", None):
                    continue
                try:
                    same = abs(float(va) - float(vb)) < 1e-9
                except ValueError:
                    same = va == vb
                if not same:
                    bad.add(h)
                    break
    if not bad:
        return rows, shared, 0
    return [r for r in rows if r["input_hash"] not in bad], shared, len(bad)


def score_pair(rows, subject, a, b, metric, props, n_bins=6, groups=None,
               relevance=None):
    """Regional verdicts for one (a, b, metric), reduced to one outcome."""
    want = manifest.expected_winner(subject, a, b)
    expected = manifest.expected_for(subject, a, b)

    regions = []
    for prop in props:
        regions.extend(coreo_compare.by_region(rows, a, b, metric, prop,
                                               n_bins=n_bins))
    decided = [r for r in regions if r["verdict"] in DECIDED]
    for_a = [r for r in decided if r["winner"] == a]
    for_b = [r for r in decided if r["winner"] == b]

    if expected == "equivalent":
        outcome = "false_positive" if decided else "correct_negative"
    elif expected == "tradeoff":
        if for_a and for_b:
            outcome = "detected"
        elif decided:
            outcome = "partial"
        else:
            outcome = "missed"
    elif want is not None:
        hits = for_a if want == a else for_b
        if hits:
            outcome = "detected"
        elif decided:
            outcome = "wrong_direction"
        else:
            outcome = "missed"
    else:
        outcome = "reported" if decided else "no_difference"

    expl, expl_evidence = explanation(subject, decided, len(regions), props,
                                      groups)
    best = max((r for r in decided),
               key=lambda r: max(r["ratio"], 1 / r["ratio"] if r["ratio"] else 1),
               default=None)
    return {
        "subject": subject["name"],
        "category": subject["category"],
        "language": subject["language"],
        "blind": subject.get("blind"),
        "a": a, "b": b, "metric": metric,
        "expected": expected if expected is not None else (want or ""),
        "n_regions": len(regions),
        "n_decided": len(decided),
        "n_for_a": len(for_a),
        "n_for_b": len(for_b),
        "outcome": outcome,
        "explanation": expl,
        "explains_expected": ",".join(subject.get("explains") or ())
                             if subject.get("explains") is not None else "",
        "explanation_evidence": expl_evidence,
        "best_ratio": round(best["ratio"], 3) if best else "",
        "best_prop": best["prop"] if best else "",
        # Reported so a weak property is visible as weak. NOT a filter: see
        # the comment in feature_select.select.
        "best_prop_relevance": (relevance or {}).get(
            best["prop"] if best else "", ""),
        "best_region": (f'{best["lo"]:.4g}-{best["hi"]:.4g}' if best else ""),
    }


def score_subject(subject, corpus_dir, max_features=4, n_bins=6):
    corpus_csv = corpus_dir / "corpus.csv"
    if not corpus_csv.exists():
        return [], f"{subject['name']}: no corpus at {corpus_csv}"
    rows = read_corpus(corpus_csv)
    if not rows:
        return [], f"{subject['name']}: corpus is empty"

    metrics, props = split_columns(list(rows[0].keys()))
    if not metrics:
        return [], f"{subject['name']}: no metric columns in the corpus header"

    # The manifest names the metric the ground truth lives on. Score that one
    # where it is present; fall back to every measured metric where the
    # manifest makes no claim.
    wanted = subject.get("expected_metrics")
    use = [m for m in (wanted or metrics) if m in metrics] or metrics[:1]

    summary = corpus_dir / "summary.csv"
    selected, groups, relevance = props, {}, {}
    if summary.exists() and props:
        try:
            selected, _, info = feature_select.select(
                str(summary), use, props, max_features=max_features,
                return_groups=True)
            groups, relevance = info["groups"], info["relevance"]
        except Exception as exc:                   # scoring must not die here
            selected = props[:max_features]
            print(f"  [{subject['name']}] property selection failed "
                  f"({type(exc).__name__}: {exc}); using the first "
                  f"{max_features} properties")

    present = {r["function_name"] for r in rows}
    header = rows[0].keys()
    shape_cols = [f"x_{c}" for c in (subject.get("shape") or DEFAULT_SHAPE)
                  if f"x_{c}" in header]
    out = []
    for a, b in manifest.pairs_to_score(subject):
        if a not in present or b not in present:
            continue
        pair_rows, shared, n_bad = agreeing_rows(rows, a, b, shape_cols)
        for metric in use:
            rec = score_pair(pair_rows, subject, a, b, metric,
                             selected, n_bins, groups, relevance)
            rec["shape_checked"] = ",".join(c[2:] for c in shape_cols) or "no"
            rec["n_shared_inputs"] = shared if shared is not None else ""
            rec["n_disagree_dropped"] = n_bad
            out.append(rec)
    if not out:
        return [], (f"{subject['name']}: no manifest system pair is present "
                    f"in the corpus (has {sorted(present)})")
    return out, None


def roll_up(rows):
    """One line per subject: the best outcome any pair/metric achieved.

    Best rather than worst, because the claim under test is that the loop finds
    the difference SOMEWHERE, and a subject measured on four metrics should not
    be marked a miss by the three the ground truth does not live on. A negative
    control inverts: there, any false positive is the subject's outcome.
    """
    rank = ["detected", "partial", "reported", "wrong_direction",
            "no_difference", "missed", "correct_negative", "false_positive"]
    order = {name: i for i, name in enumerate(rank)}
    by_subject = {}
    for r in rows:
        cur = by_subject.get(r["subject"])
        if r["expected"] == "equivalent":
            # Worst case wins for a control: one false positive is the result.
            if cur is None or order[r["outcome"]] > order[cur["outcome"]]:
                by_subject[r["subject"]] = r
        elif cur is None or order[r["outcome"]] < order[cur["outcome"]]:
            by_subject[r["subject"]] = r
    return [by_subject[k] for k in sorted(by_subject)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default=None,
                    help="a results directory holding <subject>/corpus.csv "
                         "(default: the live output/ tree)")
    ap.add_argument("--subjects", default=None,
                    help="comma-separated subset of manifest subjects")
    ap.add_argument("--csv", default=None, help="write the full rows here")
    ap.add_argument("--rq", default="RQ1",
                    help="which RQ's table to build: RQ1 (mined known pairs), "
                         "RQ1-tailored, RQ2 (latest release series), RQ3 "
                         "(competing implementations), or 'all'")
    ap.add_argument("--all", action="store_true",
                    help="include subjects the manifest excludes by default")
    ap.add_argument("--bins", type=int, default=6)
    ap.add_argument("--max-features", type=int, default=4)
    args = ap.parse_args()

    root = pathlib.Path(args.results) if args.results else REPO / "output"
    wanted = set(args.subjects.split(",")) if args.subjects else None
    rq = None if args.rq == "all" else args.rq
    subs = manifest.subjects(rq=rq,
                             include_synthetic=args.all or bool(wanted),
                             include_cross_language=args.all or bool(wanted))
    if wanted:
        subs = [s for s in manifest.SUBJECTS if s["name"] in wanted]

    rows, skipped = [], []
    for s in subs:
        got, why = score_subject(s, manifest.corpus_dir_for(s, root),
                                 max_features=args.max_features,
                                 n_bins=args.bins)
        rows.extend(got)
        if why:
            skipped.append(why)

    summary = roll_up(rows)
    print(f"\ncorpora under {root}"
          + (f"   [{args.rq}]" if args.rq != "all" else "") + "\n")
    head = (f"{'subject':<20}{'lang':<12}{'blind':<7}{'metric':<13}"
            f"{'reg':>5}{'dec':>5}  {'outcome':<17}{'explanation':<42}ratio")
    print(head)
    print("-" * len(head))
    for r in summary:
        blind = {True: "yes", False: "no", None: "?"}[r["blind"]]
        expl = r["explanation"] or "-"
        if r["explanation_evidence"]:
            expl += f" ({r['explanation_evidence']})"
        expl = expl[:40]
        print(f"{r['subject']:<20}{r['language'][:11]:<12}{blind:<7}"
              f"{r['metric'][:12]:<13}{r['n_regions']:>5}{r['n_decided']:>5}  "
              f"{r['outcome']:<17}{expl:<42}{r['best_ratio']}")

    tally = {}
    for r in summary:
        tally[r["outcome"]] = tally.get(r["outcome"], 0) + 1
    print("\n" + ", ".join(f"{v} {k}" for k, v in sorted(tally.items())))
    for line in skipped:
        print(f"  skipped: {line}")

    if args.csv:
        out = pathlib.Path(args.csv)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\n{len(rows)} rows -> {out}")


if __name__ == "__main__":
    main()
