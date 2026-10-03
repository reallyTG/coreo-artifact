from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_trav_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<trav_segment>'))

def count_wildcard_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<wildcard_selector>'))

def count_member_name_shorthand(tree):
    return _coreografa_count(tree, _CoreoNT('<member_name_shorthand>'))

def count_name_char(tree):
    return _coreografa_count(tree, _CoreoNT('<name_char>'))

def count_s_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<s_segment>'))

def count_wide_member(tree):
    return _coreografa_count(tree, _CoreoNT('<wide_member>'))

def count_leaf(tree):
    return _coreografa_count(tree, _CoreoNT('<leaf>'))

def count_doc_string(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_string>'))

def count_letter(tree):
    return _coreografa_count(tree, _CoreoNT('<letter>'))

def count_doc_int(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_int>'))

def count_pos_int(tree):
    return _coreografa_count(tree, _CoreoNT('<pos_int>'))

def count_DIGIT1(tree):
    return _coreografa_count(tree, _CoreoNT('<DIGIT1>'))

def count_DIGIT(tree):
    return _coreografa_count(tree, _CoreoNT('<DIGIT>'))

def count_inner_array(tree):
    return _coreografa_count(tree, _CoreoNT('<inner_array>'))

def count_more_leaf(tree):
    return _coreografa_count(tree, _CoreoNT('<more_leaf>'))

def count_inner_object(tree):
    return _coreografa_count(tree, _CoreoNT('<inner_object>'))

def count_wide_more_member(tree):
    return _coreografa_count(tree, _CoreoNT('<wide_more_member>'))

"""Input properties for the jpython_tailored subject (RQ1 tailored setting).

Copied from subjects/jsonpath_py/user_def_functions.py; `n_object_keys` and
`max_value_bytes` are added for the two axes the tailored grammar varies
(jpython_tailored.fan header). Both are structural counts on the document;
none runs an SUT.

Original docstring follows.


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

# TAILORED grammar for jsonpath-python 1.1.0 -> 1.1.1 -> 1.1.2 -> 1.1.3 (RQ1,
# tailored setting). A sub-language of the frozen spec grammar
# subjects/jsonpath_py/jsonpath_py.fan: every string this grammar generates is
# generated by that grammar (checked by parsing a sample with it, see
# subjects/jpython_tailored/check_sublanguage.py). Written 2026-10-02 from the
# three commits' diffs, the way a developer investigating those changes would
# shape inputs.
#
# What the commits change (jsonpath/jsonpath.py):
#
#   61152d7 (1.1.0 -> 1.1.1)  JSONPath._traverse, the loop under every wildcard
#     and descendant step, ran `re.match(r"^\w+$", k)` once per object KEY
#     VISITED; it now calls a precompiled REP_WORD_KEY.match. The saving is per
#     key the traversal walks, whether or not the key ends up matched.
#   70b0103 (1.1.1 -> 1.1.2)  `logger.debug(f"... {path} ... {obj}")` calls in
#     the trace were guarded with logger.isEnabledFor. Unguarded, the f-string
#     is built on every MATCH even with debug off, which stringifies the
#     matched value, so the cost grows with the size of each matched value.
#   3054ca4 (1.1.2 -> 1.1.3)  _build_path's REP_WORD_KEY.match(key) became
#     key.isidentifier(); again per key visited while building child paths.
#
# Input shape that exercises them: a WIDE object (many keys, so per-key work
# dominates) walked by a traversing query (`.*`, `[*]`, `..*`, `..name`), with
# member values that are themselves sizeable subtrees (arrays, small objects),
# so each match carries a large value for 1.1.2's f-string.
#
# Restrictions relative to jsonpath_py.fan (all remove alternatives, fix a
# vocabulary choice, or bound a repetition; no construct is added):
#
# | spec rule                     | here                                                   |
# |-------------------------------|--------------------------------------------------------|
# | jsonpath_query: "$" s_segment*| "$" trav_segment s_segment{0,2}: first step traverses  |
# | s_segment: optional blanks    | no blanks                                              |
# | child_segment                 | ".*", "[*]" (bracketed_selection of one wildcard), or  |
# |                               | "." member_name_shorthand (1-2 chars)                  |
# | descendant_segment            | "..*" or ".." member_name_shorthand (1-2 chars)        |
# | selectors: name/index/slice/  | dropped (only wildcard and shorthand names remain)     |
# |   filter                      |                                                        |
# | doc ws                        | "" everywhere                                          |
# | doc_root                      | nonempty_object only (the wide object)                 |
# | root members: more_member*    | wide_more_member* (renamed so `stratify` can band the  |
# |                               | width; Fandango only lands on band lower bounds, hence |
# |                               | several bands, set in example.py)                      |
# | root member_name              | the `<name_char>{3} <name_char>+` alternative with the |
# |                               | `+` bounded to {5,9}: 8-12 letters over {a,b,c,d}, so  |
# |                               | 300 keys rarely collide under unique_member_names      |
# | value under a root key        | leaf, inner array, or inner object                     |
# | inner object                  | fixed member names "a", "b", "c" in that order (each a |
# |                               | one-<name_char> member_name), so names never collide   |
# |                               | and `..a`/`..b`/`..c` queries hit                      |
# | inner array: more_value*      | more_leaf* (renamed, bandable as the value-size axis)  |
# | leaf                          | doc_int (pos_int 1-2 digits or "0") or doc_string of   |
# |                               | 1-3 letters                                            |
#
# Not used: escapes, numbers with fraction/exponent, true/false/null, nested
# containers below depth 3. The `where unique_member_names` clause of the spec
# grammar is kept.
import json as _json

def unique_member_names(tree):
    # I-JSON §2.3, copied from jsonpath_py.fan.
    text = str(tree).partition("\n@@@\n")[2]
    ok = [True]
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(set(keys)) != len(keys):
            ok[0] = False
        return dict(pairs)
    try:
        _json.loads(text, object_pairs_hook=hook)
    except Exception:
        return True
    return ok[0]

<start> ::= <jsonpath_query> "\n@@@\n" <doc>

# ---- query: traversing steps only -----------------------------------------
<jsonpath_query> ::= "$" <trav_segment> <s_segment>{0,2}
<trav_segment> ::= "." <wildcard_selector> | "[" <wildcard_selector> "]" | ".." <wildcard_selector> | ".." <member_name_shorthand>
<s_segment> ::= <trav_segment> | "." <member_name_shorthand>
<wildcard_selector> ::= "*"
<member_name_shorthand> ::= <name_first> | <name_first> <name_char>
<name_first> ::= "a" | "b" | "c"
<name_char> ::= "a" | "b" | "c" | "d"

# ---- document: one wide object --------------------------------------------
<doc> ::= <wide_object>
<wide_object> ::= "{" <wide_member> <wide_more_member>{24,28} "}"
<wide_more_member> ::= "," <wide_member>
<wide_member> ::= <wide_member_name> ":" <member_value>
<wide_member_name> ::= "\"" <name_char> <name_char> <name_char> <name_char>{5,9} "\""
<member_value> ::= <leaf> | <inner_array> | <inner_object>
<inner_object> ::= "{\"a\":" <leaf> "}" | "{\"a\":" <leaf> ",\"b\":" <inner_array> "}" | "{\"a\":" <leaf> ",\"b\":" <inner_array> ",\"c\":" <leaf> "}"
<inner_array> ::= "[" <leaf> <more_leaf>* "]"
<more_leaf> ::= "," <leaf>
<leaf> ::= <doc_int> | <doc_string>
<doc_int> ::= "0" | <pos_int>
<pos_int> ::= <DIGIT1> | <DIGIT1> <DIGIT>
<DIGIT1> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<DIGIT> ::= "0" | <DIGIT1>
<doc_string> ::= "\"" <doc_chars> "\""
<doc_chars> ::= <letter> | <letter> <letter> | <letter> <letter> <letter>
<letter> ::= "x" | "y" | "z"

where unique_member_names(<start>)


