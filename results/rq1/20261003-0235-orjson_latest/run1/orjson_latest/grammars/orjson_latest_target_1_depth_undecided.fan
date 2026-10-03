from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_ws(tree):
    return _coreografa_count(tree, _CoreoNT('<ws>'))

def count_wschar(tree):
    return _coreografa_count(tree, _CoreoNT('<wschar>'))

def count_root_scalar(tree):
    return _coreografa_count(tree, _CoreoNT('<root_scalar>'))

def count_number(tree):
    return _coreografa_count(tree, _CoreoNT('<number>'))

def count_float_number(tree):
    return _coreografa_count(tree, _CoreoNT('<float_number>'))

def count_int_sig(tree):
    return _coreografa_count(tree, _CoreoNT('<int_sig>'))

def count_DIGIT(tree):
    return _coreografa_count(tree, _CoreoNT('<DIGIT>'))

def count_digit1_9(tree):
    return _coreografa_count(tree, _CoreoNT('<digit1_9>'))

def count_zero(tree):
    return _coreografa_count(tree, _CoreoNT('<zero>'))

def count_int_frac(tree):
    return _coreografa_count(tree, _CoreoNT('<int_frac>'))

def count_exp_opt(tree):
    return _coreografa_count(tree, _CoreoNT('<exp_opt>'))

def count_exp(tree):
    return _coreografa_count(tree, _CoreoNT('<exp>'))

def count_minus(tree):
    return _coreografa_count(tree, _CoreoNT('<minus>'))

def count_exp_zeros(tree):
    return _coreografa_count(tree, _CoreoNT('<exp_zeros>'))

def count_minus_opt(tree):
    return _coreografa_count(tree, _CoreoNT('<minus_opt>'))

def count_integer_number(tree):
    return _coreografa_count(tree, _CoreoNT('<integer_number>'))

def count_int_upto15(tree):
    return _coreografa_count(tree, _CoreoNT('<int_upto15>'))

def count_int_16(tree):
    return _coreografa_count(tree, _CoreoNT('<int_16>'))

def count_false(tree):
    return _coreografa_count(tree, _CoreoNT('<false>'))

def count_null(tree):
    return _coreografa_count(tree, _CoreoNT('<null>'))

def count_true(tree):
    return _coreografa_count(tree, _CoreoNT('<true>'))

def count_string(tree):
    return _coreografa_count(tree, _CoreoNT('<string>'))

def count_char(tree):
    return _coreografa_count(tree, _CoreoNT('<char>'))

def count_char_2(tree):
    return _coreografa_count(tree, _CoreoNT('<char_2>'))

def count_char_3(tree):
    return _coreografa_count(tree, _CoreoNT('<char_3>'))

def count_unescaped_nonascii(tree):
    return _coreografa_count(tree, _CoreoNT('<unescaped_nonascii>'))

def count_unescaped_utf8_3(tree):
    return _coreografa_count(tree, _CoreoNT('<unescaped_utf8_3>'))

def count_unescaped_utf8_2(tree):
    return _coreografa_count(tree, _CoreoNT('<unescaped_utf8_2>'))

def count_unescaped_utf8_4(tree):
    return _coreografa_count(tree, _CoreoNT('<unescaped_utf8_4>'))

def count_escaped(tree):
    return _coreografa_count(tree, _CoreoNT('<escaped>'))

def count_u_escape(tree):
    return _coreografa_count(tree, _CoreoNT('<u_escape>'))

def count_hex_low_surrogate_fffe(tree):
    return _coreografa_count(tree, _CoreoNT('<hex_low_surrogate_fffe>'))

def count_hex_bmp(tree):
    return _coreografa_count(tree, _CoreoNT('<hex_bmp>'))

def count_hex_high_surrogate(tree):
    return _coreografa_count(tree, _CoreoNT('<hex_high_surrogate>'))

def count_hex_high_surrogate_not3f(tree):
    return _coreografa_count(tree, _CoreoNT('<hex_high_surrogate_not3f>'))

def count_hex_low_surrogate(tree):
    return _coreografa_count(tree, _CoreoNT('<hex_low_surrogate>'))

def count_unescaped_ascii_other(tree):
    return _coreografa_count(tree, _CoreoNT('<unescaped_ascii_other>'))

def count_unescaped_alnum(tree):
    return _coreografa_count(tree, _CoreoNT('<unescaped_alnum>'))

def count_object(tree):
    return _coreografa_count(tree, _CoreoNT('<object>'))

def count_end_object(tree):
    return _coreografa_count(tree, _CoreoNT('<end_object>'))

def count_more_member(tree):
    return _coreografa_count(tree, _CoreoNT('<more_member>'))

def count_value_separator(tree):
    return _coreografa_count(tree, _CoreoNT('<value_separator>'))

def count_member(tree):
    return _coreografa_count(tree, _CoreoNT('<member>'))

def count_value(tree):
    return _coreografa_count(tree, _CoreoNT('<value>'))

def count_array(tree):
    return _coreografa_count(tree, _CoreoNT('<array>'))

def count_begin_object(tree):
    return _coreografa_count(tree, _CoreoNT('<begin_object>'))

def count_end_array(tree):
    return _coreografa_count(tree, _CoreoNT('<end_array>'))

def count_more_value(tree):
    return _coreografa_count(tree, _CoreoNT('<more_value>'))

def count_begin_array(tree):
    return _coreografa_count(tree, _CoreoNT('<begin_array>'))

"""Structural properties of a generated JSON tree — the axes targeting reasons
over. All but depth follow the generic "count occurrences of nonterminal X"
pattern.
"""
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

PROPERTIES = ["depth", "num_pairs", "num_arrays", "num_numbers", "total_string_len"]

# Declared properties that are exactly a grammar-derived non-terminal count
# (verified equal on 30 sampled corpus inputs, 2026-09-11). The alias
# suppresses the derived duplicate so the subject keeps its own column and
# its accumulated history, rather than gaining a second axis measuring the
# same thing. The declared implementation is the one that runs.
ALIASES = {
    "num_pairs": "count_member",
    "num_arrays": "count_array",
    "num_numbers": "count_number",
    "total_string_len": "count_char",
}



def _count(tree: DerivationTree, symbol_name: str) -> int:
    """Number of nodes whose symbol is `symbol_name` in the tree."""
    target = NonTerminal(symbol_name)
    count = 1 if tree.symbol == target else 0
    for child in tree.children:
        count += _count(child, symbol_name)
    return count


_CONTAINERS = (NonTerminal("<object>"), NonTerminal("<array>"))


def depth(tree: DerivationTree) -> int:
    """JSON nesting depth: the most <object>/<array> nodes on any root-to-leaf
    path (0 for a scalar document) -- the axis where recursion limits diverge
    across engines.

    Until 2026-09-30 this was the raw derivation-tree depth. The RFC 8259
    grammar writes `ws` and `*char` as recursion, so derivation depth would
    now mostly measure whitespace runs and string length rather than nesting.
    """
    here = 1 if tree.symbol in _CONTAINERS else 0
    if not tree.children:
        return here
    return here + max(depth(child) for child in tree.children)


def num_pairs(tree: DerivationTree) -> int:
    """Total key/value pairs across all objects (document breadth+depth)."""
    return _count(tree, "<member>")


def num_arrays(tree: DerivationTree) -> int:
    return _count(tree, "<array>")


def num_numbers(tree: DerivationTree) -> int:
    return _count(tree, "<number>")


def total_string_len(tree: DerivationTree) -> int:
    """Total string payload = number of <char> nodes across all strings."""
    return _count(tree, "<char>")

# JSON input language: RFC 8259 sections 2-7, transcribed rule by rule from
# its ABNF, restricted to the I-JSON profile (RFC 7493).
#
# Structural-only grammar (Strategy C): generation does NOT run the SUT.
# Metrics are measured once-to-significance on kept inputs by the harness.
# Sizes are unbounded (`*` / recursion). Generation size is set by
# max_repetition / max_nodes and the stratify bands in example.py.
#
# Deviations from RFC 8259 (class: 1 = language-preserving rewrite, sampling
# distribution only; 2 = restriction to a named profile, I-JSON; 3 = finite
# lexical vocabulary; 4 = construct an engine does not implement):
#
# | # | Deviation                                              | Class | Source          |
# |---|--------------------------------------------------------|-------|-----------------|
# | 1 | Leading/trailing `ws` of the six structural characters  | 1     | RFC 8259 §2     |
# |   | merged so each gap holds one `ws` (ws ws = ws); empty   |       |                 |
# |   | object/array written as "{" ws "}" / "[" ws "]"         |       |                 |
# | 2 | `ws` written as right recursion ("" | wschar ws), so     | 1     | RFC 8259 §2     |
# |   | runs are short (geometric) instead of uniform in length |       |                 |
# | 3 | `*char` split into short (0-8) and long (9+) branches   | 1     | RFC 8259 §7     |
# | 4 | `char` split into nested alternative groups (ASCII      | 1     | RFC 8259 §7     |
# |   | alnum, other ASCII, non-ASCII by UTF-8 length, escape)  |       |                 |
# |   | so ASCII dominates the sample; same set of characters   |       |                 |
# | 5 | `number` split into integer form (no frac, no exp) and  | 1     | RFC 8259 §6     |
# |   | non-integer form, so each can carry its own bound       |       |                 |
# | 6 | Unescaped chars exclude surrogates D800-DFFF and        | 2     | RFC 7493 §2.1   |
# |   | noncharacters (FDD0-FDEF, U+xFFFE/U+xFFFF)              |       |                 |
# | 7 | \uXXXX never encodes a lone surrogate or a              | 2     | RFC 7493 §2.1   |
# |   | noncharacter; surrogates only as a valid hi+lo pair     |       |                 |
# | 8 | Integer-form numbers within [-(2^53)+1, 2^53-1]         | 2     | RFC 7493 §2.2   |
# | 9 | Non-integer numbers: at most 17 significant digits in   | 2     | RFC 7493 §2.2   |
# |   | int+frac, and exponent value <= 290 (leading zeros      |       |                 |
# |   | allowed). Conservative reading of "no greater magnitude |       |                 |
# |   | or precision than an IEEE 754 double": sufficient, not  |       |                 |
# |   | necessary, so it also excludes e.g. 1e300, 1e-300 and   |       |                 |
# |   | -0.000...0001 with 78 zeros (JSONTestSuite              |       |                 |
# |   | y_number_double_close_to_zero), because leading zeros   |       |                 |
# |   | of frac count towards the 17 digits                     |       |                 |
# | 10| Duplicate member names forbidden (compared after        | 2     | RFC 7493 §2.3   |
# |   | unescaping) via the `where` constraint at the bottom    |       |                 |
# | 11| Root `value` regrouped as object | array | scalar so   | 1     | RFC 8259 §2-3   |
# |   | most roots are containers (same set of values)          |       |                 |
# | 12| 3- and 4-byte codepoint classes split into one regex    | 1     | RFC 8259 §7     |
# |   | per 4096-block / per plane. Same set; exrex expands a   |       |                 |
# |   | class into a list per draw, so one 1M-codepoint class   |       |                 |
# |   | made generation ~2x slower                              |       |                 |
#
# No class-3 or class-4 deviation: the full codepoint range is expressed with
# regex character classes, and every construct is accepted by all four engines.
#
# Measured 2026-09-30 (probe scripts outside the repo):
# - soundness: 500/500 generated inputs pass CPython json.loads (strict, dup
#   names rejected via object_pairs_hook, NaN/Infinity rejected), have no lone
#   surrogate or noncharacter, integers within 2^53-1, floats finite and not
#   underflowing; 300/300 more at max_nodes=4000, max_repetition=200.
# - JSONTestSuite y_*.json: 84/95 parse and satisfy the constraint. Misses:
#   8 noncharacters (I-JSON §2.1), 2 duplicate names (§2.3), 1 number with
#   78 leading frac zeros (deviation 9).
# - orjson, ujson, json, simplejson return equal values on 200/200 inputs.
# - 100 inputs take ~1.6-2.1 s to generate (old grammar ~2.5-4.6 s); the
#   duplicate-name constraint costs nothing measurable (dup names occur in
#   ~1% of unconstrained outputs, so rejection is rare).

# RFC 8259 §2 JSON-text = ws value ws; value regrouped at the root only (deviation 11)
<start> ::= <ws> <root_value> <ws>
# RFC 8259 §3 value, regrouped so a root is a container 2/3 of the time (deviation 11)
<root_value> ::= <object> | <array> | <root_scalar>
# RFC 8259 §3 the scalar alternatives of value, at the root (deviation 11)
<root_scalar> ::= <false> | <null> | <true> | <number> | <string>

# RFC 8259 §2 begin-array = ws %x5B ws (leading ws merged, deviation 1)
<begin_array> ::= "[" <ws>
# RFC 8259 §2 begin-object = ws %x7B ws (leading ws merged, deviation 1)
<begin_object> ::= "{" <ws>
# RFC 8259 §2 end-array = ws %x5D ws (trailing ws merged, deviation 1)
<end_array> ::= <ws> "]"
# RFC 8259 §2 end-object = ws %x7D ws (trailing ws merged, deviation 1)
<end_object> ::= <ws> "}"
# RFC 8259 §2 name-separator = ws %x3A ws
<name_separator> ::= <ws> ":" <ws>
# RFC 8259 §2 value-separator = ws %x2C ws
<value_separator> ::= <ws> "," <ws>
# RFC 8259 §2 ws = *( %x20 / %x09 / %x0A / %x0D ), as right recursion (deviation 2)
<ws> ::= "" | <wschar> <ws>
# RFC 8259 §2 ws alternatives: space / horizontal tab / line feed / carriage return
<wschar> ::= " " | "\t" | "\n" | "\r"

# RFC 8259 §3 value = false / null / true / object / array / number / string
<value> ::= <false> | <null> | <true> | <object> | <array> | <number> | <string>
# RFC 8259 §3 false = %x66.61.6c.73.65
<false> ::= "false"
# RFC 8259 §3 null = %x6e.75.6c.6c
<null> ::= "null"
# RFC 8259 §3 true = %x74.72.75.65
<true> ::= "true"

# RFC 8259 §4 object = begin-object [ member *( value-separator member ) ] end-object
<object> ::= "{" <ws> "}" | <begin_object> <member> <more_member>* <end_object>
# RFC 8259 §4 the repeated part: value-separator member
<more_member> ::= <value_separator> <member>
# RFC 8259 §4 member = string name-separator value
<member> ::= <string> <name_separator> <value>

# RFC 8259 §5 array = begin-array [ value *( value-separator value ) ] end-array
<array> ::= "[" <ws> "]" | <begin_array> <value> <more_value>* <end_array>
# RFC 8259 §5 the repeated part: value-separator value
<more_value> ::= <value_separator> <value>

# RFC 8259 §6 number = [ minus ] int [ frac ] [ exp ], split by form (deviation 5)
<number> ::= <integer_number> | <float_number>
# RFC 8259 §6 number without frac/exp; I-JSON §2.2 exact integer range (deviation 8)
<integer_number> ::= <minus_opt> <int>
# RFC 8259 §6 [ minus ]
<minus_opt> ::= "" | <minus>
# RFC 8259 §6 minus = %x2D
<minus> ::= "-"
# RFC 8259 §6 int = zero / ( digit1-9 *DIGIT ), limited to |n| <= 2^53-1 (I-JSON §2.2, deviation 8)
<int> ::= <zero> | <int_upto15> | <int_16>
# RFC 8259 §6 digit1-9 *DIGIT with at most 15 digits (I-JSON §2.2, deviation 8)
<int_upto15> ::= <digit1_9> <DIGIT>{0,14}
# RFC 8259 §6 digit1-9 *DIGIT with exactly 16 digits, <= 9007199254740991 = 2^53-1 (I-JSON §2.2, deviation 8)
<int_16> ::= r"[1-8][0-9]{15}" | r"900[0-6][0-9]{12}" | r"90070[0-9]{11}" | r"90071[0-8][0-9]{10}" | r"900719[0-8][0-9]{9}" | r"9007199[0-1][0-9]{8}" | r"90071992[0-4][0-9]{7}" | r"900719925[0-3][0-9]{6}" | r"9007199254[0-6][0-9]{5}" | r"90071992547[0-3][0-9]{4}" | r"9007199254740[0-8][0-9]{2}" | r"90071992547409[0-8][0-9]{1}" | r"9007199254740990" | "9007199254740991"
# RFC 8259 §6 number with frac and/or exp: [ minus ] int frac [ exp ] / [ minus ] int exp (deviations 5, 9)
<float_number> ::= <minus_opt> <int_frac> <exp_opt> | <minus_opt> <int_sig> <exp>
# RFC 8259 §6 int with at most 17 significant digits (I-JSON §2.2, deviation 9)
<int_sig> ::= <zero> | <digit1_9> <DIGIT>{0,16}
# RFC 8259 §6 int frac = int decimal-point 1*DIGIT, at most 17 digits in total (I-JSON §2.2, deviation 9)
<int_frac> ::= r"[0-9]\.[0-9]{1,16}" | r"[1-9][0-9]{1}\.[0-9]{1,15}" | r"[1-9][0-9]{2}\.[0-9]{1,14}" | r"[1-9][0-9]{3}\.[0-9]{1,13}" | r"[1-9][0-9]{4}\.[0-9]{1,12}" | r"[1-9][0-9]{5}\.[0-9]{1,11}" | r"[1-9][0-9]{6}\.[0-9]{1,10}" | r"[1-9][0-9]{7}\.[0-9]{1,9}" | r"[1-9][0-9]{8}\.[0-9]{1,8}" | r"[1-9][0-9]{9}\.[0-9]{1,7}" | r"[1-9][0-9]{10}\.[0-9]{1,6}" | r"[1-9][0-9]{11}\.[0-9]{1,5}" | r"[1-9][0-9]{12}\.[0-9]{1,4}" | r"[1-9][0-9]{13}\.[0-9]{1,3}" | r"[1-9][0-9]{14}\.[0-9]{1,2}" | r"[1-9][0-9]{15}\.[0-9]{1,1}"
# RFC 8259 §6 [ exp ]
<exp_opt> ::= "" | <exp>
# RFC 8259 §6 exp = e [ minus / plus ] 1*DIGIT, value <= 290 (I-JSON §2.2, deviation 9)
<exp> ::= <e> <exp_sign> <exp_zeros> <exp_digits>
# RFC 8259 §6 e = %x65 / %x45
<e> ::= "e" | "E"
# RFC 8259 §6 [ minus / plus ]; plus = %x2B
<exp_sign> ::= "" | <minus> | "+"
# RFC 8259 §6 leading zeros of 1*DIGIT (right recursion keeps them rare; class-1 rewrite as in deviation 2)
<exp_zeros> ::= "" | "0" <exp_zeros>
# RFC 8259 §6 rest of 1*DIGIT: 0..290 without a leading zero (I-JSON §2.2, deviation 9)
<exp_digits> ::= r"[0-9]" | r"[1-9][0-9]" | r"1[0-9][0-9]" | r"2[0-8][0-9]" | "290"
# RFC 8259 §6 zero = %x30
<zero> ::= "0"
# RFC 8259 §6 digit1-9 = %x31-39
<digit1_9> ::= r"[1-9]"
# RFC 5234 core rule DIGIT = %x30-39 (used by RFC 8259 §6)
<DIGIT> ::= r"[0-9]"

# RFC 8259 §7 string = quotation-mark *char quotation-mark; *char split short/long (deviation 3)
<string> ::= "\"" <chars> "\""
# RFC 8259 §7 *char: 0-8 chars, or 9 and more (deviation 3)
<chars> ::= <char>{0,8} | <char>{9} <char>*
# RFC 8259 §7 char = unescaped / escape (...); grouped so ASCII dominates (deviation 4)
<char> ::= <unescaped_alnum> | <char_2>
# RFC 8259 §7 char, second group (deviation 4)
<char_2> ::= <unescaped_ascii_other> | <char_3>
# RFC 8259 §7 char, third group (deviation 4)
<char_3> ::= <unescaped_nonascii> | <escaped>
# RFC 8259 §7 unescaped, ASCII letters and digits
<unescaped_alnum> ::= r"[0-9A-Za-z]"
# RFC 8259 §7 unescaped = %x20-21 / %x23-5B / %x5D-10FFFF, remaining ASCII (includes DEL %x7F)
<unescaped_ascii_other> ::= r"[\x20\x21\x23-\x2f\x3a-\x40\x5b\x5d-\x60\x7b-\x7f]"
# RFC 8259 §7 unescaped %x80-10FFFF, split by UTF-8 encoded length (deviation 4)
<unescaped_nonascii> ::= <unescaped_utf8_2> | <unescaped_utf8_3> | <unescaped_utf8_4>
# RFC 8259 §7 unescaped %x80-7FF (2-byte UTF-8)
<unescaped_utf8_2> ::= r"[\x80-\u07ff]"
# RFC 8259 §7 unescaped %x800-FFFF (3-byte UTF-8) minus surrogates and noncharacters (I-JSON §2.1, deviation 6), one alternative per 4096-codepoint block (deviation 12)
<unescaped_utf8_3> ::= r"[\u0800-\u0fff]" | r"[\u1000-\u1fff]" | r"[\u2000-\u2fff]" | r"[\u3000-\u3fff]" | r"[\u4000-\u4fff]" | r"[\u5000-\u5fff]" | r"[\u6000-\u6fff]" | r"[\u7000-\u7fff]" | r"[\u8000-\u8fff]" | r"[\u9000-\u9fff]" | r"[\ua000-\uafff]" | r"[\ub000-\ubfff]" | r"[\uc000-\ucfff]" | r"[\ud000-\ud7ff]" | r"[\ue000-\uefff]" | r"[\uf000-\ufdcf\ufdf0-\ufffd]"
# RFC 8259 §7 unescaped %x10000-10FFFF (4-byte UTF-8) minus noncharacters U+xFFFE/U+xFFFF (I-JSON §2.1, deviation 6), one alternative per plane (deviation 12)
<unescaped_utf8_4> ::= r"[\U00010000-\U0001fffd]" | r"[\U00020000-\U0002fffd]" | r"[\U00030000-\U0003fffd]" | r"[\U00040000-\U0004fffd]" | r"[\U00050000-\U0005fffd]" | r"[\U00060000-\U0006fffd]" | r"[\U00070000-\U0007fffd]" | r"[\U00080000-\U0008fffd]" | r"[\U00090000-\U0009fffd]" | r"[\U000a0000-\U000afffd]" | r"[\U000b0000-\U000bfffd]" | r"[\U000c0000-\U000cfffd]" | r"[\U000d0000-\U000dfffd]" | r"[\U000e0000-\U000efffd]" | r"[\U000f0000-\U000ffffd]" | r"[\U00100000-\U0010fffd]"
# RFC 8259 §7 escape = %x5C, followed by one of the escaped forms
<escaped> ::= "\\\"" | "\\\\" | "\\/" | "\\b" | "\\f" | "\\n" | "\\r" | "\\t" | <u_escape>
# RFC 8259 §7 %x75 4HEXDIG; I-JSON §2.1: a surrogate only as a valid pair, no noncharacters (deviation 7)
<u_escape> ::= "\\u" <hex_bmp> | "\\u" <hex_high_surrogate> "\\u" <hex_low_surrogate> | "\\u" <hex_high_surrogate_not3f> "\\u" <hex_low_surrogate_fffe>
# RFC 8259 §7 4HEXDIG (RFC 5234 HEXDIG, case-insensitive) outside D800-DFFF, FDD0-FDEF, FFFE-FFFF (I-JSON §2.1)
<hex_bmp> ::= r"[0-9a-cA-CeE][0-9a-fA-F]{3}" | r"[dD][0-7][0-9a-fA-F]{2}" | r"[fF][0-9a-cA-CeE][0-9a-fA-F]{2}" | r"[fF][dD][0-9a-cA-CfF][0-9a-fA-F]" | r"[fF][fF][0-9a-eA-E][0-9a-fA-F]" | r"[fF][fF][fF][0-9a-dA-D]"
# RFC 8259 §7 4HEXDIG high surrogate D800-DBFF (first half of a UTF-16 pair)
<hex_high_surrogate> ::= r"[dD][89abAB][0-9a-fA-F]{2}"
# RFC 8259 §7 4HEXDIG low surrogate DC00-DFFD (pairs never form a noncharacter)
<hex_low_surrogate> ::= r"[dD][c-eC-E][0-9a-fA-F]{2}" | r"[dD][fF][0-9a-eA-E][0-9a-fA-F]" | r"[dD][fF][fF][0-9a-dA-D]"
# RFC 8259 §7 4HEXDIG high surrogate whose low 6 bits are not 3F, so pairing with DFFE/DFFF avoids U+xFFFE/U+xFFFF (I-JSON §2.1)
<hex_high_surrogate_not3f> ::= r"[dD][89abAB][0-9a-fA-F][0-9a-eA-E]" | r"[dD][89abAB][01245689aAcCdDeE][fF]"
# RFC 8259 §7 4HEXDIG low surrogate DFFE-DFFF
<hex_low_surrogate_fffe> ::= r"[dD][fF][fF][eEfF]"


# I-JSON (RFC 7493) §2.3: "Objects in I-JSON messages MUST NOT have members
# with duplicate names." Names are compared after unescaping, so "a" and
# "\u0061" collide. A CFG cannot express uniqueness, hence this constraint
# (deviation 10). Pure function of the derivation tree.
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

where depth(<start>) >= 9.551598
where depth(<start>) <= 15.0
