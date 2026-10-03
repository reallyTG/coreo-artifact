"""Input properties for the CSS selector subject.

Occurrence counts of grammar non-terminals (`count_compound`, `count_simple`,
`count_node`, ...) are derived from the grammar by `core/grammar_props.py`.
Declared here is only what no occurrence count measures: document nesting
depth, pseudo-class nesting depth in the selector, and the byte size of each
half.
"""

SEPARATOR = "\n@@@\n"

PROPERTIES = [
    "doc_depth",
    "doc_bytes",
    "selector_len",
    "selector_nesting",
]

# HTML void elements the grammar can emit: a start tag with no end tag.
# A plain string, not a one-element tuple: str.startswith accepts either, and
# the tuple literal ("input",) is rejected by Fandango's embedded-Python parser
# when this file is pasted into a targeted grammar, which fails every targeted
# request.
VOID = "input"


def _split(tree):
    selector, _, doc = str(tree).partition(SEPARATOR)
    return selector, doc


def doc_depth(tree):
    """Deepest element nesting, counted over the tag stream.

    Depth is what makes a descendant combinator expensive: matching `a b`
    walks ancestors, so the engines separate most where documents are deep.
    """
    doc = _split(tree)[1]
    depth = best = 0
    i = 0
    while i < len(doc):
        if doc[i] == "<":
            if doc[i + 1:i + 2] == "/":
                depth -= 1
            elif doc[i + 1:i + 2] == "!":
                pass                      # <!DOCTYPE html>
            elif doc.startswith(VOID, i + 1):
                best = max(best, depth + 1)
            else:
                depth += 1
                best = max(best, depth)
            close = doc.find(">", i)
            i = len(doc) if close < 0 else close + 1
        else:
            i += 1
    return best


def doc_bytes(tree):
    return len(_split(tree)[1])


def selector_len(tree):
    return len(_split(tree)[0])


def selector_nesting(tree):
    """Deepest nesting of functional pseudo-classes (:is, :where, :not, :has,
    :nth-*, :lang). The selector alphabet has no parentheses anywhere else, so
    bracket depth is exactly this."""
    sel = _split(tree)[0]
    depth = best = 0
    for ch in sel:
        if ch == "(":
            depth += 1
            best = max(best, depth)
        elif ch == ")":
            depth -= 1
    return best
