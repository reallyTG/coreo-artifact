# TAILORED grammar for simplejson 3.20.2 -> 4.0.0 (RQ1, tailored setting).
#
# A sub-language of the frozen domain grammar subjects/json/json.fan
# (RFC 8259 under I-JSON), shaped from the commit's diff as a developer
# investigating it would write it. The tool's loop runs on it unaided.
#
# Commit read
# -----------
# e2e5f0b  (#369) In the C scanner's _parse_object, interning a decoded
#          member name through the memo dict used to be
#          PyDict_GetItemWithError followed by PyDict_SetItem (two probes);
#          it is now one PyDict_SetDefault (the path taken on CPython < 3.13,
#          which is what the envs run). The change is one memo operation per
#          MEMBER NAME and touches nothing in value decoding.
#   So the work it changes is largest, relative to the whole parse, in
#   objects with many members whose names are short (cheap to decode, so the
#   memo probe is a large share of the per-member cost) and whose values are
#   cheap scalars. Strings with non-ASCII content, escapes, floats and
#   nested containers spend their time in code the commit does not touch.
#
# Input shape
# -----------
# One flat object at the root, 25 to ~4000 members (the memo dict grows with
# the number of distinct names, so wide objects also exercise its resizes),
# names of 3-6 ASCII chars, values short integers, true/false/null or short
# ASCII strings.
#
# Stratification (example.py): `<more_member>` banded into member counts
# 25-100, 100-500, 500-2000 and 2000-4000.
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
# | <key>                 | <string>                    | 3-6 chars from [0-9A-Za-z_]          |
# | <value>               | <value>                     | drop <object>, <array>               |
# | <number>              | <integer_number>            | int of at most 5 digits, opt. minus  |
# | <string>              | <string>                    | 0-12 chars of [0-9A-Za-z ] only      |
# | <false> <null> <true> | same                        | unchanged                            |
# [0-9A-Za-z] is json.fan's <unescaped_alnum>; space and `_` are in its
# <unescaped_ascii_other>. No `"` or `\` can occur, so no escapes are needed.
# The I-JSON duplicate-name constraint is kept verbatim.
#
# Regex terminals instead of per-char non-terminals keep a member at ~6
# derivation nodes, so the widest band fits under the framework's
# 30,000-node structural ceiling (core/targeting.MAX_STRUCTURAL_NODES).
#
# Expected outcome, from the commit: at most a few percent per member name,
# so the pair may well stay below the detection band on this grammar too.

<start> ::= <root_value>
<root_value> ::= <object>

# RFC 8259 §4 object, non-empty, no whitespace
<object> ::= "{" <member> <more_member>{499,1999} "}"
<more_member> ::= "," <member>
<member> ::= <key> ":" <value>

<key> ::= r"\"[0-9A-Za-z_]{3,6}\""

# Scalar values only
<value> ::= <number> | <literal> | <string>
<literal> ::= <false> | <null> | <true>
<false> ::= "false"
<null> ::= "null"
<true> ::= "true"
<number> ::= r"-?(0|[1-9][0-9]{0,4})"
<string> ::= r"\"[0-9A-Za-z ]{0,12}\""


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
