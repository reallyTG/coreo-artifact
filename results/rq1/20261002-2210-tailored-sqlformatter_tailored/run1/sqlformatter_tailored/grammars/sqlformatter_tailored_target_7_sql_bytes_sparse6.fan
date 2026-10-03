from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_ws(tree):
    return _coreografa_count(tree, _CoreoNT('<ws>'))

def count_columnref(tree):
    return _coreografa_count(tree, _CoreoNT('<columnref>'))

def count_col_id(tree):
    return _coreografa_count(tree, _CoreoNT('<col_id>'))

def count_ident_char(tree):
    return _coreografa_count(tree, _CoreoNT('<ident_char>'))

def count_elem(tree):
    return _coreografa_count(tree, _CoreoNT('<elem>'))

def count_iconst(tree):
    return _coreografa_count(tree, _CoreoNT('<iconst>'))

def count_digit(tree):
    return _coreografa_count(tree, _CoreoNT('<digit>'))

def count_more_el(tree):
    return _coreografa_count(tree, _CoreoNT('<more_el>'))

def count_ows(tree):
    return _coreografa_count(tree, _CoreoNT('<ows>'))

def count_more_el_bool(tree):
    return _coreografa_count(tree, _CoreoNT('<more_el_bool>'))

"""Input properties for the tailored sql-formatter subject.

`sql_bytes` is the spec subject's size property, kept unchanged. `list_items`
is the axis the tailored grammar is built around: the number of operands in
the statement's one long flat list (the select list in kind 1, the IN list in
kind 2), which is what PR #963's quadratic cost grows with. Occurrence counts
of non-terminals (`count_more_el`, ...) come from core/grammar_props.py.
"""
import re

PROPERTIES = [
    "sql_bytes",
    "list_items",
]

_SEP = re.compile(r"\s*,\s*|\s+(?:OR|AND)\s+")


def sql_bytes(tree):
    return len(str(tree))


def list_items(tree):
    """Operands in the long flat list: the IN list if there is one, else the select list."""
    s = str(tree)
    if "(" in s:
        body = s[s.index("(") + 1:s.rindex(")")]
    else:
        body = s[len("SELECT "):s.index(" FROM ")]
    return len(_SEP.split(body.strip()))

# TAILORED grammar (RQ1 tailored setting), sql-formatter 15.8.2 -> 15.9.0 (commit 6c21ff5, PR #963).
# A sub-language of the frozen spec grammar subjects/sql_js/sql_js.fan, written 2026-10-02.
#
# What the diff says (read from the installed dist/cjs of both versions):
#   parser/grammar.js   every nearley EBNF list of `free_form_sql` items, written as
#                       `d[0].concat([d[1]])`, copies the whole list on each new item, and
#                       nearley completes every prefix, so a container holding n items costs
#                       O(n^2).  15.9.0 replaces them with a linked `expression_list`
#                       ({previous, value}) materialised once.  The containers changed are the
#                       SELECT clause body, every other clause body (WHERE, FROM, ...), set
#                       operations, ( ) parentheses, [ ] brackets and { } braces.
#   formatter/*, lexer/disambiguateTokens.js   OPERATOR(...) spacing, array-slice colon,
#                       "- -" gluing, reserved words after AS: correctness fixes, not cost.
# So the cost axis is the number of flat items (operands plus separator tokens) inside ONE
# container, and nothing else in the statement matters.  A developer chasing this writes
# statements made of one long flat list of trivial operands and nothing else.
#
# Shape (two statement kinds, one list rule shared by both):
#   SELECT <flat_list> FROM t ;                          the SELECT-clause container
#   SELECT c FROM t WHERE c IN ( <flat_list> ) ;         the ( ) container
# <flat_list> is <elem> <more_el>*, elements are column references or integers, and the
# separator is "," two thirds of the time and OR / AND otherwise, so OR/AND chains (the
# diagnosed 2.05x at 1,000) appear inside the same lists.  One repetition site, <more_el>,
# carries the whole axis and is what example.py bands (stratify=).  A pure OR chain directly
# in the WHERE body (the other-clause container) is left out: it needs a separator set without
# ",", hence a second site and a stratify product of bands; the same quadratic code is reached
# through the two containers kept.
#
# Sub-language argument (every string derivable here is derivable in sql_js.fan):
#   <start>, <select_stmt>  = spec rules with <with_clause_opt>, <order_by_clause_opt>,
#       <limit_offset_opt>, <locking_clause_opt> fixed to their "" alternative and
#       <select_clause> to <simple_select> with zero <set_operation>.
#   <simple_select>  = spec alternative 1 with <all_opt> = "", <select_list_opt> = <ws>
#       <select_list>, <where/group_by/having>_opt = "" (kind 1); or <select_list> = one
#       <target_el> that is a <columnref>, and <where_clause_opt> = <ws> WHERE <ws> <a_expr>
#       where <a_expr> derives down to <pred_expr> alternative 3, <op_expr> <ws> <not_opt>=""
#       IN <ows> <in_expr>, <in_expr> = "(" <ows> <expr_list> <ows> ")" (kind 2).
#   <flat_list>  a string e1 s1 e2 s2 ... en with si in {",", OR, AND}.  Cut at the commas:
#       each piece is ej (OR|AND) ej+1 ... ; cut that at OR into and_exprs, each cut at AND
#       into not_exprs, each a c_expr via the unit chain <not_expr> -> <is_expr> ->
#       <comparison_expr> -> <pred_expr> -> <op_expr> -> <add_expr> -> <mul_expr> ->
#       <exp_expr> -> <at_expr> -> <unary_expr> -> <cast_expr> -> <c_expr>.  The spec's
#       right-recursive <or_expr>/<and_expr> generate exactly these strings, so each piece is
#       an <a_expr>, and the comma-separated pieces form <select_list> (pieces as <target_el>
#       alternative 1, separators as <more_target_el>) or <expr_list> (<more_expr>).  The
#       flat <more_el>* form is a class-1 rewrite of those rules (same strings), made so the
#       axis is one bandable repetition instead of right recursion.
#   <elem>  = <c_expr> alternatives <columnref> | <aexpr_const>, the constant restricted to
#       <iconst> with zero <digit_group>; <columnref> alternatives 1-2 with <subscripts_opt> = "".
#   <table_name>  = spec alternative 1.  <col_id> = its <identifier> alternative.
#   <identifier>, <ident_start>, <ident_char>, <digits>, <digit>  copied unchanged.
#   Key words: the UPPER spelling of each spec key-word group.  <ws> = its " " alternative;
#   <ows> = "" | " " (its "" alternative and the " " alternative of <ws>).
#   Every separator sits where the spec puts <ws> (around OR/AND, after key words) or <ows>
#   (around "," "(" ")" ";").
# Checked 2026-10-02: 120 generated statements (20 in each of the six example.py bands, 52 to
# 2,401 list operands, 816 to 13,243 bytes) all parse with pglast 8.4 (libpg_query 18), the
# spec grammar's soundness oracle.
#
# Bands live in example.py, not here: the list repetition is free (`*`), as in the spec.

<start> ::= <select_stmt> <ows> ";"
<select_stmt> ::= <simple_select>
# Kind 1: the long list is the select list.  Kind 2: the long list is an IN list.
<simple_select> ::= "SELECT" <ws> <flat_list> <from_clause> | "SELECT" <ws> <columnref> <from_clause> <ws> "WHERE" <ws> <columnref> <ws> "IN" <ows> "(" <ows> <flat_list> <ows> ")"
<from_clause> ::= <ws> "FROM" <ws> <table_name>
<table_name> ::= <col_id>

# The one cost axis: operands of one flat container.
<flat_list> ::= <elem> <more_el>*
# Separator then operand; "," two thirds of the time (two-tier, class 1 distribution only).
<more_el> ::= <ows> "," <ows> <elem> | <more_el_bool>
<more_el_bool> ::= <ows> "," <ows> <elem> | <ws> "OR" <ws> <elem> | <ws> "AND" <ws> <elem>
# Simple operands: a column reference or an integer constant.
<elem> ::= <columnref> | <iconst>
<columnref> ::= <col_id> | <col_id> "." <col_id>
<col_id> ::= <identifier>
<identifier> ::= <ident_start> <ident_char>*
<ident_start> ::= "a" | "b" | "c" | "d" | "e" | "_"
<ident_char> ::= "a" | "b" | "c" | "d" | "e" | "_" | "1"
<iconst> ::= <digits>
<digits> ::= <digit>+
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

<ws> ::= " "
<ows> ::= "" | " "

where sql_bytes(<start>) >= 7966.0
where sql_bytes(<start>) <= 9290.0
