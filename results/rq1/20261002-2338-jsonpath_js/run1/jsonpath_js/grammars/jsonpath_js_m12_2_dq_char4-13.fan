# JSONPath query plus JSON document, for five JavaScript implementations.
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
# rule by rule. Each rule carries its section, and nonterminal names follow the
# ABNF names with "-" written as "_". The document side transcribes RFC 8259
# under the I-JSON profile (RFC 7493), which RFC 9535 §2.1 requires of the
# query argument. Everything that can grow is `*`, `+` or recursion; the only
# finite bounds are I-JSON's (table below).
#
# Function well-typedness (RFC 9535 §2.4.3) is encoded by construction: a
# comparable takes only the ValueType functions (length, count, value), a
# test-expr only the LogicalType ones (match, search), length/match/search take
# ValueType arguments (literal, singular query or a ValueType function), and
# count/value take a filter-query. An ill-typed expression is not a valid query
# (§2.4.3), so this is the RFC's language rather than a narrowing.
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
# | *_chars, member_name_shorthand,| split into length alternatives (0/1/2/3+ chars, or     | 1 |
# | pos_int                        | 1/2/3+ digits) plus a "contains an escape" alternative |   |
# | rel_query, abs_query,          | trailing `*` written as 1/2/3+ alternatives, so a bare | 1 |
# | *_singular_query, or/and tails | `@` is a quarter of relative queries and the parser    |   |
# |                                | accepts the grammar's own output (see jsonpath_query)  |   |
# | or_op, and_op, filter_selector,| optional blanks written as alternatives, not a         | 1 |
# | comparison_op_s, paren_body    | nullable <S> (same reason)                             |   |
# | int, doc_int                   | at most 15 digits, so below 2^53 (16-digit values up to|
# |                                | 2^53-1 are left out: conservative)                     | 2: RFC 9535 §2.1 / RFC 7493 §2.2 |
# | doc_exp                        | exponent 1-2 digits (magnitude within a double)        | 2: RFC 7493 §2.2 |
# | doc_escape (hexchar)           | \u escapes are non-surrogates or surrogate pairs       | 2: RFC 7493 §2.1 |
# | where unique_member_names      | member names unique within an object                   | 2: RFC 7493 §2.3 |
# | segments (S before a segment)  | no blank space between segments                        | 4: jsonpath 100%, jsonpathly 100% |
# | bracketed_selection, slice     | no blank space inside brackets or slices               | 4: jsonpath 100% (slice: jsonpathly 100%) |
# | bracketed_selection            | a list of 2+ selectors holds only names and indices    | 4: wildcard member jsonpath 100%; slice member jsonpathly 100%; filter member both 100% |
# | filter_selector                | always "?(" logical-expr ")": no bare `?@.a`, no blank | 4: jsonpath 100% on each |
# |                                | after "?", no "?!(...)"                                |   |
# | doc_root                       | root is an object or array                             | 4: jsonpath asserts on every scalar root (6/6 kinds) |
# | doc_root                       | root is non-empty: `{}`/`[]` excluded                  | none: see below |
#
# The empty roots are a restriction that fits no class. An empty root makes
# every query select at most `$`, so those inputs carry no signal, and there is
# no class-1 way to keep them rare: Fandango picks alternatives evenly, so
# rarity needs duplicated alternatives, which makes the grammar ambiguous, and
# Fandango's parser is exponential on ambiguous grammars (19 s to parse
# `{"a":[1,2]}` with duplicated blank-space alternatives, measured 2026-09-30).
#
# Not enforced: I-JSON §2.2's SHOULD on precision (a long fraction can carry more
# digits than a double keeps).
#
# Class-4 probe (2026-09-30, 50 inputs per construct; full table in the A2
# overnight evaluation report). Partial rejections stay in the grammar, because the
# harness filters disagreeing inputs per engine pair at scoring time: function
# extensions (jsonpath 24-58%, jsonpath-plus 0-34%; both Goessner engines
# evaluate filters as JavaScript and mostly return no match rather than an
# error), absolute queries in filters (jsonpath 50%), tab/newline around
# operators (jsonpath 88%, jsonpath-plus 32%), `[::0]` (jsonpath 40%).
# json-p3 rejects every number literal with integer part 0 and a fraction or
# exponent (`0.5`, `0e1`; 100%) although RFC 9535 allows them: that is a json-p3
# bug, not a dialect gap, so those literals stay in.
#
# Parser note. Fandango's parser rejects valid input in two situations, and the
# framework drops any seed its parser rejects: (a) several nullable items
# completing at one position (`$[?(1==1||@..*)]` with starred rel-query
# segments and and/or tails); (b) ambiguous nullable rules (exponential time).
# The grammar avoids both; 100 of 100 generated inputs parse back.

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
# §2.1.1 segments = *(S segment)   (S dropped here: class 4, see table)
# (parse-safe forms inside filters: see "Parser note" in the header)
<jsonpath_query> ::= "$" <segment>*
# §2.1.1 B = %x20 / %x09 / %x0A / %x0D ; S = *B
<B> ::= " " | "\t" | "\n" | "\r"
<S> ::= "" | <B>+

# ---- §2.3 selectors -------------------------------------------------------
# §2.3 selector = name-selector / wildcard-selector / slice-selector / index-selector / filter-selector
<selector> ::= <filter_selector>

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
<string_literal> ::= "\"" <dq_chars> "\""
<dq_chars> ::= <dq_mixed>
<dq_mixed> ::= <letter>* <dq_special> <dq_char>{4,13}
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
# (S dropped inside the slice: class 4, see table)
<slice_selector> ::= <start_opt> ":" <end_opt> <step_opt>
<start_opt> ::= "" | <int>
<end_opt> ::= "" | <int>
<step_opt> ::= "" | ":" | ":" <int>

# §2.3.5.1 filter-selector = "?" S logical-expr
# (class 4: the logical-expr is always a parenthesised one, as "?(" S logical-expr S ")",
# with no S after "?" and no "!" before "(": jsonpath rejects the rest, see table)
# (the optional S on each side is written out as alternatives: Fandango's parser
# rejects "?(" <S> <logical_expr> when S is empty and the expression is a test)
<filter_selector> ::= "?(" <logical_expr> ")" | "?(" <B>+ <logical_expr> ")" | "?(" <logical_expr> <B>+ ")" | "?(" <B>+ <logical_expr> <B>+ ")"
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
<basic_expr> ::= <comparison_expr>
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
<abs_query> ::= "$" | "$" <segment> | "$" <segment> <segment> | "$" <segment> <segment> <segment>+
# §2.3.5.1 rel-query = current-node-identifier segments ; current-node-identifier = "@"
<rel_query> ::= "@" | "@" <segment> | "@" <segment> <segment> | "@" <segment> <segment> <segment>+
# §2.3.5.1 comparison-expr = comparable S comparison-op S comparable
<comparison_expr> ::= <comparable> <comparison_op_s> <comparable>
<comparison_op_s> ::= <comparison_op> | <B>+ <comparison_op> | <comparison_op> <B>+ | <B>+ <comparison_op> <B>+
# §2.3.5.1 literal = number / string-literal / true / false / null
<literal> ::= <string_literal>
# §2.3.5.1 comparable = literal / singular-query / function-expr  (ValueType functions, §2.4.3)
<comparable> ::= <literal>
# §2.3.5.1 comparison-op = "==" / "!=" / "<=" / ">=" / "<" / ">"
<comparison_op> ::= "==" | "!=" | "<=" | ">=" | "<" | ">"
# §2.3.5.1 singular-query = rel-singular-query / abs-singular-query
<singular_query> ::= <rel_singular_query> | <abs_singular_query>
# §2.3.5.1 rel-singular-query = current-node-identifier singular-query-segments
<rel_singular_query> ::= "@" | "@" <singular_segment> | "@" <singular_segment> <singular_segment> | "@" <singular_segment> <singular_segment> <singular_segment>+
# §2.3.5.1 abs-singular-query = root-identifier singular-query-segments
<abs_singular_query> ::= "$" | "$" <singular_segment> | "$" <singular_segment> <singular_segment> | "$" <singular_segment> <singular_segment> <singular_segment>+
# §2.3.5.1 singular-query-segments = *(S (name-segment / index-segment))   (no S: class 4)
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
<segment> ::= <child_segment>
# §2.5.1.1 child-segment = bracketed-selection / ("." (wildcard-selector / member-name-shorthand))
<child_segment> ::= <bracketed_selection>
# §2.5.1.1 bracketed-selection = "[" S selector *(S "," S selector) S "]"
# (class 4: no S inside brackets; a list of two or more selectors holds only
# name and index selectors, since jsonpath rejects wildcard and filter members
# and jsonpathly rejects slice and filter members; see table)
<bracketed_selection> ::= "[" <selector> "]"
<more_selector> ::= "," <union_selector>
<union_selector> ::= <name_selector> | <index_selector>
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
# the root. Here the root is a non-empty object or array: scalar roots are
# class 4 (jsonpath asserts "obj needs to be an object" on every one), and the
# two empty roots are left out by design, see the deviations table.
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
