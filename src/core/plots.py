"""Per-system comparison plots (all SUTs in a benchmark on one axes).

Reads summary.csv (means + structural properties) and, when present, joins
summary_stats.csv (per-input CIs from the rigorous measurement) to draw error
bars. One series per `function_name`, so every system in a subject appears
together for a metric-vs-property comparison.
"""
import csv
import math
import os
import statistics
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# A cost metric on one plot can run from a few hundred to a few million. On a
# linear axis the bulk of the data then collapses onto the x-axis under a
# couple of outliers.
#
# Range alone is the wrong test, because what makes a plot unreadable is skew,
# not span: a metric can cover a modest range while its median sits near the
# bottom of the axis. So trigger on either a wide span or a long tail above
# the median.
LOG_SCALE_SPAN = 50.0     # max / min
LOG_SCALE_SKEW = 10.0     # max / median


def autoscale_y(values, axis=None):
    """Use a log y-axis when a linear one would flatten the data.

    Applies only when at least two values are positive and finite, since a log
    axis cannot show zero or a censored (NaN) measurement. Returns whether the
    scale was changed, so a caller drawing error bars can keep them positive.
    """
    ax = axis or plt.gca()
    pos = [v for v in values if v is not None and math.isfinite(v) and v > 0]
    if len(pos) < 2:
        return False
    hi, lo, mid = max(pos), min(pos), statistics.median(pos)
    if hi / lo < LOG_SCALE_SPAN and (mid <= 0 or hi / mid < LOG_SCALE_SKEW):
        return False
    ax.set_yscale("log")
    return True


def _read_cis(stats_csv):
    """(function_name, input_id, metric) -> (ci_lo, ci_hi)."""
    cis = {}
    if not stats_csv or not os.path.exists(stats_csv):
        return cis
    with open(stats_csv) as f:
        for s in csv.DictReader(f):
            try:
                cis[(s["function_name"], s["input_id"], s["metric"])] = (
                    float(s["ci_lo"]), float(s["ci_hi"]))
            except (KeyError, ValueError):
                continue
    return cis


def plot_systems(summary_csv, metric, feature, output_dir, stats_csv=None):
    """Scatter of `metric` vs `feature`, one series per system, error bars if available."""
    os.makedirs(output_dir, exist_ok=True)
    cis = _read_cis(stats_csv)

    series = defaultdict(lambda: {"x": [], "y": [], "lo": [], "hi": []})
    with open(summary_csv) as f:
        for r in csv.DictReader(f):
            try:
                x = float(r[feature])
                y = float(r[metric])
            except (KeyError, ValueError):
                continue
            fn = r.get("function_name", "system")
            d = series[fn]
            d["x"].append(x)
            d["y"].append(y)
            lo, hi = cis.get((fn, r.get("input_id"), metric), (y, y))
            d["lo"].append(max(0.0, y - lo))
            d["hi"].append(max(0.0, hi - y))

    if not series:
        return None

    have_bars = bool(cis) and any(any(d["lo"]) or any(d["hi"]) for d in series.values())
    plt.figure()
    log_y = autoscale_y([y for d in series.values() for y in d["y"]])
    if log_y and have_bars:
        # A normal-approximation CI on a skewed cost metric can reach below
        # zero, which a log axis cannot draw. Truncate the lower whisker at a
        # floor just under the smallest positive value rather than dropping the
        # bar; the upper whisker, which carries the interesting spread, is kept.
        pos = [y for d in series.values() for y in d["y"] if y > 0]
        floor = min(pos) / 2.0
        for d in series.values():
            for i, y in enumerate(d["y"]):
                d["lo"][i] = min(d["lo"][i], max(0.0, y - floor))
    for fn, d in sorted(series.items()):
        if have_bars:
            plt.errorbar(d["x"], d["y"], yerr=[d["lo"], d["hi"]], fmt="o",
                         capsize=3, markersize=4, alpha=0.8, label=fn)
        else:
            plt.scatter(d["x"], d["y"], s=18, alpha=0.8, label=fn)
    plt.xlabel(feature)
    plt.ylabel(metric)
    plt.title(f"{metric} vs {feature} by system"
              + (" (95% CI)" if have_bars else "")
              + (" [log scale]" if log_y else ""))
    plt.legend()
    filename = f"systems_{metric}_vs_{feature}.png".replace(" ", "_")
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()
    return filepath


def plot_all_systems(summary_csv, metrics, features, output_dir, stats_csv=None):
    for metric in metrics:
        for feature in features:
            plot_systems(summary_csv, metric, feature, output_dir, stats_csv=stats_csv)
