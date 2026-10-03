from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_member(tree):
    return _coreografa_count(tree, _CoreoNT('<member>'))

def count_key_ascii(tree):
    return _coreografa_count(tree, _CoreoNT('<key_ascii>'))

def count_key_latin1(tree):
    return _coreografa_count(tree, _CoreoNT('<key_latin1>'))

def count_literal(tree):
    return _coreografa_count(tree, _CoreoNT('<literal>'))

def count_null(tree):
    return _coreografa_count(tree, _CoreoNT('<null>'))

def count_true(tree):
    return _coreografa_count(tree, _CoreoNT('<true>'))

def count_false(tree):
    return _coreografa_count(tree, _CoreoNT('<false>'))

def count_number(tree):
    return _coreografa_count(tree, _CoreoNT('<number>'))

def count_string(tree):
    return _coreografa_count(tree, _CoreoNT('<string>'))

def count_str_one_wide(tree):
    return _coreografa_count(tree, _CoreoNT('<str_one_wide>'))

def count_ascii_run(tree):
    return _coreografa_count(tree, _CoreoNT('<ascii_run>'))

def count_str_ascii(tree):
    return _coreografa_count(tree, _CoreoNT('<str_ascii>'))

def count_str_latin1(tree):
    return _coreografa_count(tree, _CoreoNT('<str_latin1>'))

def count_more_member(tree):
    return _coreografa_count(tree, _CoreoNT('<more_member>'))

"""Input properties for the tailored orjson subject.

Occurrence counts of the grammar's non-terminals (`count_member`,
`count_str_latin1`, `count_str_one_wide`, `count_key_latin1`, `count_null`,
...) are derived from orjson_tailored.fan by core/grammar_props.py and
need no function here. Declared here is what no occurrence count measures:
document size in bytes and how densely it packs member names, the axis the
3.10.2 change is expected to scale with, and the share of non-ASCII string
content in the Latin-1 range, the axis of the 3.10.6 change.

`PROPERTIES` declares which functions are features; the rest are helpers.
"""

PROPERTIES = ["num_pairs", "doc_bytes", "key_density", "latin1_char_share"]

# num_pairs is exactly the derived member count; keep the domain's column name.
ALIASES = {"num_pairs": ["count_member", "count_more_member"]}


def _decoded_strings(text):
    """Every member name and string value, decoded. The tailored grammar has
    no escapes, so a string is the text between two quotes."""
    return text.split('"')[1::2]


def num_pairs(tree):
    """Members of the root object."""
    return str(tree).count('":')


def doc_bytes(tree):
    """UTF-8 size of the document."""
    return len(str(tree).encode("utf-8"))


def key_density(tree):
    """Member names per byte of document."""
    text = str(tree)
    return text.count('":') / max(1, len(text.encode("utf-8")))


def latin1_char_share(tree):
    """Fraction of non-ASCII string characters that are below U+0100."""
    wide = [c for s in _decoded_strings(str(tree)) for c in s if ord(c) >= 0x80]
    if not wide:
        return 0.0
    return sum(1 for c in wide if ord(c) < 0x100) / len(wide)

# TAILORED grammar for orjson 3.10.1 .. 3.10.6 (RQ1, tailored setting).
#
# A sub-language of the frozen domain grammar subjects/json/json.fan
# (RFC 8259 under I-JSON), shaped from the two commits in this version range
# that change the parse path for flat objects and strings, as a developer
# investigating them would write it. The tool's loop runs on it unaided.
#
# Commits read
# ------------
# 3.10.1 -> 3.10.2
#   a1a2ed9  rewrites the yyjson -> PyObject population
#            (src/deserialize/yyjson.rs), the per-value/per-container work
#            of loads, and
#   fcbd9a4  doubles the direct-mapped object-key cache (KeyMap,
#            src/deserialize/cache.rs) from 1024 to 2048 slots; every member
#            name of <= 64 bytes goes through it.
#   Both change per-MEMBER cost of an object: every member pays a key-cache
#   lookup and one value construction. The share of parse time they touch is
#   largest when an object has many members with cheap values, i.e.
#   key-dense objects with short keys and scalar values. Long string values
#   or nested containers spend their time elsewhere and dilute the change.
#   The cache doubling only matters once an object has more distinct short
#   names than the old 1024 slots, and stops helping past 2048.
# 3.10.5 -> 3.10.6
#   c369ea4  rewrites PyUnicode creation for every decoded string and key
#            (src/str/create.rs -> scalar.rs): one byte scan picks the
#            1/2/4-byte PyUnicode kind. Only the non-ASCII branch changed;
#            the 1-byte kind is the Latin-1 case (max codepoint < U+0100),
#            and
#   9382058  switches the key-cache hash from ahash to xxh3_64, one hash per
#            member name of <= 64 bytes.
#   The str path only differs from the old one when a string is non-ASCII,
#   and the 1-byte kind only when every char is below U+0100. json.fan picks
#   a non-ASCII char uniformly among the 2/3/4-byte UTF-8 classes, so a
#   generated non-ASCII string almost always contains a char above U+0100 and
#   usually an astral one, and never exercises the Latin-1 path.
# 3.10.3 -> 3.10.4 (c96351f removes null checks) is not targeted; `null` stays
#   in the value vocabulary so the commit's code still runs.
#
# Input shape
# -----------
# One flat object at the root, 25 to ~2000 members, short keys (3-6 chars),
# scalar values: short integers, true/false/null, and short strings. Strings
# come in three shapes, each its own non-terminal so the loop can count and
# target them:
#   <str_ascii>       ASCII only (old and new str paths coincide: control);
#   <str_latin1>      at least one char in U+0080-U+00FF, all chars < U+0100
#                     (the new 1-byte non-ASCII path);
#   <str_one_wide>    ASCII plus exactly one char in U+0080-U+FFFF minus
#                     surrogates/noncharacters (the mixed case, where the
#                     rewrite has to widen a mostly-ASCII string).
# Keys are ASCII or Latin-1 by the same reasoning (keys go through the same
# str creation plus the xxh3-keyed cache).
# Astral chars, escapes, floats, big ints and nesting are removed: they are
# either outside both diffs or dilute the per-member cost the diffs change.
#
# Stratification (example.py): `<more_member>` banded into member counts
# 25-60, 60-200, 200-800 (population rewrite, cache not yet full) and
# 800-2000 (crosses the old 1024-slot cache size, up to the new 2048).
#
# Sub-language of json.fan, rule by rule
# --------------------------------------
# | here                  | json.fan                    | restriction                          |
# |-----------------------|-----------------------------|--------------------------------------|
# | <start>               | <start> ::= ws root ws      | ws = "" (one alternative of <ws>)    |
# | <root_value>          | <root_value>                | only the <object> alternative        |
# | <object>              | <object>                    | non-empty alternative only; ws = ""  |
# | <more_member>         | <more_member>               | ws = ""                              |
# | <member>              | <member> ::= string : value | ws = ""; name is <key>, value <value>|
# | <key>                 | <string>                    | 3-6 chars from [0-9A-Za-z_] or a     |
# |                       |                             | Latin-1 form; no escapes             |
# | <value>               | <value>                     | drop <object>, <array>               |
# | <number>              | <integer_number>            | int of at most 5 digits, opt. minus  |
# | <str_*>               | <string>                    | chars drawn from json.fan's          |
# |                       |                             | <unescaped_alnum>, <unescaped_ascii_ |
# |                       |                             | other>, <unescaped_utf8_2>/<..._3>   |
# |                       |                             | classes only; length 0-17            |
# | <false> <null> <true> | same                        | unchanged                            |
# Every regex below is a subset of the json.fan rule in the right column:
# ASCII here is [0-9A-Za-z] (= <unescaped_alnum>) plus
# [ !#-/:-@\[\]-`{-~] (subset of <unescaped_ascii_other>, which also has
# DEL); [\x80-\xff] is a subset of <unescaped_utf8_2> [\x80-\u07ff];
# <wide_char> is <unescaped_utf8_2> plus json.fan's own <unescaped_utf8_3>
# blocks verbatim (surrogates and noncharacters already excluded there).
# Keys and strings never contain `"` or `\`, so they need no escape.
# The I-JSON duplicate-name constraint is kept verbatim.
#
# Regex terminals instead of per-char non-terminals keep a member at ~6
# derivation nodes, so a 2000-member band fits under the framework's
# 30,000-node structural ceiling (core/targeting.MAX_STRUCTURAL_NODES)
# without Fandango falling back to the cheapest derivation for every member.

<start> ::= <root_value>
<root_value> ::= <object>

# RFC 8259 §4 object, non-empty, no whitespace
<object> ::= "{" <member> <more_member>+ "}"
<more_member> ::= "," <member>
<member> ::= <key> ":" <value>

# Member names: ASCII, or Latin-1 (at least one char in U+00A0-U+00FF)
<key> ::= <key_ascii> | <key_latin1>
<key_ascii> ::= r"\"[0-9A-Za-z_]{3,6}\""
<key_latin1> ::= r"\"[0-9A-Za-z]{0,2}[\xa0-\xff][0-9A-Za-z\xa0-\xff]{2,3}\""

# Scalar values only
<value> ::= <number> | <string> | <literal>
<literal> ::= <false> | <null> | <true>
<false> ::= "false"
<null> ::= "null"
<true> ::= "true"
<number> ::= r"-?(0|[1-9][0-9]{0,4})"

<string> ::= <str_ascii> | <str_latin1> | <str_one_wide>
<str_ascii> ::= r"\"[0-9A-Za-z !#-/:-@\[\]-`{-~]{0,16}\""
<str_latin1> ::= r"\"[0-9A-Za-z ]{0,4}[\x80-\xff][0-9A-Za-z \x80-\xff]{0,11}\""
<str_one_wide> ::= "\"" <ascii_run> <wide_char> <ascii_run> "\""
<ascii_run> ::= "" | r"[0-9A-Za-z ]{1,8}"
<wide_char> ::= r"[\x80-\xff]" | r"[\u0100-\u07ff]" | r"[\u0800-\u0fff]" | r"[\u1000-\u1fff]" | r"[\u2000-\u2fff]" | r"[\u3000-\u3fff]" | r"[\u4000-\u4fff]" | r"[\u5000-\u5fff]" | r"[\u6000-\u6fff]" | r"[\u7000-\u7fff]" | r"[\u8000-\u8fff]" | r"[\u9000-\u9fff]" | r"[\ua000-\uafff]" | r"[\ub000-\ubfff]" | r"[\uc000-\ucfff]" | r"[\ud000-\ud7ff]" | r"[\ue000-\uefff]" | r"[\uf000-\ufdcf\ufdf0-\ufffd]"


# I-JSON (RFC 7493) §2.3, verbatim from json.fan: no duplicate member names.
import json as _ijson_json

def _ijson_member_names(obj):
    """Decoded names of the members directly inside one <object> node."""
    names = []
    stack = list(obj.children)
    while stack:
        node = stack.pop()
        sym = str(node.symbol)
        if sym == "<member>":
            names.append(_ijson_json.loads(str(node.children[0])))
        elif sym == "<more_member>":
            stack.extend(node.children)
    return names

def ijson_unique_names(obj):
    names = _ijson_member_names(obj)
    return len(names) == len(set(names))

where forall <o> in <object>: ijson_unique_names(<o>)

where key_density(<start>) >= 0.07592869465209891
where key_density(<start>) <= 0.07850488786659
