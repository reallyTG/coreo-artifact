"""The labelled benchmark: what each subject is, and what the right answer is.

Each entry carries the scoreable facts of one subject: category, systems,
expected verdict, and whether the grammar was written before anyone read the
diff. A subject's docstring explains it; this module is what gets scored.

WHICH RQ A SUBJECT SERVES

  RQ1  mined known pairs. A `*_known` subject runs them on the frozen
       specification grammar (the blind setting), a `*_tailored` subject on a
       grammar shaped from the commit's diff.
  RQ2  latest release series, preregistered, with no known answer.
  RQ3  competing implementations of one specification.

CATEGORIES, scored by different rules:

  known           release pairs around mined performance commits. Ground truth
                  is the diff, so there is a right answer and a direction.
  series          the last releases of one library as adjacent pairs. No
                  ground truth: a decided region is a lead to triage.
  implementations several independent implementations of ONE specification.
                  There is no diff and usually no known ordering, so a verdict
                  is reported rather than marked right or wrong.
  pair            one before/after pair. The only one here is the nwsapi
                  control, scored out of the selectors_js corpus.

DETECTION RULE, fixed before any evaluation run: a subject counts
as detected when at least one REGIONAL verdict comes back non-equivalent with
the direction the manifest expects. Not the pooled verdict, which can sit
inside the equivalence band while one region moves. Not "any region in any
direction" either: direction is checked wherever the manifest knows it.

`blind` is a separate axis from `expected`, and it is the one a reviewer will
press on. It records whether the grammar could already express the region the
effect lives in BEFORE the diff was read. Where it is False, the subject shows
that the loop closes once the grammar reaches the inputs that matter, which is
a weaker claim than rediscovery and has to be reported as the weaker claim.
"""

# Expected-verdict vocabulary, matching core.compare's own:
#   "a_faster"    system a is cheaper: b is the regression
#   "b_faster"    system b is cheaper: b is the fix
#   "tradeoff"    both directions occur in different regions (a crossover)
#   "equivalent"  no difference anywhere -- a NEGATIVE CONTROL
#   None          no known ordering; report, do not score for direction
EXPECTED = ("a_faster", "b_faster", "tradeoff", "equivalent", None)

SUBJECTS = [
    # ---------------------------------------------------------------- pairs

    {
        "name": "selectors_js_pair",
        "rqs": ("control",),
        "mechanism": None,
        "explains": None,
        "category": "pair",
        "language": "JavaScript",
        "project": "dperini/nwsapi",
        # Scored out of the selectors_js corpus: both releases are already
        # measured there on the same inputs, so this pair costs no build and
        # no run. A `pair` entry drawn from another subject's corpus.
        "corpus_from": "selectors_js",
        "systems": ("nwsapi_prev", "nwsapi"),
        "change": "2.2.25 -> 2.2.27, spanning the 2026 rewrite",
        "expected": "equivalent",
        "expected_metrics": ("runtime_ns",),
        "blind": True,
        "note": "A negative control, and a narrow one. "
                "The documented 270x slowdown (upstream #171) is the "
                ":fullscreen pseudo-class: 2.2.26 evaluates it via "
                "matchesNative -> Element.matches, and where Element.matches "
                "IS nwsapi that re-enters itself ~940 frames deep until the "
                "stack unwinds. Reproduced here at ~230x (2.3ms -> 530ms) by "
                "routing Element.matches back into the nwsapi under test.\n"
                "THREE barriers make it unreachable for this subject, and "
                "they are independent:\n"
                "  (1) GRAMMAR. <qualifier> offers class, id, [class=..], "
                ":nth-child, :not and :is. No pseudo-STATE class exists in the "
                "language, so :fullscreen cannot be generated at all.\n"
                "  (2) ENVIRONMENT. The subject pins jsdom 30.1.0, which uses "
                "@asamuzakjp/dom-selector for Element.matches and does not "
                "depend on nwsapi. The re-entrancy needs jsdom < 30, where "
                "nwsapi IS the matcher. Under this subject's wiring "
                ":fullscreen costs 4-8ms on all three versions.\n"
                "  (3) SUPPORT. 2.2.25 throws ReferenceError on :fullscreen -- "
                "it did not implement the pseudo-class -- so across the pair "
                "this is support versus non-support, not a like-for-like "
                "timing comparison.\n"
                "SO: 'equivalent' here means equivalent ON THE REACHABLE "
                "LANGUAGE, not equivalent in general. It still works as a "
                "control -- a reported difference on reachable inputs would be "
                "a genuine false positive -- but it must NOT be read as "
                "evidence that these releases do not differ. 2.2.27 does not "
                "fix #171 either: measured 318ms against 2.2.25's 2.3ms, and "
                "the reporter says the same.",
    },

    # ------------------------------------------------------- implementations
    {
        "name": "json",
        "rqs": ("RQ3",),
        "category": "implementations",
        "language": "Python",
        "project": "orjson / ujson / stdlib json / simplejson",
        "systems": ("json_orjson", "json_ujson", "json_stdlib",
                    "json_simplejson"),
        "expected_order": ("json_orjson", "json_ujson", "json_stdlib",
                           "json_simplejson"),
        "expected": None,
        "expected_metrics": ("runtime_ns",),
        "blind": True,
        "note": "The one implementation set with a widely believed ordering, "
                "so it doubles as a sanity check on the comparison engine. "
                "K-repeat parsing, because str(tree) at ~1900 ns/byte is the "
                "in-process measurement floor.",
    },
    {
        "name": "jsonpath_js",
        "rqs": ("RQ3",),
        "category": "implementations",
        "language": "JavaScript",
        "project": "five independent JSONPath implementations",
        "systems": ("dchester", "jsonpathly", "p3", "plus", "rfc9535"),
        "expected": None,
        "expected_metrics": ("runtime_ns",),
        "blind": True,
        "note": "Three findings came out of it: "
                "quadratic result accumulation in jsonpathly and in dchester's "
                "jsonpath, and a RangeError in json-p3.",
    },
    {
        "name": "jsonpath_py",
        "rqs": ("RQ3",),
        "category": "implementations",
        "language": "Python",
        "project": "four independent JSONPath implementations",
        "systems": ("ng", "jpython", "pyjsonpath", "rfc9535"),
        "expected": None,
        "expected_metrics": ("runtime_ns",),
        "blind": True,
        "note": "jsonpath-ng raises on $.a[0] over "
                "{'a': 1}.",
    },
    {
        "name": "selectors_js",
        "rqs": ("RQ3",),
        "category": "implementations",
        "language": "JavaScript",
        "project": "nwsapi / nwsapi_prev / dom-selector / css-select",
        "systems": ("nwsapi", "nwsapi_prev", "cssselect", "domselector"),
        "expected": None,
        "expected_metrics": ("runtime_ns",),
        "blind": True,
        "note": "Carries a version pair INSIDE an implementation set: nwsapi "
                "2.2.27 against 2.2.25. Two findings: nwsapi rejects valid "
                "pseudo + [attr] selectors (a regression in 2.2.12, 35M "
                "downloads/week, reached through jsdom<30 and jest) and "
                "overflows its stack on long selectors.",
    },
    {
        "name": "sql_js",
        "rqs": ("RQ3",),
        "category": "implementations",
        "language": "JavaScript",
        "project": "pgsql-ast-parser / sql-formatter / sql-cst",
        "systems": ("pgsql", "formatter", "cst"),
        "expected": None,
        "expected_metrics": ("runtime_ns",),
        "blind": True,
        "note": "pgsql-ast-parser reports 'Ambiguous SQL syntax' on 32% of "
                "generated statements that are valid per PostgreSQL's own "
                "grammar -- found from the failure ledger, not the metrics.",
    },
]

# ------------------------------------------------------------ latest series
# For each domain, the most-downloaded
# implementation with at least six non-prerelease releases; its last six
# releases give five ADJACENT pairs. Chosen and preregistered mechanically in
# eval/latest_series_2026-09-30.json (timestamped 2026-09-30T21:06Z), before
# the domain grammars were frozen and before any version was measured. So these
# are blind by construction: nobody knew an answer to leak.
#
# `series` is its own category because a pair has exactly one (before, after)
# and a series has five; pairs_to_score returns the adjacent ones, oldest
# first, so a verdict "b_faster" always means the newer release is cheaper.
# expected is None: a latest pair has no ground truth, and any non-equivalent
# regional verdict is a lead to triage, not a score.
def _series(name, lib, prefix, language, versions, domain, first_batch, note="",
            shape=None):
    return {
        "name": name, "rqs": ("RQ2",), "category": "series",
        "language": language, "project": lib, "domain_subject": domain,
        "systems": tuple(prefix + v.replace(".", "_") for v in versions),
        "versions": tuple(versions),
        "expected": None, "expected_metrics": ("runtime_ns",),
        "blind": True, "first_batch": first_batch,
        **({"shape": shape} if shape is not None else {}),
        "note": "Latest release series, preregistered. " + note,
    }


SUBJECTS += [
    _series("sql_formatter_latest", "sql-formatter", "sql_formatter_",
            "JavaScript", ("15.7.3", "15.7.4", "15.8.0", "15.8.1", "15.8.2",
                           "15.9.0"), "sql_js", True,
            "`nodes` is not used as a shape check: it counts the formatter's "
            "own parse tree, which a release may legitimately restructure.",
            shape=()),
    _series("orjson_latest", "orjson", "orjson_", "Python",
            ("3.11.5", "3.11.6", "3.11.7", "3.11.8", "3.11.9", "3.12.0"),
            "json", True,
            "Measured out of process with the domain's K_PARSE loop, unlike "
            "the in-process json subject; comparable within the series only."),
    _series("jsonpath_plus_latest", "jsonpath-plus", "jsonpath_plus_",
            "JavaScript", ("10.2.0", "10.3.0", "10.4.0", "11.0.0", "11.0.1",
                           "11.1.0"), "jsonpath_js", True,
            "11.0.0 replaced JSONPath.cache with clearCache(); the runner "
            "clears whichever exists so every version times parse+evaluate."),
    _series("css_select_latest", "css-select", "css_select_", "JavaScript",
            ("5.1.0", "5.2.0", "5.2.2", "6.0.0", "7.0.0"), "selectors_js",
            False,
            "5.2.1 is preregistered but a broken publish (tarball lacks "
            "lib/compile.js, require throws), so it cannot be measured; its "
            "neighbours 5.2.0 and 5.2.2 are scored as adjacent instead."),
    _series("jsonpath_ng_latest", "jsonpath-ng", "jsonpath_ng_", "Python",
            ("1.5.2", "1.5.3", "1.6.0", "1.6.1", "1.7.0", "1.8.0"),
            "jsonpath_py", False),
]

# ------------------------------------------------------------- known pairs
# RQ1, blind setting. Performance commits mined from every spec-domain
# SUT since 2024-01-01 by one keyword rule, triaged through a fixed funnel
# (perf change -> input-dependent -> expressible by the frozen grammar), and
# mapped to the release pair around the commit. Per library, at most the five
# most recent expressible pairs are measured. Funnel rows and reasons are in
# eval/known_pairs/*.csv. Grammars were frozen on 2026-09-30, before the
# mining, so every pair is blind with respect to the grammar.
# Expected verdict per pair is "b_faster" (the later release is cheaper)
# unless the funnel predicted no effect.
def _known(name, lib, prefix, language, versions, pairs, domain,
           expected=None, note="", shape=None):
    sysname = lambda v: prefix + v.replace(".", "_")
    pl = [(sysname(a), sysname(b)) for a, b in pairs]
    exp = expected or {}
    return {
        "name": name, "rqs": ("RQ1",), "category": "known",
        "language": language, "project": lib, "domain_subject": domain,
        "systems": tuple(sysname(v) for v in versions),
        "versions": tuple(versions), "pairs": tuple(pl),
        "pair_expected": {(sysname(a), sysname(b)): exp.get((a, b), "b_faster")
                          for a, b in pairs},
        "expected": "b_faster", "expected_metrics": ("runtime_ns",),
        "blind": True,
        **({"shape": shape} if shape is not None else {}),
        "note": "Mined known pairs (RQ1, blind). " + note,
    }


SUBJECTS += [
    _known("nwsapi_known", "nwsapi", "nwsapi_", "JavaScript",
           ("2.2.21", "2.2.22", "2.2.23", "2.2.24", "2.2.25", "2.2.26", "2.2.27"),
           [("2.2.26", "2.2.27"), ("2.2.25", "2.2.26"), ("2.2.24", "2.2.25"),
            ("2.2.23", "2.2.24"), ("2.2.21", "2.2.22")], "selectors_js",
           note="2.2.26 also carries the #171 slowdown, unreachable by the "
                "grammar; several pairs include correctness fixes, handled by "
                "the shape check."),
    _known("domselector_known", "@asamuzakjp/dom-selector", "domselector_",
           "JavaScript",
           ("8.2.4", "8.2.5", "9.0.3", "9.0.4", "9.1.0", "9.1.1", "9.1.2",
            "9.2.1", "9.2.2"),
           [("9.2.1", "9.2.2"), ("9.1.1", "9.1.2"), ("9.0.4", "9.1.0"),
            ("9.0.3", "9.0.4"), ("8.2.4", "8.2.5")], "selectors_js",
           note="8.2.5 fixes perf regression #286. 20 expressible pairs in "
                "total; the cap keeps the five most recent."),
    _known("css_select_known", "css-select", "css_select_", "JavaScript",
           ("5.1.0", "5.2.0"), [("5.1.0", "5.2.0")], "selectors_js",
           note="#1025 caches :has subtree results; 5.1.0 throws on "
                ":read-only/:read-write (dropped by the failure path)."),
    _known("sqlcst_known", "sql-parser-cst", "sqlcst_", "JavaScript",
           ("0.21.2", "0.22.0"), [("0.21.2", "0.22.0")], "sql_js",
           note="#52 backtracking fixes; PostgreSQL DML changes in the range "
                "are unreachable from a SELECT grammar.", shape=()),
    _known("orjson_known", "orjson", "orjson_", "Python",
           ("3.10.1", "3.10.2", "3.10.3", "3.10.4", "3.10.5", "3.10.6"),
           [("3.10.1", "3.10.2"), ("3.10.3", "3.10.4"), ("3.10.5", "3.10.6")],
           "json", expected={("3.10.3", "3.10.4"): "equivalent"},
           note="Changelog entries mapped to tag-range commits (strict "
                "linked-commit reading gives 0 pairs). 3.10.3->3.10.4 only "
                "removes null checks and is expected to show no effect."),
    _known("simplejson_known", "simplejson", "simplejson_", "Python",
           ("3.20.2", "4.0.0"), [("3.20.2", "4.0.0")], "json",
           note="4.0.0 is a large release; a difference cannot be credited "
                "to the key-interning commit alone."),
    _known("pyjsonpath_known", "python-jsonpath", "pyjsonpath_", "Python",
           ("1.3.2", "2.0.0"), [("1.3.2", "2.0.0")], "jsonpath_py",
           note="2.0.0 is a rewrite; the regex-cache commit is not the only "
                "change."),
    _known("jpython_known", "jsonpath-python", "jpython_", "Python",
           ("1.1.0", "1.1.1", "1.1.2", "1.1.3"),
           [("1.1.0", "1.1.1"), ("1.1.1", "1.1.2"), ("1.1.2", "1.1.3")],
           "jsonpath_py",
           note="1.1.2 stops building a debug string per match."),
]

# ------------------------------------------------------------ tailored
# RQ1, tailored setting: the same mined pairs as the blind
# known-pair subjects, on grammars shaped from each commit's diff the way a
# developer investigating it would write them. Every tailored grammar is a
# sub-language of the frozen spec grammar (except one declared widening back
# toward the specification: CSS escapes for nwsapi), its rationale is recorded
# in the .fan header, and the loop then runs exactly as in the blind setting.
# Not blind by construction; reported side by side with the blind verdicts.
def _tailored(name, base, systems=None, pairs=None, expected_metrics=None,
              note=""):
    b = next(x for x in SUBJECTS if x["name"] == base)
    d = dict(b)
    d.update(name=name, rqs=("RQ1-tailored",), blind=False,
             tailored_from=base,
             note="Tailored (RQ1). " + note)
    if systems is not None:
        d["systems"] = tuple(systems)
    if pairs is not None:
        d["pairs"] = tuple(pairs)
        d["pair_expected"] = {pp: "b_faster" for pp in pairs}
    if expected_metrics is not None:
        d["expected_metrics"] = tuple(expected_metrics)
    return d


for _t in [
    _tailored("jpython_tailored", "jpython_known",
              note="wide objects walked by wildcard/descendant queries"),
    _tailored("pyjsonpath_tailored", "pyjsonpath_known",
              note="match()/search() filters over many nodes; pair mis-specified, expected null"),
    _tailored("orjson_tailored", "orjson_known",
              note="key-dense objects with scalar values; Latin-1-range strings"),
    _tailored("simplejson_tailored", "simplejson_known",
              note="key-heavy objects; effect at most ~1.06x by hand"),
    _tailored("sqlformatter_tailored", "sql_formatter_latest",
              systems=("sql_formatter_15_8_2", "sql_formatter_15_9_0"),
              pairs=[("sql_formatter_15_8_2", "sql_formatter_15_9_0")],
              note="long select/IN lists and OR chains (PR #963)"),
    _tailored("domselector_tailored", "domselector_known",
              expected_metrics=("runtime_ns", "fresh_ns"),
              note="bare [name], attribute-led compounds, wide sibling lists; "
                   "fresh_ns (cold engine caches) added as a declared second metric"),
    _tailored("nwsapi_tailored", "nwsapi_known",
              note="CSS escapes re-admitted (declared widening toward the spec)"),
    _tailored("cssselect_tailored", "css_select_known",
              note=":has-heavy selectors over deep documents"),
]:
    SUBJECTS.append(_t)

CANDIDATES = []

import pathlib as _pathlib
_SUBJECT_ROOT = _pathlib.Path(__file__).resolve().parents[2] / "subjects"
SUBJECTS = [s for s in SUBJECTS
            if (_SUBJECT_ROOT / s.get("corpus_from", s["name"])).is_dir()]

BY_NAME = {s["name"]: s for s in SUBJECTS}
BY_NAME.update({c["name"]: c for c in CANDIDATES})


def subjects(category=None, rq=None, include_synthetic=False,
             include_cross_language=False):
    """The benchmark, filtered the way a given RQ's table wants it.

    `rq="RQ1"` gives the mined known pairs, `rq="RQ1-tailored"` their
    tailored counterparts, `rq="RQ2"` the latest release series and
    `rq="RQ3"` the competing implementations.
    """
    out = []
    for s in SUBJECTS:
        if category and s["category"] != category:
            continue
        if rq and rq not in (s.get("rqs") or ()):
            continue
        if s.get("synthetic") and not include_synthetic:
            continue
        if s.get("cross_language") and not include_cross_language:
            continue
        out.append(s)
    return out


def corpus_dir_for(subject, root):
    """Where this subject's corpus lives.

    Most subjects own their corpus. A pair drawn from an implementation set
    (selectors_js_pair) reads that set's corpus instead, because both releases
    are already measured there on the same inputs -- which is what makes the
    comparison paired and the pair free.
    """
    return root / subject.get("corpus_from", subject["name"])


def pairs_to_score(subject):
    """The (a, b) system pairs a scorer should look at for this subject.

    A `pair` subject has exactly one, ordered before-then-after, so "direction"
    means something. An implementation set has every unordered pair, ordered by
    the expected ranking where one is known so that a confirmed ordering reads
    as `a_faster` throughout.
    """
    syss = list(subject["systems"])
    if subject.get("pairs"):
        # Known-pair subjects carry many versions but score only the pairs
        # the funnel selected, which need not be adjacent.
        return [tuple(p) for p in subject["pairs"]]
    if subject["category"] == "pair":
        return [(syss[0], syss[1])]
    if subject["category"] == "series":
        return list(zip(syss, syss[1:]))
    order = list(subject.get("expected_order") or syss)
    rank = {n: i for i, n in enumerate(order)}
    out = []
    for i, a in enumerate(syss):
        for b in syss[i + 1:]:
            out.append((a, b) if rank.get(a, 99) <= rank.get(b, 99) else (b, a))
    return out


def expected_for(subject, a, b):
    """The expected verdict for one (a, b) pair: a per-pair override where the
    subject declares one (known-pair subjects), else the subject's own."""
    return (subject.get("pair_expected") or {}).get((a, b), subject.get("expected"))


def expected_winner(subject, a, b):
    """Which system the manifest expects to win, or None where it has no claim."""
    exp = expected_for(subject, a, b)
    if exp == "a_faster":
        return a
    if exp == "b_faster":
        return b
    if subject.get("expected_order"):
        order = subject["expected_order"]
        if a in order and b in order:
            return a if order.index(a) < order.index(b) else b
    return None
