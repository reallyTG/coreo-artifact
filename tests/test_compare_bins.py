"""The binning invariant in `core.compare.property_bins`.

Every input with a finite property value must land in exactly one region.
Bins built from positive values only would leave inputs at 0 in no region at
all, and 0 is the commonest value a grammar count takes. These checks fail on
such a binning.

Runs as a plain script (`.venv/bin/python tests/test_compare_bins.py`), since
the venv has no pytest; the `test_` functions also collect under pytest.
"""
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from core import compare  # noqa: E402


def _check_exactly_once(values, bins):
    last = len(bins) - 1
    bad = []
    for v in values:
        c = sum(compare.in_region(v, lo, hi, i == last)
                for i, (lo, hi) in enumerate(bins))
        if c != 1:
            bad.append((v, c))
    assert not bad, f"values not in exactly one region: {bad[:5]} with bins {bins}"


def test_every_value_in_exactly_one_region():
    rng = random.Random(0)
    cases = [
        # Count with many zeros and a wide span.
        [0] * 421 + [rng.randint(1, 11) for _ in range(137)],
        # Wide count, no zeros.
        [rng.randint(1, 2285) for _ in range(500)] + [1, 2285],
        # Bounded fraction with zeros.
        [0.0] * 42 + [rng.uniform(0.25, 1.0) for _ in range(300)] + [0.25, 1.0],
        # Too narrow to split; single distinct positive; all zero; binary 0/1.
        [100, 120, 150, 199],
        [5, 5, 5],
        [0, 0, 0],
        [0, 1, 1, 0, 1],
        # Negatives, which no shipped property produces but nothing forbids.
        [-3.0, -1.0, 0.0, 2.0, 40.0],
        [-3.0, -2.0, -1.0],
    ]
    for values in cases:
        bins = compare.property_bins(values, 6)
        _check_exactly_once(values, bins)
        # Edges are where half-open intervals go wrong: a value sitting exactly
        # on an inner edge must go to one side, never both and never neither.
        edges = [e for b in bins for e in b if min(values) <= e <= max(values)]
        _check_exactly_once(edges, bins)


def test_zero_gets_its_own_region_first():
    bins = compare.property_bins([0, 0, 1, 3, 11], 6)
    assert bins[0] == (0.0, 0.0), bins
    assert all(lo > 0 for lo, _ in bins[1:]), bins
    # No zero present -> no zero region.
    assert compare.property_bins([1, 3, 11], 6)[0][0] == 1


def test_bounded_property_gets_equal_width_bins():
    bins = compare.property_bins([0.0, 0.25, 0.5, 0.75, 1.0], 6)
    widths = [hi - lo for lo, hi in bins[1:]]
    assert len(widths) == 6 and max(widths) - min(widths) < 1e-12, bins


def test_wide_property_gets_equal_ratio_bins():
    bins = compare.property_bins([1, 10, 100, 2285], 6)
    ratios = [hi / lo for lo, hi in bins]
    assert len(ratios) == 6 and max(ratios) - min(ratios) < 1e-9, bins
    assert bins[0][0] == 1 and bins[-1][1] == 2285


def test_labels():
    assert compare.region_label(0.0, 0.0) == "=0"
    assert compare.region_label(1, 3.5) == "[1,3.5)"
    assert compare.region_label(1, 3.5, last=True) == "[1,3.5]"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
