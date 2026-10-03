from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_s_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<s_segment>'))

def count_B(tree):
    return _coreografa_count(tree, _CoreoNT('<B>'))

def count_child_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<child_segment>'))

def count_wildcard_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<wildcard_selector>'))

def count_member_name_shorthand(tree):
    return _coreografa_count(tree, _CoreoNT('<member_name_shorthand>'))

def count_name_first(tree):
    return _coreografa_count(tree, _CoreoNT('<name_first>'))

def count_name_char(tree):
    return _coreografa_count(tree, _CoreoNT('<name_char>'))

def count_bracketed_selection(tree):
    return _coreografa_count(tree, _CoreoNT('<bracketed_selection>'))

def count_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<selector>'))

def count_index_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<index_selector>'))

def count_int(tree):
    return _coreografa_count(tree, _CoreoNT('<int>'))

def count_pos_int(tree):
    return _coreografa_count(tree, _CoreoNT('<pos_int>'))

def count_DIGIT1(tree):
    return _coreografa_count(tree, _CoreoNT('<DIGIT1>'))

def count_DIGIT(tree):
    return _coreografa_count(tree, _CoreoNT('<DIGIT>'))

def count_name_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<name_selector>'))

def count_name_sq_chars(tree):
    return _coreografa_count(tree, _CoreoNT('<name_sq_chars>'))

def count_name_sq_mixed(tree):
    return _coreografa_count(tree, _CoreoNT('<name_sq_mixed>'))

def count_name_sq_special(tree):
    return _coreografa_count(tree, _CoreoNT('<name_sq_special>'))

def count_escapable(tree):
    return _coreografa_count(tree, _CoreoNT('<escapable>'))

def count_hexchar(tree):
    return _coreografa_count(tree, _CoreoNT('<hexchar>'))

def count_high_surrogate(tree):
    return _coreografa_count(tree, _CoreoNT('<high_surrogate>'))

def count_D(tree):
    return _coreografa_count(tree, _CoreoNT('<D>'))

def count_HEXDIG(tree):
    return _coreografa_count(tree, _CoreoNT('<HEXDIG>'))

def count_non_surrogate(tree):
    return _coreografa_count(tree, _CoreoNT('<non_surrogate>'))

def count_oct_digit(tree):
    return _coreografa_count(tree, _CoreoNT('<oct_digit>'))

def count_non_d_hex(tree):
    return _coreografa_count(tree, _CoreoNT('<non_d_hex>'))

def count_low_surrogate(tree):
    return _coreografa_count(tree, _CoreoNT('<low_surrogate>'))

def count_name_sq_char(tree):
    return _coreografa_count(tree, _CoreoNT('<name_sq_char>'))

def count_name_dq_chars(tree):
    return _coreografa_count(tree, _CoreoNT('<name_dq_chars>'))

def count_name_dq_mixed(tree):
    return _coreografa_count(tree, _CoreoNT('<name_dq_mixed>'))

def count_name_dq_special(tree):
    return _coreografa_count(tree, _CoreoNT('<name_dq_special>'))

def count_name_dq_char(tree):
    return _coreografa_count(tree, _CoreoNT('<name_dq_char>'))

def count_filter_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<filter_selector>'))

def count_logical_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<logical_expr>'))

def count_or_tail(tree):
    return _coreografa_count(tree, _CoreoNT('<or_tail>'))

def count_logical_and_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<logical_and_expr>'))

def count_and_tail(tree):
    return _coreografa_count(tree, _CoreoNT('<and_tail>'))

def count_basic_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<basic_expr>'))

def count_test_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<test_expr>'))

def count_filter_query(tree):
    return _coreografa_count(tree, _CoreoNT('<filter_query>'))

def count_abs_query(tree):
    return _coreografa_count(tree, _CoreoNT('<abs_query>'))

def count_slice_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<slice_selector>'))

def count_more_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<more_selector>'))

def count_descendant_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<descendant_segment>'))

def count_rel_query(tree):
    return _coreografa_count(tree, _CoreoNT('<rel_query>'))

def count_S(tree):
    return _coreografa_count(tree, _CoreoNT('<S>'))

def count_logical_function_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<logical_function_expr>'))

def count_search_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<search_expr>'))

def count_value_argument(tree):
    return _coreografa_count(tree, _CoreoNT('<value_argument>'))

def count_literal(tree):
    return _coreografa_count(tree, _CoreoNT('<literal>'))

def count_number(tree):
    return _coreografa_count(tree, _CoreoNT('<number>'))

def count_exp(tree):
    return _coreografa_count(tree, _CoreoNT('<exp>'))

def count_sign_opt(tree):
    return _coreografa_count(tree, _CoreoNT('<sign_opt>'))

def count_frac(tree):
    return _coreografa_count(tree, _CoreoNT('<frac>'))

def count_string_literal(tree):
    return _coreografa_count(tree, _CoreoNT('<string_literal>'))

def count_dq_chars(tree):
    return _coreografa_count(tree, _CoreoNT('<dq_chars>'))

def count_letter(tree):
    return _coreografa_count(tree, _CoreoNT('<letter>'))

def count_dq_mixed(tree):
    return _coreografa_count(tree, _CoreoNT('<dq_mixed>'))

def count_dq_special(tree):
    return _coreografa_count(tree, _CoreoNT('<dq_special>'))

def count_dq_char(tree):
    return _coreografa_count(tree, _CoreoNT('<dq_char>'))

def count_sq_chars(tree):
    return _coreografa_count(tree, _CoreoNT('<sq_chars>'))

def count_sq_mixed(tree):
    return _coreografa_count(tree, _CoreoNT('<sq_mixed>'))

def count_sq_special(tree):
    return _coreografa_count(tree, _CoreoNT('<sq_special>'))

def count_sq_char(tree):
    return _coreografa_count(tree, _CoreoNT('<sq_char>'))

def count_singular_query(tree):
    return _coreografa_count(tree, _CoreoNT('<singular_query>'))

def count_abs_singular_query(tree):
    return _coreografa_count(tree, _CoreoNT('<abs_singular_query>'))

def count_s_singular_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<s_singular_segment>'))

def count_index_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<index_segment>'))

def count_name_segment(tree):
    return _coreografa_count(tree, _CoreoNT('<name_segment>'))

def count_rel_singular_query(tree):
    return _coreografa_count(tree, _CoreoNT('<rel_singular_query>'))

def count_value_function_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<value_function_expr>'))

def count_length_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<length_expr>'))

def count_count_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<count_expr>'))

def count_value_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<value_expr>'))

def count_regex_argument(tree):
    return _coreografa_count(tree, _CoreoNT('<regex_argument>'))

def count_iregexp_literal(tree):
    return _coreografa_count(tree, _CoreoNT('<iregexp_literal>'))

def count_ire_regexp(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_regexp>'))

def count_ire_branch(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_branch>'))

def count_ire_piece(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_piece>'))

def count_ire_alt(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_alt>'))

def count_ire_char_class(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_char_class>'))

def count_ire_quantifier(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_quantifier>'))

def count_ire_range_quantifier(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_range_quantifier>'))

def count_match_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<match_expr>'))

def count_logical_not_op(tree):
    return _coreografa_count(tree, _CoreoNT('<logical_not_op>'))

def count_comparison_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<comparison_expr>'))

def count_comparable(tree):
    return _coreografa_count(tree, _CoreoNT('<comparable>'))

def count_paren_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<paren_expr>'))

def count_ire_char_class_expr(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_char_class_expr>'))

def count_ire_cce1(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_cce1>'))

def count_ire_normal_char(tree):
    return _coreografa_count(tree, _CoreoNT('<ire_normal_char>'))

def count_ws(tree):
    return _coreografa_count(tree, _CoreoNT('<ws>'))

def count_nonempty_array(tree):
    return _coreografa_count(tree, _CoreoNT('<nonempty_array>'))

def count_value(tree):
    return _coreografa_count(tree, _CoreoNT('<value>'))

def count_array(tree):
    return _coreografa_count(tree, _CoreoNT('<array>'))

def count_doc_string(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_string>'))

def count_object(tree):
    return _coreografa_count(tree, _CoreoNT('<object>'))

def count_nonempty_object(tree):
    return _coreografa_count(tree, _CoreoNT('<nonempty_object>'))

def count_doc_number(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_number>'))

def count_doc_exp(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_exp>'))

def count_more_value(tree):
    return _coreografa_count(tree, _CoreoNT('<more_value>'))

def count_doc_mixed(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_mixed>'))

def count_doc_special(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_special>'))

def count_doc_char(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_char>'))

def count_member(tree):
    return _coreografa_count(tree, _CoreoNT('<member>'))

def count_more_member(tree):
    return _coreografa_count(tree, _CoreoNT('<more_member>'))

def count_doc_escape(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_escape>'))

def count_doc_name_mixed(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_name_mixed>'))

def count_doc_name_special(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_name_special>'))

def count_doc_name_char(tree):
    return _coreografa_count(tree, _CoreoNT('<doc_name_char>'))

"""Input properties for the Python JSONPath subject.

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

# JSONPath query plus JSON document, for four Python implementations.
#
# One input encodes both halves, separated by a marker line:
#
#     <query>
#     @@@
#     <json document>
#
# The runner splits on the first "\n@@@\n". Neither half can produce "@@@":
# the document has no "@" outside \u escapes, and in a query "@" is always
# followed by a segment, blank space, an operator or ")", never by "@".
#
# The query side transcribes the ABNF of RFC 9535 (collected in its Appendix A)
# rule by rule; the document side transcribes RFC 8259 under the I-JSON profile
# (RFC 7493), which RFC 9535 §2.1 requires of the query argument. It is the
# grammar of subjects/jsonpath_js without that subject's class-4 exclusions,
# because none of them applies here: on the per-construct probe, python-jsonpath,
# jsonpath-rfc9535 and jsonpath-python accept every construct (jsonpath-rfc9535
# rejects the literal `0e1`, an RFC-valid number, which is a bug and stays in;
# jsonpath-python accepts but returns no match for most RFC-form filters), and
# the one engine that rejects whole constructs is jsonpath-ng (below). Everything that
# can grow is `*`, `+` or recursion; the only finite bounds are I-JSON's.
#
# Function well-typedness (RFC 9535 §2.4.3) is encoded by construction, as in the
# JS subject: comparables take the ValueType functions (length, count, value),
# test-exprs the LogicalType ones (match, search), and count/value take a
# filter-query.
#
# Deviations. Classes: (1) language-preserving rewrite, distribution only;
# (2) restriction to a named profile of another spec; (3) finite lexical
# vocabulary; (4) construct an engine rejects on >=95% of probe inputs.
#
# | rule(s)                        | departure                                              | class |
# |--------------------------------|--------------------------------------------------------|-------|
# | member_name_shorthand, name_*  | name characters over {a,b,c,d} so queries hit doc keys | 3 |
# | name_string_literal            | unescaped characters over {a,b,c,d}                    | 3 |
# | string_literal, doc_string     | unescaped characters over {x,y,z}                      | 3 |
# | ire_* (I-Regexp, RFC 9485)     | characters over {a-d,x-z}; no escapes or \p{..};       | 3 |
# |                                | {n,m} from a fixed list with n<=m                      |   |
# | regex_argument                 | a string pattern is always an I-Regexp literal         | 3 |
# | *_chars, member_name_shorthand,| split into length alternatives plus a "contains an     | 1 |
# | pos_int                        | escape" alternative                                    |   |
# | rel_query, abs_query,          | trailing `*` written as 1/2/3+ alternatives            | 1 |
# | *_singular_query, or/and tails |                                                        |   |
# | s_segment, comma_s, slice,     | optional blanks written as alternatives, not a         | 1 |
# | or_op, and_op, filter_selector,| nullable <S> (parser note)                             |   |
# | comparison_op_s, paren_body,   |                                                        |   |
# | bracketed_selection            |                                                        |   |
# | int, doc_int                   | at most 15 digits, so below 2^53 (16-digit values up to|
# |                                | 2^53-1 are left out: conservative)                     | 2: RFC 9535 §2.1 / RFC 7493 §2.2 |
# | doc_exp                        | exponent 1-2 digits (magnitude within a double)        | 2: RFC 7493 §2.2 |
# | doc_escape (hexchar)           | \u escapes are non-surrogates or surrogate pairs       | 2: RFC 7493 §2.1 |
# | where unique_member_names      | member names unique within an object                   | 2: RFC 7493 §2.3 |
# | doc_root                       | root is a non-empty object or array                    | none: see below |
#
# The root restriction fits no class. A scalar or empty root makes every query
# select at most `$`, so those inputs carry no signal; there is no class-1 way
# to keep them rare, because rarity under Fandango's even choice needs
# duplicated alternatives, and Fandango's parser is exponential on the
# resulting ambiguity (19 s for `{"a":[1,2]}`, measured 2026-09-30).
#
# Not enforced: I-JSON §2.2's SHOULD on precision.
#
# jsonpath-ng. On the class-4 probe (2026-09-30, 50 inputs per construct)
# jsonpath-ng rejects 100% of: `&&`, `||`, `!`, parenthesised expressions, all
# five function extensions, path-to-path comparison, absolute queries in
# filters, number literals with a fraction or exponent, filters under `..`,
# unions other than name-only lists, blank space around union commas, inside
# paren-exprs and in function arguments. Excluding all of that would leave
# filters of one comparison against an integer or string, the grammar the
# subject had before. So nothing is excluded for it: jsonpath-ng is flagged
# instead (A2 report, 2026-09-30), and it fails most generated inputs.
# Partial disagreement (jsonpath-python returning 0 for some filters, `[::0]`
# errors in jsonpath-python 40% and jsonpath-ng 36%) stays in the grammar,
# because the harness filters disagreeing inputs per engine pair at scoring
# time.
#
# Parser note. Fandango's parser rejects valid input when several nullable items
# complete at one position, and is exponential on ambiguous nullable rules; the
# framework drops any seed its parser rejects. Optional blanks and trailing
# repetitions inside filters are therefore written as alternatives.
import json as _json

def unique_member_names(tree):
    # I-JSON §2.3: the names within an object MUST be unique. Checked on the
    # document half by parsing it with a pairs hook.
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

# ---- RFC 9535 §2.1.1 syntax ------------------------------------------------
# §2.1.1 jsonpath-query = root-identifier segments
# §2.1.1 segments = *(S segment)
# (parse-safe forms inside filters: see "Parser note" in the header)
<jsonpath_query> ::= "$" <s_segment>{24,28}
# (S segment) with the optional blanks written out (parser note in the header)
<s_segment> ::= <segment> | <B>+ <segment>
# §2.1.1 B = %x20 / %x09 / %x0A / %x0D ; S = *B
<B> ::= " " | "\t" | "\n" | "\r"
<S> ::= "" | <B>+

# ---- §2.3 selectors -------------------------------------------------------
# §2.3 selector = name-selector / wildcard-selector / slice-selector / index-selector / filter-selector
<selector> ::= <name_selector> | <wildcard_selector> | <slice_selector> | <index_selector> | <filter_selector>

# §2.3.1.1 name-selector = string-literal
<name_selector> ::= <name_string_literal>
# §2.3.1.1 string-literal = %x22 *double-quoted %x22 / %x27 *single-quoted %x27
# (name vocabulary, class 3; short/long split, class 1)
<name_string_literal> ::= "\"" <name_dq_chars> "\"" | "'" <name_sq_chars> "'"
<name_dq_chars> ::= "" | <name_char> | <name_char> <name_char> | <name_char> <name_char> <name_char>+ | <name_dq_mixed>
<name_dq_mixed> ::= <name_char>* <name_dq_special> <name_dq_char>*
<name_dq_char> ::= <name_char> | <name_dq_special>
<name_dq_special> ::= "'" | "\\\"" | "\\" <escapable>
# §2.3.1.1 single-quoted = unescaped / %x22 / ESC %x27 / ESC escapable
<name_sq_chars> ::= "" | <name_char> | <name_char> <name_char> | <name_char> <name_char> <name_char>+ | <name_sq_mixed>
<name_sq_mixed> ::= <name_char>* <name_sq_special> <name_sq_char>*
<name_sq_char> ::= <name_char> | <name_sq_special>
<name_sq_special> ::= "\"" | "\\'" | "\\" <escapable>

# §2.3.1.1 string-literal, used as a comparison literal (letter vocabulary, class 3)
<string_literal> ::= "\"" <dq_chars> "\"" | "'" <sq_chars> "'"
<dq_chars> ::= "" | <letter> | <letter> <letter> | <letter> <letter> <letter>+ | <dq_mixed>
<dq_mixed> ::= <letter>* <dq_special> <dq_char>*
<dq_char> ::= <letter> | <dq_special>
<dq_special> ::= "'" | "\\\"" | "\\" <escapable>
# §2.3.1.1 single-quoted = unescaped / %x22 / ESC %x27 / ESC escapable
<sq_chars> ::= "" | <letter> | <letter> <letter> | <letter> <letter> <letter>+ | <sq_mixed>
<sq_mixed> ::= <letter>* <sq_special> <sq_char>*
<sq_char> ::= <letter> | <sq_special>
<sq_special> ::= "\"" | "\\'" | "\\" <escapable>
# §2.3.1.1 escapable = %x62 / %x66 / %x6E / %x72 / %x74 / "/" / "\" / (%x75 hexchar)
<escapable> ::= "b" | "f" | "n" | "r" | "t" | "/" | "\\" | "u" <hexchar>
# §2.3.1.1 hexchar = non-surrogate / (high-surrogate "\" %x75 low-surrogate)
<hexchar> ::= <non_surrogate> | <high_surrogate> "\\u" <low_surrogate>
# §2.3.1.1 non-surrogate = ((DIGIT / "A"/"B"/"C" / "E"/"F") 3HEXDIG) / ("D" %x30-37 2HEXDIG)
<non_surrogate> ::= <non_d_hex> <HEXDIG> <HEXDIG> <HEXDIG> | <D> <oct_digit> <HEXDIG> <HEXDIG>
<non_d_hex> ::= <DIGIT> | "A" | "B" | "C" | "E" | "F" | "a" | "b" | "c" | "e" | "f"
<D> ::= "D" | "d"
<oct_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7"
# §2.3.1.1 high-surrogate = "D" ("8"/"9"/"A"/"B") 2HEXDIG
<high_surrogate> ::= <D> <high_second> <HEXDIG> <HEXDIG>
<high_second> ::= "8" | "9" | "A" | "B" | "a" | "b"
# §2.3.1.1 low-surrogate = "D" ("C"/"D"/"E"/"F") 2HEXDIG
<low_surrogate> ::= <D> <low_second> <HEXDIG> <HEXDIG>
<low_second> ::= "C" | "D" | "E" | "F" | "c" | "d" | "e" | "f"
# RFC 5234 HEXDIG (RFC 9535 §2.3.1.1 notes HEXDIG is case-insensitive)
<HEXDIG> ::= <DIGIT> | "A" | "B" | "C" | "D" | "E" | "F" | "a" | "b" | "c" | "d" | "e" | "f"

# §2.3.2.1 wildcard-selector = "*"
<wildcard_selector> ::= "*"

# §2.3.3.1 index-selector = int
<index_selector> ::= <int>
# §2.3.3.1 int = "0" / (["-"] DIGIT1 *DIGIT)   (<=15 digits: class 2, RFC 9535 §2.1 I-JSON range)
<int> ::= "0" | <pos_int> | "-" <pos_int>
# short/long split (class 1)
<pos_int> ::= <DIGIT1> | <DIGIT1> <DIGIT> | <DIGIT1> <DIGIT>{2,14}
# §2.3.3.1 DIGIT1 = %x31-39 ; RFC 5234 DIGIT
<DIGIT1> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<DIGIT> ::= "0" | <DIGIT1>

# §2.3.4.1 slice-selector = [start S] ":" S [end S] [":" [S step ]]
# (optional blanks written out as alternatives; parser note in the header)
<slice_selector> ::= <start_opt> ":" <end_opt> <step_opt>
<start_opt> ::= "" | <int> | <int> <B>+
<end_opt> ::= "" | <B>+ | <int> | <B>+ <int> | <int> <B>+ | <B>+ <int> <B>+
<step_opt> ::= "" | ":" | ":" <int> | ":" <B>+ <int>

# §2.3.5.1 filter-selector = "?" S logical-expr
<filter_selector> ::= "?" <logical_expr> | "?" <B>+ <logical_expr>
# §2.3.5.1 logical-expr = logical-or-expr
<logical_expr> ::= <logical_or_expr>
# §2.3.5.1 logical-or-expr = logical-and-expr *(S "||" S logical-and-expr)
<logical_or_expr> ::= <logical_and_expr> | <logical_and_expr> <or_tail>+
<or_tail> ::= <or_op> <logical_and_expr>
# S "||" S with the optional blanks written out (no nullable item; see the note at jsonpath_query)
<or_op> ::= "||" | <B>+ "||" | "||" <B>+ | <B>+ "||" <B>+
# §2.3.5.1 logical-and-expr = basic-expr *(S "&&" S basic-expr)
<logical_and_expr> ::= <basic_expr> | <basic_expr> <and_tail>+
<and_tail> ::= <and_op> <basic_expr>
<and_op> ::= "&&" | <B>+ "&&" | "&&" <B>+ | <B>+ "&&" <B>+
# §2.3.5.1 basic-expr = paren-expr / comparison-expr / test-expr
<basic_expr> ::= <paren_expr> | <comparison_expr> | <test_expr>
# §2.3.5.1 paren-expr = [logical-not-op S] "(" S logical-expr S ")"
# ([logical-not-op S] written out as two alternatives: Fandango's parser fails on the
# nullable-prefix form, which would make the framework drop valid seeds)
<paren_expr> ::= <paren_body> | <logical_not_op> <S> <paren_body>
<paren_body> ::= "(" <logical_expr> ")" | "(" <B>+ <logical_expr> ")" | "(" <logical_expr> <B>+ ")" | "(" <B>+ <logical_expr> <B>+ ")"
# §2.3.5.1 logical-not-op = "!"
<logical_not_op> ::= "!"
# §2.3.5.1 test-expr = [logical-not-op S] (filter-query / function-expr)
# (function-expr restricted to LogicalType results, §2.4.3)
<test_expr> ::= <filter_query> | <logical_not_op> <S> <filter_query> | <logical_function_expr> | <logical_not_op> <S> <logical_function_expr>
# §2.3.5.1 filter-query = rel-query / jsonpath-query
<filter_query> ::= <rel_query> | <abs_query>
# the same jsonpath-query production, as a copy with the split below (class 1)
<abs_query> ::= "$" | "$" <s_segment> | "$" <s_segment> <s_segment> | "$" <s_segment> <s_segment> <s_segment>{24,28}
# §2.3.5.1 rel-query = current-node-identifier segments ; current-node-identifier = "@"
<rel_query> ::= "@" | "@" <s_segment> | "@" <s_segment> <s_segment> | "@" <s_segment> <s_segment> <s_segment>{24,28}
# §2.3.5.1 comparison-expr = comparable S comparison-op S comparable
<comparison_expr> ::= <comparable> <comparison_op_s> <comparable>
<comparison_op_s> ::= <comparison_op> | <B>+ <comparison_op> | <comparison_op> <B>+ | <B>+ <comparison_op> <B>+
# §2.3.5.1 literal = number / string-literal / true / false / null
<literal> ::= <number> | <string_literal> | "true" | "false" | "null"
# §2.3.5.1 comparable = literal / singular-query / function-expr  (ValueType functions, §2.4.3)
<comparable> ::= <literal> | <singular_query> | <value_function_expr>
# §2.3.5.1 comparison-op = "==" / "!=" / "<=" / ">=" / "<" / ">"
<comparison_op> ::= "==" | "!=" | "<=" | ">=" | "<" | ">"
# §2.3.5.1 singular-query = rel-singular-query / abs-singular-query
<singular_query> ::= <rel_singular_query> | <abs_singular_query>
# §2.3.5.1 rel-singular-query = current-node-identifier singular-query-segments
<rel_singular_query> ::= "@" | "@" <s_singular_segment> | "@" <s_singular_segment> <s_singular_segment> | "@" <s_singular_segment> <s_singular_segment> <s_singular_segment>+
# §2.3.5.1 abs-singular-query = root-identifier singular-query-segments
<abs_singular_query> ::= "$" | "$" <s_singular_segment> | "$" <s_singular_segment> <s_singular_segment> | "$" <s_singular_segment> <s_singular_segment> <s_singular_segment>+
# §2.3.5.1 singular-query-segments = *(S (name-segment / index-segment))
<s_singular_segment> ::= <singular_segment> | <B>+ <singular_segment>
<singular_segment> ::= <name_segment> | <index_segment>
# §2.3.5.1 name-segment = ("[" name-selector "]") / ("." member-name-shorthand)
<name_segment> ::= "[" <name_selector> "]" | "." <member_name_shorthand>
# §2.3.5.1 index-segment = "[" index-selector "]"
<index_segment> ::= "[" <index_selector> "]"
# §2.3.5.1 number = (int / "-0") [ frac ] [ exp ]
<number> ::= <num_int> | <num_int> <frac> | <num_int> <exp> | <num_int> <frac> <exp>
<num_int> ::= <int> | "-0"
# §2.3.5.1 frac = "." 1*DIGIT
<frac> ::= "." <DIGIT>+
# §2.3.5.1 exp = "e" [ "-" / "+" ] 1*DIGIT
<exp> ::= <exp_e> <sign_opt> <DIGIT>+
# ABNF quoted strings are case-insensitive (RFC 5234 §2.3), so "e" is e or E
<exp_e> ::= "e" | "E"
<sign_opt> ::= "" | "-" | "+"

# ---- §2.4 function extensions ------------------------------------------------
# §2.4 function-expr = function-name "(" S [function-argument *(S "," S function-argument)] S ")"
# Split by result type (§2.4.1, §2.4.3); names are the five §2.4.4-2.4.8 functions.
<value_function_expr> ::= <length_expr> | <count_expr> | <value_expr>
<logical_function_expr> ::= <match_expr> | <search_expr>
# §2.4.4 length(ValueType) -> ValueType
<length_expr> ::= "length(" <S> <value_argument> <S> ")"
# §2.4.5 count(NodesType) -> ValueType
<count_expr> ::= "count(" <S> <filter_query> <S> ")"
# §2.4.6 match(ValueType, ValueType) -> LogicalType
<match_expr> ::= "match(" <S> <value_argument> <S> "," <S> <regex_argument> <S> ")"
# §2.4.7 search(ValueType, ValueType) -> LogicalType
<search_expr> ::= "search(" <S> <value_argument> <S> "," <S> <regex_argument> <S> ")"
# §2.4.8 value(NodesType) -> ValueType
<value_expr> ::= "value(" <S> <filter_query> <S> ")"
# §2.4.2-2.4.3 a ValueType argument: literal, singular query, or ValueType function
<value_argument> ::= <literal> | <singular_query> | <value_function_expr>
# §2.4.6-2.4.7 the pattern argument: an I-Regexp string literal, or any ValueType
<regex_argument> ::= <iregexp_literal> | <number> | "true" | "false" | "null" | <singular_query> | <value_function_expr>
<iregexp_literal> ::= "'" <ire_regexp> "'" | "\"" <ire_regexp> "\""

# RFC 9485 §5 I-Regexp (the pattern language of §2.4.6-2.4.7), vocabulary class 3.
# i-regexp = branch *( "|" branch )
<ire_regexp> ::= <ire_branch> | <ire_branch> <ire_alt>+
<ire_alt> ::= "|" <ire_branch>
# branch = *piece
<ire_branch> ::= "" | <ire_piece>+
# piece = atom [ quantifier ]
<ire_piece> ::= <ire_atom> | <ire_atom> <ire_quantifier>
# quantifier = ( "*" / "+" / "?" ) / range-quantifier
<ire_quantifier> ::= "*" | "+" | "?" | <ire_range_quantifier>
# range-quantifier = "{" QuantExact [ "," [ QuantExact ] ] "}"  (fixed list, n<=m)
<ire_range_quantifier> ::= "{" <DIGIT> "}" | "{" <DIGIT> ",}" | "{0,1}" | "{0,2}" | "{1,2}" | "{1,3}" | "{2,4}"
# atom = NormalChar / charClass / ( "(" i-regexp ")" )
<ire_atom> ::= "a" | "b" | "c" | "d" | "x" | "y" | "z" | <ire_char_class> | "(" <ire_regexp> ")"
# NormalChar (vocabulary class 3)
<ire_normal_char> ::= <name_char> | <letter>
# charClass = "." / SingleCharEsc / charClassEsc / charClassExpr  (escapes omitted, class 3)
<ire_char_class> ::= "." | <ire_char_class_expr>
# charClassExpr = "[" [ "^" ] ( "-" / CCE1 ) *CCE1 [ "-" ] "]"
<ire_char_class_expr> ::= "[" <ire_caret_opt> <ire_cce1>+ "]"
<ire_caret_opt> ::= "" | "^"
# CCE1 = ( CCchar [ "-" CCchar ] ) / charClassEsc
<ire_cce1> ::= <ire_normal_char> | "a-d" | "x-z"

# ---- §2.5 segments -------------------------------------------------------------
# §2.5 segment = child-segment / descendant-segment
<segment> ::= <child_segment> | <descendant_segment>
# §2.5.1.1 child-segment = bracketed-selection / ("." (wildcard-selector / member-name-shorthand))
<child_segment> ::= <bracketed_selection> | "." <wildcard_selector> | "." <member_name_shorthand>
# §2.5.1.1 bracketed-selection = "[" S selector *(S "," S selector) S "]"
<bracketed_selection> ::= "[" <selection_list> "]" | "[" <B>+ <selection_list> "]" | "[" <selection_list> <B>+ "]" | "[" <B>+ <selection_list> <B>+ "]"
<selection_list> ::= <selector> | <selector> <more_selector>+
<more_selector> ::= <comma_s> <selector>
<comma_s> ::= "," | <B>+ "," | "," <B>+ | <B>+ "," <B>+
# §2.5.1.1 member-name-shorthand = name-first *name-char  (vocabulary class 3; split class 1)
<member_name_shorthand> ::= <name_first> | <name_first> <name_char> | <name_first> <name_char> <name_char>+
# §2.5.1.1 name-first = ALPHA / "_" / %x80-D7FF / %xE000-10FFFF   (class 3: a-d)
<name_first> ::= "a" | "b" | "c" | "d"
# §2.5.1.1 name-char = name-first / DIGIT   (class 3: a-d)
<name_char> ::= <name_first>
# §2.5.2.1 descendant-segment = ".." (bracketed-selection / wildcard-selector / member-name-shorthand)
<descendant_segment> ::= ".." <bracketed_selection> | ".." <wildcard_selector> | ".." <member_name_shorthand>

# Letters of comparison strings and document strings (class 3)
<letter> ::= "x" | "y" | "z"

# ---- Document: RFC 8259 under I-JSON (RFC 7493) ---------------------------------
# RFC 8259 §2 JSON-text = ws value ws. RFC 9535 §2.1 allows any I-JSON value as
# the root; here it is a non-empty object or array (deviations table).
<doc> ::= <ws> <doc_root> <ws>
<doc_root> ::= <nonempty_object> | <nonempty_array>
# RFC 8259 §2 ws = *( %x20 / %x09 / %x0A / %x0D )  (class 1 split)
<ws> ::= "" | <B>+
# RFC 8259 §3 value = false / null / true / object / array / number / string
<value> ::= "false" | "null" | "true" | <object> | <array> | <doc_number> | <doc_string>
# RFC 8259 §4 object = begin-object [ member *( value-separator member ) ] end-object
<object> ::= "{" <ws> "}" | <nonempty_object>
<nonempty_object> ::= "{" <ws> <member> <more_member>* <ws> "}"
<more_member> ::= <ws> "," <ws> <member>
# RFC 8259 §4 member = string name-separator value  (names unique: I-JSON §2.3, `where` below)
<member> ::= <member_name> <ws> ":" <ws> <value>
<member_name> ::= "\"" <doc_name_chars> "\""
<doc_name_chars> ::= <name_char> | <name_char> <name_char> | <name_char> <name_char> <name_char> | <name_char> <name_char> <name_char> <name_char>+ | <doc_name_mixed>
<doc_name_mixed> ::= <name_char>* <doc_name_special> <doc_name_char>*
<doc_name_char> ::= <name_char> | <doc_name_special>
<doc_name_special> ::= <doc_escape>
# RFC 8259 §5 array = begin-array [ value *( value-separator value ) ] end-array
<array> ::= "[" <ws> "]" | <nonempty_array>
<nonempty_array> ::= "[" <ws> <value> <more_value>* <ws> "]"
<more_value> ::= <ws> "," <ws> <value>
# RFC 8259 §6 number = [ minus ] int [ frac ] [ exp ]
<doc_number> ::= <doc_num_int> | <doc_num_int> <frac> | <doc_num_int> <doc_exp> | <doc_num_int> <frac> <doc_exp>
<doc_num_int> ::= <doc_int> | "-" <doc_int>
# RFC 8259 §6 int = zero / ( digit1-9 *DIGIT )   (<=15 digits: I-JSON §2.2)
<doc_int> ::= "0" | <pos_int>
# RFC 8259 §6 exp = e [ minus / plus ] 1*DIGIT   (1-2 digits: I-JSON §2.2 magnitude)
<doc_exp> ::= <doc_e> <sign_opt> <DIGIT> | <doc_e> <sign_opt> <DIGIT> <DIGIT>
<doc_e> ::= "e" | "E"
# RFC 8259 §7 string = quotation-mark *char quotation-mark
<doc_string> ::= "\"" <doc_chars> "\""
<doc_chars> ::= "" | <letter> | <letter> <letter> | <letter> <letter> <letter>+ | <doc_mixed>
<doc_mixed> ::= <letter>* <doc_special> <doc_char>*
<doc_char> ::= <letter> | <doc_special>
<doc_special> ::= <doc_escape>
# RFC 8259 §7 escape: \" \\ \/ \b \f \n \r \t \uXXXX  (no lone surrogates: I-JSON §2.1)
<doc_escape> ::= "\\\"" | "\\\\" | "\\/" | "\\b" | "\\f" | "\\n" | "\\r" | "\\t" | "\\u" <hexchar>

# I-JSON §2.3: member names unique within each object.
where unique_member_names(<start>)


