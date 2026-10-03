"""A crossover: which system is cheaper depends on the input.

Subject: selectors_js, css-select against dom-selector on
runtime, by the number of type selectors in the query. The winner changes
along the axis; the script prints each region's verdict.

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

from core import compare

RUN = sorted((REPO / "results/rq1").glob("*-selectors_js/run1/selectors_js"))[-1]
OUT = REPO / "figures"
A, B = "cssselect", "domselector"
PROP, METRIC = "count_type_selector", "runtime_ns"
BAND = compare.EQUIVALENCE

C_A, C_B = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d4"


def main():
    rows = list(csv.DictReader(open(RUN / "corpus.csv")))
    regions = compare.by_region(rows, A, B, METRIC, PROP)

    plt.rcParams.update({
        "font.family": "serif", "font.size": 8, "axes.labelsize": 8,
        "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "figure.dpi": 200,
    })
    fig, ax = plt.subplots(figsize=(3.3, 1.9))
    ax.axhspan(1 / BAND, BAND, color=GRID, alpha=0.6, lw=0, zorder=0)
    ax.axhline(1.0, color=MUTED, lw=0.6, zorder=1)

    xs, ys, los, his, colours = [], [], [], [], []
    for r in regions:
        if not r.get("ratio"):
            continue
        lo = r["lo"] if r["lo"] > 0 else 0.55
        hi = r["hi"] if r["hi"] > 0 else 0.8
        mid = (lo * hi) ** 0.5
        xs.append(mid); ys.append(r["ratio"])
        los.append(r["ci"][0]); his.append(r["ci"][1])
        colours.append(C_A if r["ratio"] > 1 else C_B)
    ax.plot(xs, ys, color=MUTED, lw=0.8, zorder=2, alpha=0.6)
    for x, y, lo, hi, c in zip(xs, ys, los, his, colours):
        ax.plot([x, x], [lo, hi], color=c, lw=1.3, solid_capstyle="round", zorder=3)
        ax.plot(x, y, marker="o", ms=4.5, color=c, zorder=4)

    ax.set_xscale("symlog", linthresh=1, linscale=0.4)
    ax.set_yscale("log")
    ax.set_xlim(-0.25, 90)
    ax.set_xticks([0, 1, 10, 59], ["0", "1", "10", "59"])
    from matplotlib.ticker import NullFormatter, NullLocator
    ax.set_yticks([0.2, 0.5, 1, 2, 3], ["0.2x", "0.5x", "1x", "2x", "3x"])
    ax.yaxis.set_minor_locator(NullLocator())      # log minors add 6x10^0 noise
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_ylim(0.15, 7.5)
    ax.set_xlabel("type selectors in the query")
    ax.set_ylabel("dom-selector / css-select")
    ax.annotate("css-select cheaper", (2.2, 4.6), fontsize=6.5, color=C_A,
                ha="left", va="center")
    ax.annotate("dom-selector cheaper", (12, 0.26), fontsize=6.5, color=C_B,
                ha="left", va="center")
    ax.grid(color=GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"crossover.{ext}", bbox_inches="tight")
    print("wrote", OUT / "crossover.pdf")
    for r in regions:
        print(f"  [{r['lo']:.3g},{r['hi']:.3g}] n={r['n']:3d} "
              f"{r.get('ratio', float('nan')):.2f} {r['verdict']}")


if __name__ == "__main__":
    main()
