"""The motivating-example figure: three panels telling the run as a story.

Subject: jsonpath_plus_latest. Pair 10.4.0 vs 11.0.0 on
runtime_ns. The axis that decides the comparison is `count_ire_regexp`, the
number of regexp sub-expressions in the query.

(a) What generating from the grammar gives you: both versions' runtime against
    input size. The clouds sit on top of each other, which is the answer a
    size-based reading produces.
(b) The same exploration corpus as per-input ratios against the number of
    regexp literals. Almost none carry one, so the axis that holds the
    answer is nearly empty and little on it can be decided.
(c) The corpus after the targeted iterations: the axis is populated and the
    ratio rises with the count.

Run with .venv/bin/python from the repo root. Writes a PDF and a PNG into
figures/, and prints the counts behind each panel.
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
from core.corpus import accepted

RUN = sorted((REPO / "results/rq1").glob("*-jsonpath_plus_latest/run1/jsonpath_plus_latest"))[-1]
OUT = REPO / "figures"
A, B = "jsonpath_plus_10_4_0", "jsonpath_plus_11_0_0"
PROP, METRIC = "count_ire_regexp", "runtime_ns"
BAND = compare.EQUIVALENCE

# Validated two-slot categorical palette (the dataviz skill's
# validate_palette.js, light mode: all checks pass; normal-vision dE 33.6,
# protan 24.7). Marker shape repeats the distinction, so the figure survives
# greyscale printing.
C_OLD = "#2a78d6"      # 10.4.0, and the targeted corpus
C_NEW = "#eb6834"      # 11.0.0, and the exploration corpus
INK = "#0b0b0b"
MUTED = "#52514e"
GRID = "#d9d8d4"


def _f(row, key):
    try:
        v = float(row[key])
        return v if v == v else None
    except (TypeError, ValueError, KeyError):
        return None


def load():
    rows = list(csv.DictReader(open(RUN / "corpus.csv")))
    per_input = {}
    for r in rows:
        h = r["input_hash"]
        d = per_input.setdefault(h, {"iter": int(float(r["first_seen_iter"]))})
        d[PROP] = _f(r, PROP) or 0.0
        d["bytes"] = (_f(r, "doc_bytes") or 0) + (_f(r, "query_len") or 0)
        rt = _f(r, METRIC)
        if rt and rt > 0 and accepted(r):
            d[r["function_name"]] = rt
    usable = {h: d for h, d in per_input.items() if A in d and B in d}
    for d in usable.values():
        d["ratio"] = d[B] / d[A]
    return rows, usable


def style():
    plt.rcParams.update({
        "font.family": "serif", "font.size": 8, "axes.labelsize": 8,
        "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "figure.dpi": 200,
    })


def ratio_axis(ax):
    """Shared geometry for the two ratio panels, so (b) and (c) compare."""
    ax.axhspan(1 / BAND, BAND, color=GRID, alpha=0.55, lw=0, zorder=0)
    ax.axhline(1.0, color=MUTED, lw=0.6, zorder=1)
    ax.set_xscale("symlog", linthresh=1, linscale=0.45)
    ax.set_xlim(-0.3, 130)
    ax.set_xticks([0, 1, 10, 100], ["0", "1", "10", "100"])
    ax.set_ylim(0.93, 1.45)
    ax.set_yticks([1.0, 1.1, 1.2, 1.3, 1.4],
                  ["1.0x", "1.1x", "1.2x", "1.3x", "1.4x"])
    ax.grid(color=GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def main():
    rows, inputs = load()
    explore = {h: d for h, d in inputs.items() if d["iter"] == 0}
    targeted = {h: d for h, d in inputs.items() if d["iter"] > 0}
    style()
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.2, 2.05))
    fig.subplots_adjust(wspace=0.36)

    # ---- (a) runtime against size: the two versions overlap -------------
    for ver, colour, marker, lbl in ((A, C_OLD, "o", "10.4.0"),
                                     (B, C_NEW, "^", "11.0.0")):
        ax1.scatter([d["bytes"] for d in explore.values()],
                    [d[ver] / 1e6 for d in explore.values()],
                    s=9, c=colour, marker=marker, alpha=0.55, linewidths=0,
                    zorder=3, label=lbl)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("input size (bytes)")
    ax1.set_ylabel("runtime (ms)")
    ax1.set_title("(a) Generate and measure:\nthe versions look alike",
                  loc="left", pad=6)
    ax1.grid(color=GRID, lw=0.5, zorder=0)
    ax1.set_axisbelow(True)
    for s in ("top", "right"):
        ax1.spines[s].set_visible(False)
    ax1.legend(frameon=False, fontsize=6.5, loc="upper left",
               handletextpad=0.2, borderpad=0.2, labelspacing=0.25)

    # ---- (b) the deciding axis is empty ---------------------------------
    ratio_axis(ax2)
    xs = [d[PROP] for d in explore.values()]
    ax2.scatter(xs, [d["ratio"] for d in explore.values()], s=11,
                facecolors="none", edgecolors=C_NEW, linewidths=0.9, zorder=3)
    ax2.annotate(f"{sum(1 for v in xs if v == 0)} of {len(xs)} inputs\ncarry no regexp",
                 (0, 1.30), fontsize=6.5, color=MUTED, ha="left",
                 xytext=(5, 0), textcoords="offset points")
    ax2.annotate("nothing generated here", (2.6, 1.045), fontsize=6.5,
                 color=MUTED, ha="left")
    ax2.annotate("", xy=(110, 1.02), xytext=(2.6, 1.02),
                 arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7,
                                 shrinkA=0, shrinkB=0))
    ax2.set_xlabel("regexp sub-expressions in the query")
    ax2.set_ylabel("runtime of 11.0.0 relative to 10.4.0")
    ax2.set_title("(b) Decompose by property:\nthe axis is unexplored",
                  loc="left", pad=6)

    # ---- (c) after targeting that axis ----------------------------------
    ratio_axis(ax3)
    ax3.scatter([d[PROP] for d in explore.values()],
                [d["ratio"] for d in explore.values()], s=11,
                facecolors="none", edgecolors=C_NEW, linewidths=0.9, zorder=3,
                label="from exploration")
    ax3.scatter([d[PROP] for d in targeted.values()],
                [d["ratio"] for d in targeted.values()], s=9, c=C_OLD,
                marker="o", alpha=0.5, linewidths=0, zorder=4,
                label="from requests")
    # Region medians: the verdicts the text quotes, drawn where they hold.
    for reg in compare.by_region(rows, A, B, METRIC, PROP):
        if reg.get("ratio") and reg["verdict"] in ("a_faster", "b_faster"):
            lo = reg["lo"] if reg["lo"] > 0 else -0.15
            ax3.plot([lo, reg["hi"]], [reg["ratio"]] * 2, color=INK, lw=1.4,
                     zorder=6, solid_capstyle="butt")
    ax3.annotate("region medians,\n1.16x to 1.21x", (1.6, 1.30), fontsize=6.5,
                 color=INK, ha="left")
    ax3.set_xlabel("regexp sub-expressions in the query")
    ax3.set_title("(c) Generate along it:\nthe difference appears",
                  loc="left", pad=6)
    ax3.legend(frameon=False, fontsize=6.5, loc="lower right",
               handletextpad=0.2, borderpad=0.2, labelspacing=0.25)

    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"motivating_jsonpath_plus.{ext}", bbox_inches="tight")
    print("wrote", OUT / "motivating_jsonpath_plus.pdf")
    print(f"explore usable={len(explore)} "
          f"(with a regexp: {sum(1 for d in explore.values() if d[PROP] > 0)}), "
          f"targeted usable={len(targeted)}, "
          f"max regexps={max(d[PROP] for d in inputs.values()):.0f}")


if __name__ == "__main__":
    main()
