"""How the reported relationship forms as the loop runs.

Subject: jsonpath_plus_latest, pair 10.4.0 vs 11.0.0 on
runtime_ns, against `count_ire_regexp` (regexp literals in the query).

(a) Every input the corpus holds, placed at the iteration that first produced it
    and at its position on the property axis. Iteration 0 is the stratified
    exploration; the rest are targeted.
(b) The verdict over the inputs whose query carries a regular expression, as the
    corpus grows: the median ratio with its 95% interval against the
    equivalence band. A verdict needs at least eight paired inputs.

Run with .venv/bin/python from the repo root.
"""
import csv
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from core import compare

RUN = sorted((REPO / "results/rq1").glob("*-jsonpath_plus_latest/run1/jsonpath_plus_latest"))[-1]
OUT = REPO / "figures"
A, B = "jsonpath_plus_10_4_0", "jsonpath_plus_11_0_0"
PROP, METRIC = "count_ire_regexp", "runtime_ns"
BAND = compare.EQUIVALENCE

C_EXPL = "#eb6834"     # exploration (iteration 0)
C_LOOP = "#2a78d6"     # targeted iterations
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d4"


def main():
    rows = list(csv.DictReader(open(RUN / "corpus.csv")))
    prop = {r["input_hash"]: float(r[PROP] or 0) for r in rows}
    seen = {r["input_hash"]: int(float(r["first_seen_iter"])) for r in rows}
    iters = sorted(set(seen.values()))

    plt.rcParams.update({
        "font.family": "serif", "font.size": 8, "axes.labelsize": 8,
        "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "figure.dpi": 200,
    })
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 1.95))
    fig.subplots_adjust(wspace=0.28)

    # ---- (a) where each input landed, and when ---------------------------
    rng = random.Random(0)
    for k in iters:
        hs = [h for h, i in seen.items() if i == k]
        ys = [prop[h] for h in hs]
        xs_j = [k + rng.uniform(-0.3, 0.3) for _ in ys]
        ax1.scatter(xs_j, ys, s=5, alpha=0.3, linewidths=0,
                    c=C_EXPL if k == 0 else C_LOOP, zorder=3)
    ax1.set_yscale("symlog", linthresh=1, linscale=0.4)
    ax1.set_yticks([0, 1, 10, 100], ["0", "1", "10", "100"])
    ax1.set_ylim(-0.3, 130)
    ax1.set_xticks(iters[::2])
    ax1.set_xlabel("iteration that first produced the input")
    ax1.set_ylabel("regexp sub-expressions in the query")
    ax1.set_title("(a) The corpus filling the axis", loc="left", pad=6)
    ax1.annotate("exploration", (0, 60), fontsize=6.5, color=C_EXPL, ha="left",
                 xytext=(4, 0), textcoords="offset points")
    ax1.grid(color=GRID, lw=0.5, zorder=0)
    ax1.set_axisbelow(True)
    for s in ("top", "right"):
        ax1.spines[s].set_visible(False)

    # ---- (b) the verdict as evidence accumulates -------------------------
    ax2.axhspan(1 / BAND, BAND, color=GRID, alpha=0.55, lw=0, zorder=0)
    ax2.axhline(1.0, color=MUTED, lw=0.6, zorder=1)
    xs, mids, los, his = [], [], [], []
    for k in iters:
        sub = [r for r in rows
               if seen[r["input_hash"]] <= k and prop[r["input_hash"]] >= 1]
        v = compare.compare_pair(compare.paired(sub, METRIC), A, B, METRIC)
        if v is None:
            continue
        xs.append(k); mids.append(v["ratio"])
        los.append(v["ci"][0]); his.append(v["ci"][1])
    ax2.fill_between(xs, los, his, color=C_LOOP, alpha=0.2, lw=0, zorder=2)
    ax2.plot(xs, mids, color=C_LOOP, lw=1.4, marker="o", ms=3.5, zorder=4)
    ax2.axvline(0.5, color=MUTED, lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax2.annotate("iteration 0 holds two such inputs\nthat can be compared: no verdict",
                 (0.7, 1.035), fontsize=6.5, color=C_EXPL, ha="left", va="center")
    ax2.set_xticks(iters[::2])
    ax2.set_ylim(0.96, 1.30)
    ax2.set_yticks([1.0, 1.1, 1.2, 1.3], ["1.0x", "1.1x", "1.2x", "1.3x"])
    ax2.set_xlabel("corpus after iteration")
    ax2.set_ylabel("runtime of 11.0.0 relative to 10.4.0")
    ax2.set_title("(b) The verdict on regexp-carrying inputs",
                  loc="left", pad=6)
    ax2.grid(color=GRID, lw=0.5, zorder=0)
    ax2.set_axisbelow(True)
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)

    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"corpus_evolution.{ext}", bbox_inches="tight")
    print("wrote", OUT / "corpus_evolution.pdf")
    print("verdict first available at iteration", xs[0],
          f"({mids[0]:.3f}, CI {los[0]:.3f}-{his[0]:.3f});",
          f"final {mids[-1]:.3f}, CI {los[-1]:.3f}-{his[-1]:.3f}")


if __name__ == "__main__":
    main()
