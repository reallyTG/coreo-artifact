"""The verdict rule, and how an unsettled region becomes a request.

(a) Schematic: where a region's confidence interval sits relative to the
    equivalence band gives one of five answers.
(b) The same rule on the real regions of the running example
    (jsonpath_plus_latest, 10.4.0 vs 11.0.0, by regexp literals in the query).
    The region the corpus cannot decide is rewritten into the production that
    governs the property, which is what the next round of generation samples.

Run with .venv/bin/python from the repo root.
"""
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

from core import compare

RUN = sorted((REPO / "results/rq1").glob("*-jsonpath_plus_latest/run1/jsonpath_plus_latest"))[-1]
OUT = REPO / "figures"
A, B = "jsonpath_plus_10_4_0", "jsonpath_plus_11_0_0"
PROP, METRIC = "count_ire_regexp", "runtime_ns"
BAND = compare.EQUIVALENCE

C_DEC = "#2a78d6"      # decided
C_OPEN = "#eb6834"     # not decided: undecided or insufficient
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d4"

def main():
    rows = list(csv.DictReader(open(RUN / "corpus.csv")))
    regions = compare.by_region(rows, A, B, METRIC, PROP)

    plt.rcParams.update({
        "font.family": "serif", "font.size": 8, "axes.labelsize": 7.5,
        "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "figure.dpi": 200,
    })
    fig, ax1 = plt.subplots(figsize=(3.3, 1.2))

    # ---- (a) the rule --------------------------------------------------
    cases = [
        ("$A$ cheaper",   1.18, 1.30, C_DEC),
        ("$B$ cheaper",   0.74, 0.86, C_DEC),
        ("equivalent",    0.95, 1.06, C_DEC),
        ("undecided",     1.04, 1.21, C_OPEN),
        ("insufficient",  None, None, C_OPEN),
    ]
    ax1.axvspan(1 / BAND, BAND, color=GRID, alpha=0.6, lw=0, zorder=0)
    ax1.axvline(1.0, color=MUTED, lw=0.6, zorder=1)
    for y, (label, lo, hi, colour) in zip(range(len(cases))[::-1], cases):
        if lo is None:
            ax1.annotate("fewer than eight paired inputs", (0.70, y),
                         fontsize=6.5, color=MUTED, va="center", ha="left")
        else:
            ax1.plot([lo, hi], [y, y], color=colour, lw=1.8, zorder=3,
                     solid_capstyle="round")
            ax1.plot([(lo + hi) / 2], [y], marker="o", ms=4, color=colour, zorder=4)
        ax1.annotate(label, (0.655, y), fontsize=7, color=INK, va="center",
                     ha="right", annotation_clip=False)
    ax1.text(1.0, len(cases) - 0.35, "equivalence band", fontsize=6.5,
             color=MUTED, ha="center", va="bottom")
    ax1.set_xlim(0.68, 1.38)
    ax1.set_xticks([1 / BAND, 1.0, BAND], ["$1/\\delta$", "1", "$\\delta$"])
    ax1.set_ylim(-0.6, len(cases) - 0.3)
    ax1.set_yticks([])
    ax1.set_xlabel("confidence interval on the median ratio in a region")
    ax1.set_title("The verdict rule", loc="left", pad=5)
    for s in ("top", "right", "left"):
        ax1.spines[s].set_visible(False)

    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"verdicts.{ext}", bbox_inches="tight")
    print("wrote", OUT / "verdicts.pdf")
    print("regions on file:", len(regions))

if __name__ == "__main__":
    main()
