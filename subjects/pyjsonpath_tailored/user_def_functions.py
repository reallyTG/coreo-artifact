"""Input properties for the pyjsonpath_tailored subject (RQ1 tailored setting).

The properties of subjects/jsonpath_py/user_def_functions.py plus
`n_doc_nodes` and `n_function_calls`, for the axis the tailored grammar varies
(pyjsonpath_tailored.fan header). Both are structural counts; none runs an
SUT.

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
    "n_doc_nodes",
    "n_function_calls",
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


def n_doc_nodes(tree):
    """Values in the document (containers and scalars): the nodes a
    descendant filter `..[?...]` is applied to."""
    import json
    try:
        stack, n = [json.loads(_split(tree)[1])], 0
    except ValueError:
        return 0
    while stack:
        v = stack.pop()
        n += 1
        if isinstance(v, dict):
            stack.extend(v.values())
        elif isinstance(v, list):
            stack.extend(v)
    return n


def n_function_calls(tree):
    """match()/search() calls written in the query; each runs once per node
    the filter visits (the per-call cost commit 7ed181a caches)."""
    q = _split(tree)[0]
    return q.count("match(") + q.count("search(")
