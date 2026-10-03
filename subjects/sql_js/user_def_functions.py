"""Input properties for the SQL parser subject.

Occurrence counts of grammar non-terminals (`count_select`, `count_join`,
`count_predicate`, ...) come from `core/grammar_props.py`. Declared here is
what no occurrence count measures: how deeply the statement nests, and its
size.
"""

PROPERTIES = [
    "sql_bytes",
    "paren_depth",
]


def sql_bytes(tree):
    return len(str(tree))


def paren_depth(tree):
    """Deepest parenthesis nesting.

    Subqueries and parenthesised expressions both nest here, and a recursive
    descent parser's cost follows this rather than length.
    """
    depth = best = 0
    for ch in str(tree):
        if ch == "(":
            depth += 1
            best = max(best, depth)
        elif ch == ")":
            depth -= 1
    return best
