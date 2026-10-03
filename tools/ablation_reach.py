"""Score the ablation arms on one fixed region set: what each arm reaches.

This is the number the paper's Motivating Example cites: generating from the
specification grammar with the fuzzer's defaults never produces a query carrying
a regular expression, so the axis along which the two releases differ cannot be
looked at.

`src/core/ablate.py` runs the arms and this script scores their corpora
directly. Regions are computed ONCE over the union of all arms, before any arm
is scored, so an arm cannot win by shaping the bins it is measured on.

    .venv/bin/python tools/ablation_reach.py

Reproduce the arms first with:

    .venv/bin/python src/core/ablate.py jsonpath_plus_latest --runs 1 \
        --budget 100 --arms fandango,fandango_tuned,guided \
        --out output/_ablate_jsonpath_plus
"""
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from core import compare

ROOT = REPO / "output/_ablate_jsonpath_plus/run1"
ARMS = ("fandango", "fandango_tuned", "stratified", "guided")
A, B = "jsonpath_plus_10_4_0", "jsonpath_plus_11_0_0"
PROP, METRIC = "count_ire_regexp", "runtime_ns"


def main():
    corpora = {}
    for arm in ARMS:
        f = ROOT / arm / "corpus.csv"
        corpora[arm] = list(csv.DictReader(open(f))) if f.exists() else []

    union = [r for rows in corpora.values() for r in rows]
    if not union:
        sys.exit(f"no arm corpora under {ROOT}; run ablate.py first")
    bins = compare.property_bins([float(r[PROP] or 0) for r in union], 6)

    print(f"pair: {A} vs {B} on {METRIC}, property {PROP}")
    print("regions (fixed over the union of all arms): "
          + ", ".join(f"[{lo:g},{hi:g}]" for lo, hi in bins))
    print(f"\n{'arm':16s} {'inputs':>6} {'max':>5} {'with a regexp':>13} "
          f"{'regions decided':>15}  pooled")
    for arm in ARMS:
        rows = corpora[arm]
        if not rows:
            print(f"{arm:16s} {'(no corpus)':>6}")
            continue
        prop_of = {r["input_hash"]: float(r[PROP] or 0) for r in rows}
        paired = compare.paired(rows, METRIC)
        decided = tested = 0
        for k, (lo, hi) in enumerate(bins):
            sub = {h: d for h, d in paired.items()
                   if h in prop_of
                   and compare.in_region(prop_of[h], lo, hi, k == len(bins) - 1)}
            v = compare.compare_pair(sub, A, B, METRIC)
            if v:
                tested += 1
                decided += v["verdict"] in ("a_faster", "b_faster")
        pooled = compare.compare_pair(paired, A, B, METRIC)
        print(f"{arm:16s} {len(set(prop_of)):6d} {max(prop_of.values()):5.0f} "
              f"{sum(1 for v in prop_of.values() if v > 0):13d} "
              f"{decided:7d}/{tested:<7d}  "
              + (f"{pooled['ratio']:.3f} {pooled['verdict']}" if pooled else "-"))


if __name__ == "__main__":
    main()
