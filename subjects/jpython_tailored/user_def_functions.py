"""Input properties for the jpython_tailored subject (RQ1 tailored setting).

The properties of subjects/jsonpath_py/user_def_functions.py plus
`n_object_keys` and `max_value_bytes`, the two axes the tailored grammar varies
(jpython_tailored.fan header). Both are structural counts on the document;
none runs an SUT.

Occurrence counts of the grammar's non-terminals (`count_descendant`,
`count_filter`, `count_test`, `count_object`, ...) are derived from the grammar
by `core/grammar_props.py` and need no function here. What is declared here is
what no occurrence count measures: how deep the document nests, and the byte
size of each half.

`PROPERTIES` declares which functions are features; the rest are helpers.
"""

SEPARATOR = "\n@@@\n"

PROPERTIES = [
    "doc_depth",
    "doc_bytes",
    "query_len",
    "n_object_keys",
    "max_value_bytes",
]


def _split(tree):
    """Return (query, document) for a generated input."""
    query, _, doc = str(tree).partition(SEPARATOR)
    return query, doc


def doc_depth(tree):
    """Deepest container nesting in the document.

    A descendant segment walks the whole subtree under each node it starts
    from, so depth multiplies with the number of `..` segments in the query.
    Counted on the text: unescaped string characters come from small letter
    alphabets and escapes never produce a literal bracket, so no bracket
    appears inside a string.
    """
    depth = best = 0
    for ch in _split(tree)[1]:
        if ch in "{[":
            depth += 1
            best = max(best, depth)
        elif ch in "}]":
            depth -= 1
    return best


def doc_bytes(tree):
    """Size of the document in compact form, in UTF-8 bytes.

    The grammar emits RFC 8259 blank space between tokens, which JSON.parse /
    json.loads strips before any engine sees the value, so the raw text length
    would mostly measure blanks. Member names are unique (I-JSON, enforced in
    the grammar), so parsing loses nothing and the compact size is the size of
    the value the engines walk.
    """
    import json
    raw = _split(tree)[1]
    try:
        value = json.loads(raw)
    except ValueError:
        return len(raw)
    return len(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def query_len(tree):
    return len(_split(tree)[0])


def _doc_value(tree):
    import json
    try:
        return json.loads(_split(tree)[1])
    except ValueError:
        return None


def n_object_keys(tree):
    """Total object keys in the document: a proxy for the keys a `..*` walk
    visits (per-key regex work, commits 61152d7 and 3054ca4)."""
    stack, n = [_doc_value(tree)], 0
    while stack:
        v = stack.pop()
        if isinstance(v, dict):
            n += len(v)
            stack.extend(v.values())
        elif isinstance(v, list):
            stack.extend(v)
    return n


def max_value_bytes(tree):
    """Compact size of the largest value directly under the root: what one
    match stringifies in 1.1.1's unguarded debug f-string (commit 70b0103)."""
    import json
    v = _doc_value(tree)
    vals = v.values() if isinstance(v, dict) else (v if isinstance(v, list) else [])
    return max((len(json.dumps(x, separators=(",", ":"))) for x in vals), default=0)
