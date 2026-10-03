"""Emit a targeted grammar: structural grammar + property fns + `where` clauses.

The constraint split in practice: each targeted request is a copy of the
structural `.fan` with the eval's property functions made available (so
`depth(<start>)` etc. resolve) and the targeting constraints appended as
SEPARATE `where` clauses. Fandango ANDs hard constraints internally, so N
clauses = their conjunction -- no monolithic OR-joined constraints() function.

A request can also be realised STRUCTURALLY, by rewriting the repetition that
governs the property instead of constraining the property. That is the better
realisation whenever it is available: the clause makes the search find what
the rewrite constructs. The clause is also the case that fails outright rather
than degrading: an unsatisfiable hard clause returns nothing and spends the
whole request budget doing it.

A rewritten band tends to return inputs at its lower bound: Fandango lands
there and stays. Spread has to come from issuing several narrow bands, the way
`fuzz_stratified` does, not from one wide one.
"""
import re
from pathlib import Path


_RULE = re.compile(r"^(<[A-Za-z_][\w]*>)\s*::=\s*(.*)$")
_NT = re.compile(r"<[A-Za-z_][\w]*>")


def _split_alternatives(rhs):
    """Split a rule's right-hand side at top-level `|`.

    Skips `|` inside quoted strings (with backslash escapes) and inside
    parenthesised groups, and stops at a `#` comment outside quotes.
    """
    alts, cur, depth, quote, i = [], [], 0, None, 0
    while i < len(rhs):
        c = rhs[i]
        if quote:
            cur.append(c)
            if c == "\\" and i + 1 < len(rhs):
                cur.append(rhs[i + 1]); i += 2; continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c; cur.append(c)
        elif c == "#":
            break
        elif c == "(":
            depth += 1; cur.append(c)
        elif c == ")":
            depth -= 1; cur.append(c)
        elif c == "|" and depth == 0:
            alts.append("".join(cur).strip()); cur = []
        else:
            cur.append(c)
        i += 1
    alts.append("".join(cur).strip())
    return [a for a in alts if a]


def _unquoted(alt):
    """The alternative with quoted strings blanked, so `<x>` inside a string
    literal is not mistaken for a reference."""
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', alt)


def _required_refs(alt):
    """Non-terminals an alternative MUST derive: optional repetitions (`*`,
    `{0,..}`) do not count."""
    s = _unquoted(alt)
    out = set()
    for m in _NT.finditer(s):
        tail = s[m.end():m.end() + 4]
        if tail.startswith("*") or re.match(r"\{\s*0\s*,", tail) or tail.startswith("{0}"):
            continue
        out.add(m.group(0))
    return out


def _productive(rules):
    """Non-terminals that can derive a finite string (the standard fixpoint)."""
    prod, changed = set(), True
    while changed:
        changed = False
        for lhs, alts in rules.items():
            if lhs in prod:
                continue
            if any(_required_refs(a) <= prod for a in alts):
                prod.add(lhs); changed = True
    return prod


def force_through(text, nt):
    """Prune the alternatives that let generation bypass the repetition site
    on `nt`.

    Banding `<more_member>*` to `{11,24}` constrains objects, but `<doc_root> ::=
    <nonempty_object> | <nonempty_array>` lets the generator avoid objects, and
    under a node budget it does: a JSONPath 11-24 member stratum can produce
    documents with zero keys, every one an array. This keeps,
    along the shortest path from `<start>` to a rule containing the site, only
    the alternatives that continue the path, so every input passes through the
    site at least once. A stratum is then a sub-language; the strata together
    still cover the language.

    A pruned rule changes every use of that rule, and pruning one that sits on a
    cycle could leave a grammar that never terminates. Any rule that would stop
    being productive keeps its original alternatives.
    """
    lines = text.split("\n")
    rules, where = {}, {}
    for i, line in enumerate(lines):
        m = _RULE.match(line)
        if m:
            rules[m.group(1)] = _split_alternatives(m.group(2))
            where[m.group(1)] = i
    if "<start>" not in rules:
        return text
    site_re = re.compile(re.escape(nt) + r"\s*(?:\{|\*|\+)")
    targets = {lhs for lhs, alts in rules.items()
               if any(site_re.search(_unquoted(a)) for a in alts)}
    if not targets or "<start>" in targets:
        return text
    # Shortest path <start> -> some target, over references.
    parent, frontier, found = {"<start>": None}, ["<start>"], None
    while frontier and found is None:
        nxt = []
        for a in frontier:
            for alt in rules.get(a, []):
                for ref in _NT.findall(_unquoted(alt)):
                    if ref in rules and ref not in parent:
                        parent[ref] = a
                        if ref in targets:
                            found = ref
                            break
                        nxt.append(ref)
                if found: break
            if found: break
        frontier = nxt
    if found is None:
        return text
    path, x = [], found
    while x is not None:
        path.append(x); x = parent[x]
    path.reverse()
    pruned = dict(rules)
    for a, b in zip(path, path[1:]):
        keep = [alt for alt in rules[a] if b in _NT.findall(_unquoted(alt))]
        if keep and len(keep) < len(rules[a]):
            pruned[a] = keep
    keep = [alt for alt in rules[found] if site_re.search(_unquoted(alt))]
    if keep and len(keep) < len(rules[found]):
        pruned[found] = keep
    prod = _productive(pruned)
    for lhs in list(pruned):
        if pruned[lhs] is not rules[lhs] and lhs not in prod:
            pruned[lhs] = rules[lhs]
    if not ("<start>" in _productive(pruned)):
        return text
    for lhs, alts in pruned.items():
        if alts is not rules[lhs]:
            lines[where[lhs]] = f"{lhs} ::= " + " | ".join(alts)
    return "\n".join(lines)


def rewrite_repetition(text, nt, lo, hi, force=True):
    """Set the repetition on `nt` to `{lo,hi}` wherever it appears.

    `<nt>{n,m}`, `<nt>*` and `<nt>+` are all rewritable, and one of the three
    must follow the non-terminal, so a bare `<nt>` (including a rule's own
    left-hand side) is never touched.

    An explicit bound also overrides Fandango's `max_repetition` setting, which
    otherwise caps `*` and `+` at 20 during generation regardless of the node
    budget. That is why this is the lever that works: raising max_nodes does
    not lengthen a free `*`, while an explicit bound does.
    """
    pattern = re.compile(rf"{re.escape(nt)}\s*(?:\{{[^}}]*\}}|\*|\+)")
    lo, hi = int(lo), int(hi)
    if hi <= 0:
        # The zero band. Fandango rejects `{0,0}` ("Maximum repetitions 0 must
        # be greater than 0"), which would fail every request aimed at zero
        # occurrences. Zero repetitions of anything is the empty string, so
        # say that instead.
        return pattern.sub('""', text)
    out = pattern.sub(f"{nt}{{{max(lo, 0)},{max(hi, lo)}}}", text)
    # A band that asks for at least one repetition must not be routable
    # around (see force_through).
    return force_through(out, nt) if (force and lo >= 1) else out


def build_targeted_grammar(structural_fan_path, udf_path, where_clause_bodies,
                           rewrites=None, soft_clauses=None, extra_source=None):
    """Return .fan text = udf (imports + property fns) + grammar + clauses.

    `extra_source` is Python prepended alongside the subject's own, and is how
    grammar-derived properties become usable in a clause: they are closures
    built by `core.grammar_props`, so without their definitions a
    `where count_<X>(<start>) ...` clause names something the grammar has never
    heard of.

    `rewrites` is a list of (non-terminal, lo, hi) applied to the grammar text.
    `soft_clauses` are `maximizing`/`minimizing` bodies; note the spelling,
    since Fandango's lexer accepts only the American form and `minimising`
    parses as ordinary Python, failing with an error about non-terminals that
    never mentions the keyword.
    """
    udf = Path(udf_path).read_text()
    if extra_source:
        udf = f"{extra_source}\n{udf}"
    grammar = Path(structural_fan_path).read_text()
    for nt, lo, hi in (rewrites or []):
        grammar = rewrite_repetition(grammar, nt, lo, hi)
    clauses = [f"where {body}" for body in where_clause_bodies]
    clauses += list(soft_clauses or [])
    return f"{udf}\n{grammar}\n" + "\n".join(clauses) + "\n"
