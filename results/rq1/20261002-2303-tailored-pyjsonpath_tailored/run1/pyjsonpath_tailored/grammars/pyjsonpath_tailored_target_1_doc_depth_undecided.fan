from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_pre_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<pre_segment>'))

def count_basic_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<basic_expr>'))

def count_match_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<match_expr>'))

def count_value_argument(tree):
    return _coreografa_count(tree, _CoreoNT('<value_argument>'))

def count_iregexp_literal(tree):
    return _coreografa_count(tree, _CoreoNT('<iregexp_literal>'))

def count_ire_alt(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_alt>'))

def count_ire_branch(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_branch>'))

def count_ire_piece(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_piece>'))

def count_ire_char_class(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_char_class>'))

def count_ire_char_class_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_char_class_expr>'))

def count_ire_cce1(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_cce1>'))

def count_ire_quantifier(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_quantifier>'))

def count_ire_range_quantifier(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_range_quantifier>'))

def count_search_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<search_expr>'))

def count_and_tail(tree):
    return _coreografa_count(tree, _CoreoNT('<and_tail>'))

def count_item(tree):
    return _coreografa_count(tree, _CoreoNT('<item>'))

def count_doc_string(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_string>'))

def count_letter(tree):
    return _coreografa_count(tree, _CoreoNT('<letter>'))

def count_wide_more_item(tree):
    return _coreografa_count(tree, _CoreoNT('<wide_more_item>'))

"""Input properties for the pyjsonpath_tailored subject (RQ1 tailored setting).

Copied from subjects/jsonpath_py/user_def_functions.py; `n_doc_nodes` and
`n_function_calls` are added for the axis the tailored grammar varies
(pyjsonpath_tailored.fan header). Both are structural counts; none runs an
SUT.

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

# TAILORED grammar for python-jsonpath 1.3.2 -> 2.0.0 (RQ1, tailored setting).
# A sub-language of the frozen spec grammar subjects/jsonpath_py/jsonpath_py.fan:
# every string this grammar generates is generated by that grammar (checked by
# parsing a sample with it: subjects/jpython_tailored/check_sublanguage.py
# pyjsonpath_tailored). Written 2026-10-02 from the diff of the commit the pair
# was mined for.
#
# What the commit changes: 7ed181a ("Cache checked and mapped regex patterns")
# rewrites jsonpath/function_extensions/match.py and search.py. Before, every
# CALL of match()/search() ran iregexp check(pattern) and map_re(pattern) (when
# those optional packages are installed) and then re.fullmatch / re.search on
# the raw pattern string; after, the compiled pattern (or None for an invalid
# one) is kept in a 300-entry LRUCache keyed by the pattern string, and the
# call does a cache lookup plus pattern.fullmatch / pattern.search. The saving
# is per function call, i.e. per node a filter containing match()/search() is
# evaluated against, and is largest when the value is short (regex work small
# relative to the per-call overhead) and the pattern repeats.
#
# Expected outcome: null. The diagnosis of 2026-10-02 found that the cached
# code path is not the 1.3.2 -> 2.0.0 difference that matters: 1.3.2 already
# goes through re's own compiled-pattern cache, and neither env has the
# optional regex/iregexp-check packages (py_runner.py docstring), so the
# check/map_re work the cache removes never ran in 1.3.2 either. The grammar is
# tailored to the diff regardless; a null here is a valid result.
#
# Input shape that exercises the diff: a filter whose test is one or more
# match()/search() calls, applied by a child or descendant filter segment to a
# WIDE array whose elements are short strings or small objects with string
# members, so the function is called once per element (per node under `..`).
#
# Restrictions relative to jsonpath_py.fan (all remove alternatives, fix a
# vocabulary choice, or bound a repetition; no construct is added):
#
# | spec rule                     | here                                                   |
# |-------------------------------|--------------------------------------------------------|
# | jsonpath_query: "$" s_segment*| "$" filter_segment, optionally after one ".*" / "[*]"  |
# | segment                       | "[" filter_selector "]" or ".." "[" filter_selector "]"|
# |                               | (bracketed_selection of one filter, no blanks)         |
# | filter_selector               | "?" logical_expr, no blanks                            |
# | logical_or_expr               | a single logical_and_expr (no "||")                    |
# | logical_and_expr              | basic_expr ("&&" basic_expr)* with and_op = "&&"       |
# | basic_expr                    | test_expr only                                         |
# | test_expr                     | logical_function_expr, optionally "!"-prefixed (S="")  |
# | match/search arguments        | S = ""; value_argument = rel_singular_query "@",       |
# |                               | "@.a" or "@.b"; regex_argument = iregexp_literal only  |
# | ire_* (I-Regexp)              | same rules, atoms over {x,y,z} and ".", no nested      |
# |                               | "(" ")" groups, at most 4 pieces per branch            |
# | doc ws                        | "" everywhere                                          |
# | doc_root                      | nonempty_array only (the wide array)                   |
# | root items: more_value*       | wide_more_item* (renamed so `stratify` can band the    |
# |                               | width; several bands, set in example.py)               |
# | value of an element           | doc_string, or an object with fixed member names "a"   |
# |                               | or "a","b" (one-<name_char> names: never collide)      |
# | doc_chars                     | the "" alternative dropped: match()/search() see a    |
# |                               | non-empty string (letters over {x,y,z}, as in the spec)|
#
# The spec grammar's `where unique_member_names` clause holds by construction
# (inner objects have fixed distinct names) and is kept anyway.
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

# ---- query: one filter segment calling match()/search() --------------------
<jsonpath_query> ::= "$" <filter_segment> | "$" <pre_segment> <filter_segment>
<pre_segment> ::= "." <wildcard_selector> | "[" <wildcard_selector> "]"
<wildcard_selector> ::= "*"
<filter_segment> ::= "[" <filter_selector> "]" | ".." "[" <filter_selector> "]"
<filter_selector> ::= "?" <logical_expr>
<logical_expr> ::= <logical_and_expr>
<logical_and_expr> ::= <basic_expr> | <basic_expr> <and_tail>+
<and_tail> ::= "&&" <basic_expr>
<basic_expr> ::= <test_expr>
<test_expr> ::= <logical_function_expr> | "!" <logical_function_expr>
<logical_function_expr> ::= <match_expr> | <search_expr>
<match_expr> ::= "match(" <value_argument> "," <iregexp_literal> ")"
<search_expr> ::= "search(" <value_argument> "," <iregexp_literal> ")"
<value_argument> ::= "@" | "@.a" | "@.b"
<iregexp_literal> ::= "'" <ire_regexp> "'" | "\"" <ire_regexp> "\""
<ire_regexp> ::= <ire_branch> | <ire_branch> <ire_alt>
<ire_alt> ::= "|" <ire_branch>
<ire_branch> ::= <ire_piece>{1,4}
<ire_piece> ::= <ire_atom> | <ire_atom> <ire_quantifier>
<ire_quantifier> ::= "*" | "+" | "?" | <ire_range_quantifier>
<ire_range_quantifier> ::= "{0,1}" | "{0,2}" | "{1,2}" | "{1,3}" | "{2,4}"
<ire_atom> ::= "x" | "y" | "z" | <ire_char_class>
<ire_char_class> ::= "." | <ire_char_class_expr>
<ire_char_class_expr> ::= "[" <ire_caret_opt> <ire_cce1>{1,3} "]"
<ire_caret_opt> ::= "" | "^"
<ire_cce1> ::= "x" | "y" | "z" | "x-z"

# ---- document: one wide array ------------------------------------------------
<doc> ::= <wide_array>
<wide_array> ::= "[" <item> <wide_more_item>* "]"
<wide_more_item> ::= "," <item>
<item> ::= <doc_string> | "{\"a\":" <doc_string> "}" | "{\"a\":" <doc_string> ",\"b\":" <doc_string> "}"
<doc_string> ::= "\"" <doc_chars> "\""
<doc_chars> ::= <letter> | <letter> <letter> | <letter> <letter> <letter>+
<letter> ::= "x" | "y" | "z"

where unique_member_names(<start>)

where doc_depth(<start>) >= 1.166667
where doc_depth(<start>) <= 1.333333
