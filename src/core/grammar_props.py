"""Properties derived from the grammar, and the repetition that governs each.

Input properties have three sources: occurrence counts of every non-terminal,
occurrence counts of the repetition-shaped ones, and user-defined functions.
This module derives the first two, so a subject does not hand-write a
`_count_nonterminal` helper per property.

Deriving them buys more than the boilerplate. A property that is `count_<X>`
for a non-terminal in the grammar has a *statically known* governing
repetition: the repetition sites from whose body `<X>` is reachable. That is
what lets a request for "more `<X>` than we have seen" be realised
structurally, by rewriting `<more_member>*` to `<more_member>{1001,1200}`,
rather than as a `where count_more_member(<start>) >= 1002` clause that the
search has to find its own way to.

User-defined properties stay: ratios and `depth` are not occurrence counts of
anything, they have no governing repetition, and the levers that need one do
not apply to them. That split falls out of the derivation rather than having
to be declared.

Two bounds are tracked per repetition, and keeping them apart is the point:

* the LANGUAGE bound, written in the grammar (`<tchar>{1,12}`). `*` and `+` are
  unbounded here, whatever a search setting says.
* `max_repetition`, a Fandango grammar SETTING defaulting to 20, which bounds
  `*` and `+` during generation and is invisible in the .fan text.

A property stuck at 20 on a `*` axis is stuck against the setting; one stuck at
12 on `<tchar>{1,12}` is stuck against the language. The first is a budget to
raise, the second a claim about the subject, and the frontier report needs
both to tell them apart.
"""
import math
import re
from dataclasses import dataclass, field

from fandango.api import parse
from fandango.language.symbols import NonTerminal

INF = math.inf

# How large a count has to get before it is called unbounded. Recursion makes
# the fixpoint below grow geometrically, so anything genuinely unbounded passes
# this within a few rounds, and no real grammar means to bound a count above it.
SATURATE = 10 ** 6


@dataclass
class Site:
    """One repetition in the grammar: `<more_member>*`, `<tchar>{1,12}`."""
    nt: str                 # non-terminal directly under the repetition, "<x>"
    kind: str               # "star" | "plus" | "repetition" | "option"
    lang_min: float         # bound written in the grammar
    lang_max: float         # INF for * and +, whatever max_repetition says
    rule: str               # the rule it appears in, for reporting
    governs: set = field(default_factory=set)   # non-terminals reachable from it
    # Upper bound on derivation-tree nodes for ONE repetition of this site, or
    # None when recursion makes it unbounded. A structural request asking for N
    # repetitions needs a node budget of about N times this, and gets degenerate
    # inputs without it: at Fandango's default 200 nodes a 200-repetition band
    # has no nodes left for the elements, so each takes its cheapest derivation
    # and the elements come out near-identical.
    nodes_per_item: "int | None" = None

    @property
    def bounded_in_language(self):
        return self.lang_max < INF

    def describe(self, max_repetition=None):
        if self.bounded_in_language:
            return f"{self.nt}{{{self.lang_min:g},{self.lang_max:g}}} in {self.rule}"
        op = {"star": "*", "plus": "+"}.get(self.kind, "*")
        cap = f", capped at {max_repetition} by max_repetition" if max_repetition else ""
        return f"{self.nt}{op} in {self.rule}{cap}"


@dataclass
class ListRecursion:
    """A rule that spells a list as recursion instead of a repetition.

    `<texts> ::= <text> <texts> | <text>` and `<text>+` are the same language,
    and both shapes count as "recursive". Only the second carries a
    repetition node, so only the second can be banded by `fuzz_stratified` or
    rewritten by a structural request -- the first silently has no governing
    site and every property under it is unreachable.

    Detected, not repaired. The replacement depends on whether the list has a
    separator, and a rule is a claim about the subject's language: the author
    should make it, with the exact edit named for them.
    """
    rule: str               # the recursive non-terminal, "<texts>"
    element: str            # what repeats, "<text>"
    separator: bool         # whether symbols sit between the element and the tail

    def advice(self):
        if self.separator:
            helper = f"<more_{self.element.strip('<>')}>"
            return (f"{self.rule} is a separated list written as recursion; "
                    f"write it as `{self.rule} ::= {self.element} {helper}*` "
                    f"with `{helper} ::= <separator> {self.element}` so the "
                    f"length can be banded")
        return (f"{self.rule} is a list written as recursion; write it as "
                f"`{self.rule} ::= {self.element}+` so the length can be banded")


@dataclass
class GrammarInfo:
    counts: dict            # "<x>" -> (min, max) occurrences in a derivation
    sites: list             # every Site
    governors: dict         # "<x>" -> [Site], outermost first
    max_repetition: int     # the grammar's setting
    start: str
    local: dict = field(default_factory=dict)   # rule -> per-expansion counts
    aliases: dict = field(default_factory=dict)  # representative -> [same count]
    list_recursions: list = field(default_factory=list)   # [ListRecursion]

    @property
    def varying(self):
        """Non-terminals whose occurrence count can move.

        A count that is the same in every derivation is not a property: it
        cannot correlate with anything, and asking for more of it is a request
        the grammar can never satisfy.
        """
        return [nt for nt, (lo, hi) in self.counts.items() if hi > lo]

    def governing_site(self, nt):
        """The site to widen for `nt`, or None if nothing governs it.

        None means the count varies by recursion or by an alternative rather
        than by a repetition, so there is no bound to rewrite and the request
        has to go through `max_repetition` / `max_nodes` instead.
        """
        sites = self.governors.get(nt) or []
        return sites[0] if sites else None


def _add(a, b):
    return (a[0] + b[0], min(a[1] + b[1], INF))


def _mul(a, b):
    lo = a[0] * b[0]
    hi = INF if (a[1] == INF or b[1] == INF) else a[1] * b[1]
    return (lo, INF if hi > SATURATE else hi)


def _merge(acc, nt, interval):
    acc[nt] = _add(acc.get(nt, (0, 0)), interval)


def _rep_bounds(node):
    """(language min, language max) for a repetition node.

    `Star.max` and `Plus.max` report `max_repetition` (20 by default), which is
    a search setting and not part of the language. They are INF here; the
    setting is carried separately on GrammarInfo.
    """
    kind = type(node).__name__.lower()
    if kind == "star":
        return 0, INF, "star"
    if kind == "plus":
        return 1, INF, "plus"
    if kind == "option":
        return 0, 1, "option"
    return float(node.min), float(node.max), "repetition"


def _walk(node, rule, sites):
    """Occurrence counts of each non-terminal in one expansion of `node`."""
    cls = type(node).__name__
    if cls == "NonTerminalNode":
        return {str(node.symbol): (1, 1)}
    if cls == "TerminalNode":
        return {}
    if cls == "Alternative":
        branches = [_walk(c, rule, sites) for c in node.children()]
        keys = set().union(*branches) if branches else set()
        out = {}
        for k in keys:
            los = [b.get(k, (0, 0))[0] for b in branches]
            his = [b.get(k, (0, 0))[1] for b in branches]
            out[k] = (min(los), max(his))
        return out
    if cls in ("Star", "Plus", "Option", "Repetition"):
        lo, hi, kind = _rep_bounds(node)
        body = {}
        for c in node.children():
            for k, v in _walk(c, rule, sites).items():
                _merge(body, k, v)
        # The site is named by the non-terminal directly under it, because that
        # is what the textual rewrite keys on (`<more_member>*` -> `{lo,hi}`).
        direct = [str(c.symbol) for c in node.children()
                  if type(c).__name__ == "NonTerminalNode"]
        if direct:
            sites.append(Site(nt=direct[0], kind=kind, lang_min=lo,
                              lang_max=hi, rule=rule))
        return {k: _mul((lo, hi), v) for k, v in body.items()}
    # Concatenation and anything else with children: sum them.
    out = {}
    for c in node.children():
        for k, v in _walk(c, rule, sites).items():
            _merge(out, k, v)
    return out


def _alternatives(node):
    """The top-level alternatives of a rule body."""
    if type(node).__name__ == "Alternative":
        return list(node.children())
    return [node]


def _find_list_recursions(rules):
    """Rules whose body is a list spelled as direct tail (or head) recursion.

    The test is a DIRECT self-reference in tail or head position, alongside at
    least one other symbol. That is what separates a list from genuine nesting:
    `<tree> ::= <open><inner><close>` recurses through `<inner>` but its tail
    is `<close>`, so it is a tree and is left alone -- which is right, because
    nesting depth is not a length to band.
    """
    out = []
    for symbol, body in rules.items():
        name = str(symbol)
        for alt in _alternatives(body):
            kids = (list(alt.children())
                    if type(alt).__name__ == "Concatenation" else [alt])
            if len(kids) < 2:
                continue
            def is_self(n):
                return (type(n).__name__ == "NonTerminalNode"
                        and str(n.symbol) == name)
            if is_self(kids[-1]):
                rest = kids[:-1]
            elif is_self(kids[0]):
                rest = kids[1:]
            else:
                continue
            nts = [str(k.symbol) for k in rest
                   if type(k).__name__ == "NonTerminalNode"]
            if not nts:
                continue
            out.append(ListRecursion(rule=name, element=nts[0],
                                     separator=len(rest) > 1))
            break
    return out


def _reachable(local):
    """nt -> every non-terminal reachable from it (transitively)."""
    reach = {a: set(local.get(a, {})) for a in local}
    changed = True
    while changed:
        changed = False
        for a in reach:
            grown = set(reach[a])
            for b in list(reach[a]):
                grown |= reach.get(b, set())
            if grown != reach[a]:
                reach[a] = grown
                changed = True
    return reach


def _unbounded(local, reach, start):
    """Non-terminals whose count has no upper bound, because of recursion.

    The fixpoint below cannot decide this on its own. Recursion through a
    single occurrence (`<text> ::= <text_char> <text> | <text_char>`) grows the
    upper bound by one per round rather than geometrically, so it never reaches
    SATURATE and the round limit truncates it instead. The truncated bound
    reads as a grammar that caps nesting and is simply the round count.

    Decided structurally instead. A non-terminal on a cycle can be unrolled
    without limit, so it and everything reachable from it are unbounded --
    provided the cycle is reachable from the start symbol, since a rule nothing
    derives bounds nothing.
    """
    recursive = {a for a in local if a in reach.get(a, set())}
    live = {start} | reach.get(start, set())
    out = set()
    for r in recursive & live:
        out |= {r} | reach.get(r, set())
    return out


def _totals(local, start):
    """Occurrences of each non-terminal in a full derivation of `start`.

    A fixpoint rather than an SCC decomposition. It is exact for a grammar
    without recursion; `_unbounded` handles the rest, and the lower bounds it
    produces stay correct either way, so a recursive rule with an empty
    alternative still reports a minimum of 0 rather than being called unbounded
    in both directions.
    """
    total = {a: {} for a in local}
    for _ in range(2 * len(local) + 8):
        changed = False
        for a in local:
            acc = {}
            for x, mult in local[a].items():
                _merge(acc, x, mult)
                for y, inner in total.get(x, {}).items():
                    _merge(acc, y, _mul(mult, inner))
            if acc != total[a]:
                total[a] = acc
                changed = True
        if not changed:
            break
    return total.get(start, {})


def expansion_nodes(local, nt):
    """Upper bound on tree nodes in one full expansion of `nt`, or None.

    Counts every non-terminal occurrence reachable from `nt`, plus one for
    `nt` itself, and adds a terminal allowance. None when any count is
    unbounded, since a recursive body has no finite worst case and the caller
    has to fall back to a constant.
    """
    totals = _totals(local, nt)
    n = 1
    for _, (_, hi) in totals.items():
        if hi >= INF:
            return None
        n += hi
    return int(n * 2)          # allowance for terminal nodes under each


def _identical_counts(local):
    """Group non-terminals whose counts are equal in EVERY derivation.

    Derived properties are redundant by construction: one repetition often
    governs many counts that all rise with it. Most of that has to be measured
    away by the correlation pass, but part of it is provable from the grammar
    and costs nothing to find: if `<B>` occurs exactly once in every expansion
    of `<A>` and `<A>` is its only parent, then count_B == count_A in every
    input, not merely correlated with it. `<number> ::= <sign> <magnitude>`
    gives two of those.

    Only exact identity is claimed. Counts that differ by a constant (a list's
    elements and its separators) are left to the empirical pass, which is where
    a judgement about "close enough" belongs -- it depends on the corpus, and
    it should be visible as a correlation rather than hidden in a static rule.
    """
    parents = {}
    for a, counts in local.items():
        for b, (_, hi) in counts.items():
            if hi > 0:
                parents.setdefault(b, set()).add(a)

    parent_of = {}
    for b, ps in parents.items():
        if len(ps) != 1:
            continue
        a = next(iter(ps))
        if local[a].get(b) == (1, 1):
            parent_of[b] = a

    def root(x, seen=None):
        seen = seen or set()
        while x in parent_of and x not in seen:
            seen.add(x)
            x = parent_of[x]
        return x

    groups = {}
    for nt in local:
        groups.setdefault(root(nt), []).append(nt)
    return {r: sorted(v) for r, v in groups.items() if len(v) > 1}


def analyze(fan_path):
    """Parse a .fan and derive its counts, repetition sites and governors."""
    with open(fan_path) as fh:
        grammar, _ = parse(fh, use_stdlib=False)

    local, sites = {}, []
    for symbol, rule in grammar.rules.items():
        name = str(symbol)
        local[name] = _walk(rule, name, sites)

    start = "<start>" if "<start>" in local else next(iter(local))
    reach = _reachable(local)
    counts = _totals(local, start)
    counts.setdefault(start, (1, 1))
    for nt in _unbounded(local, reach, start):
        if nt in counts:
            counts[nt] = (counts[nt][0], INF)

    for site in sites:
        site.governs = {site.nt} | reach.get(site.nt, set())
        site.nodes_per_item = expansion_nodes(local, site.nt)

    governors = {}
    for nt in counts:
        owning = [s for s in sites if nt in s.governs]
        # Outermost first: the site that governs the most non-terminals is the
        # one furthest up the derivation, and widening it moves the most.
        # When `count_digit` is governed by both `<digit>{0,3}` and an outer
        # `*` list, the latter is the cheap axis and comes first.
        owning.sort(key=lambda s: (len(s.governs), s.lang_max == INF), reverse=True)
        if owning:
            governors[nt] = owning

    return GrammarInfo(counts=counts, sites=sites, governors=governors,
                       max_repetition=grammar.get_max_repetition(), start=start,
                       local=local, aliases=_identical_counts(local),
                       list_recursions=_find_list_recursions(grammar.rules))


# --- properties ---------------------------------------------------------

def _count_nonterminal(tree, target):
    count = 1 if tree.symbol == target else 0
    for child in tree.children:
        count += _count_nonterminal(child, target)
    return count


def _counter(nt):
    target = NonTerminal(nt)

    def count(tree):
        return _count_nonterminal(tree, target)
    return count


def property_name(nt):
    """`<more_member>` -> `count_more_member`."""
    return "count_" + re.sub(r"\W", "_", nt.strip("<>"))


def duplicates(info):
    """Non-terminals dropped for having a count identical to another's."""
    return {nt for rep, members in info.aliases.items()
            for nt in members if nt != rep}


def derived_properties(info):
    """{property name -> callable(tree)} for every non-terminal that can vary.

    Excluded: the start symbol, any count the grammar fixes (`varying`), and
    every member of an identical-count group but its representative. What
    survives still needs the empirical correlation pass -- this only removes
    what can be ruled out without data.
    """
    drop = duplicates(info)
    out = {}
    for nt in info.varying:
        if nt == info.start or nt in drop:
            continue
        out[property_name(nt)] = _counter(nt)
    return out


def _log_bands(lo, hi, n):
    """Equal-ratio bands over [lo, hi], with an explicit zero band when lo is 0.

    Log-spaced because a repetition count's effect on cost is a power law: equal
    WIDTH bands over 0..200 put four fifths of the strata above 40 and none
    between 1 and 10, where most of the interesting behaviour is.

    The zero band is called out separately because zero is a shape, not a size.
    jsonpath_js generated `{}` for 57% of its documents purely because the
    generator chose evenly between alternatives; a stratum that owns the empty
    case gives it one share of the budget instead of whatever the generator
    happens to produce.
    """
    import math

    lo, hi = int(lo), int(hi)
    bands = []
    if lo <= 0:
        bands.append((0, 0))
        lo = 1
        n -= 1
    if hi <= lo or n <= 0:
        if hi >= lo:
            bands.append((lo, hi))
        return bands
    edges = [lo * (hi / lo) ** (i / n) for i in range(n + 1)]
    # `prev` rather than bands[-1]: a band can collapse to nothing when the
    # range is short relative to the band count, and then there is no previous
    # entry to read.
    prev = lo - 1
    for i in range(n):
        a = max(int(round(edges[i])), prev + 1)
        b = hi if i == n - 1 else int(round(edges[i + 1])) - 1
        if b >= a:
            bands.append((a, b))
            prev = b
    return bands


# Ceiling for a site whose body can recurse. Breadth and depth MULTIPLY there,
# so a band asking for 53-200 children applies at every level, and the request
# does not finish in a usable time. A site with no finite `nodes_per_item` is
# exactly the recursive case -- `expansion_nodes` returns None when some count
# under it is unbounded.
RECURSIVE_CEILING = 24


def stratify_axes(info, n_bands=5, max_repetition=200, max_axes=None):
    """Exploration strata derived from the grammar: one axis per repetition site.

    One AXIS PER SITE, not per property. A site typically governs several
    derived counts and banding it once bands all of them, so the stratum count
    follows the grammar's shape rather than its property count.

    The ceiling is the language bound where the grammar states one and
    `max_repetition` where it does not, which keeps a stratum from asking for
    inputs the specification forbids.

    Ordered by how much each site governs, so a budget that cannot afford every
    axis keeps the ones that move the most.
    """
    seen, axes = set(), []
    for site in sorted(info.sites, key=lambda s: -len(s.governs)):
        if site.nt in seen:
            continue
        seen.add(site.nt)
        hi = (site.lang_max if site.lang_max < INF else max_repetition)
        ceiling = (RECURSIVE_CEILING if site.nodes_per_item is None
                   else max_repetition)
        bands = _log_bands(site.lang_min, min(hi, ceiling), n_bands)
        if len(bands) >= 2:
            axes.append({"nt": site.nt, "bands": bands})
    return axes[:max_axes] if max_axes else axes


def derived_source(info, names=None):
    """Python defining the derived properties, for embedding in a .fan.

    A derived property is a closure built here, so it exists in the framework
    and nowhere else. `build_targeted_grammar` prepends the subject's
    `user_def_functions.py`, which defines only the declared properties, so a
    clause like `where count_more_member(<start>) >= 189` would reference a
    name the grammar has never heard of. Fandango reports that per evaluation
    rather than raising, so it does not stop a run: the run prints
    `name 'count_more_member' is not defined` messages while appearing to
    work, with every affected region quietly constraining nothing.

    Emitting the definitions alongside the clauses is what makes a derived
    property usable as a constraint rather than only as a column.
    """
    wanted = set(names) if names is not None else set(derived_properties(info))
    lines = [
        "from fandango.language.symbols import NonTerminal as _CoreoNT",
        "",
        "def _coreografa_count(tree, target):",
        "    n = 1 if tree.symbol == target else 0",
        "    for _c in tree.children:",
        "        n += _coreografa_count(_c, target)",
        "    return n",
        "",
    ]
    emitted = 0
    for nt in info.varying:
        name = property_name(nt)
        if name not in wanted:
            continue
        lines += [f"def {name}(tree):",
                  f"    return _coreografa_count(tree, _CoreoNT({nt!r}))",
                  ""]
        emitted += 1
    return "\n".join(lines) if emitted else ""


def describe(info):
    """Report lines: what was derived, what governs it, what bounds it."""
    drop = duplicates(info)
    lines = [f"[props] max_repetition={info.max_repetition} "
             f"(bounds * and + during generation)"]
    for nt in sorted(info.varying):
        if nt == info.start or nt in drop:
            continue
        lo, hi = info.counts[nt]
        site = info.governing_site(nt)
        where = (f"governed by {site.describe(info.max_repetition)}"
                 if site else "no governing repetition (recursion or alternative)")
        span = f"{lo:g}..{'inf' if hi == INF else f'{hi:g}'}"
        lines.append(f"[props]   {property_name(nt):28s} {span:>12s}  {where}")
    for rep, members in sorted(info.aliases.items()):
        others = [m for m in members if m != rep]
        if others and rep in info.varying:
            lines.append(f"[props] identical to {property_name(rep)}, "
                         f"not derived: {', '.join(property_name(m) for m in others)}")
    for lr in info.list_recursions:
        lines.append(f"[props] WARNING {lr.advice()}")
    fixed = [nt for nt, (lo, hi) in info.counts.items()
             if hi == lo and nt != info.start]
    if fixed:
        lines.append(f"[props] fixed count, not derived: "
                     f"{', '.join(sorted(fixed))}")
    return lines
