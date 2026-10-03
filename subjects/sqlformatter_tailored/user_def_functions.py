"""Input properties for the tailored sql-formatter subject.

`sql_bytes` is the spec subject's size property, kept unchanged. `list_items`
is the axis the tailored grammar is built around: the number of operands in
the statement's one long flat list (the select list in kind 1, the IN list in
kind 2), which is what PR #963's quadratic cost grows with. Occurrence counts
of non-terminals (`count_more_el`, ...) come from core/grammar_props.py.
"""
import re

PROPERTIES = [
    "sql_bytes",
    "list_items",
]

_SEP = re.compile(r"\s*,\s*|\s+(?:OR|AND)\s+")


def sql_bytes(tree):
    return len(str(tree))


def list_items(tree):
    """Operands in the long flat list: the IN list if there is one, else the select list."""
    s = str(tree)
    if "(" in s:
        body = s[s.index("(") + 1:s.rindex(")")]
    else:
        body = s[len("SELECT "):s.index(" FROM ")]
    return len(_SEP.split(body.strip()))
