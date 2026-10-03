# A PostgreSQL SELECT statement, for three JavaScript SQL parsers.
#
# Transcribed rule by rule from the PostgreSQL 18 documentation (the major that pglast 8.4 /
# libpg_query embeds, used as the soundness oracle):
#   sql-select        the SELECT command synopsis and its clause sections
#   §4.1              lexical structure: identifiers and key words (§4.1.1), constants (§4.1.2),
#                     operators (§4.1.3), special characters (§4.1.4), comments (§4.1.5),
#                     operator precedence (§4.1.6, Table 4.2)
#   §4.2              value expressions (§4.2.1 - §4.2.13)
#   §9.2, §9.7, §9.18, §9.21, §9.23, §9.24   comparison, pattern matching, conditional,
#                     aggregate, subquery and row/array comparison expressions
# Every rule carries a comment naming the section or synopsis item it transcribes.
#
# Single-part input: the statement is the whole file.  Parsing needs no schema, so semantic
# validity (tables and columns existing) is not modelled; only syntactic validity per
# PostgreSQL's raw parser.
#
# Everything that can grow uses `*`, `+` or recursion: select list, FROM list, join chain,
# set-operation chain, WITH list, GROUP BY / ORDER BY lists, expression depth, subquery
# depth, identifier and literal length.  The only numeric bound is Iconst (int32) where the
# grammar demands an integer constant.  Rare constructs are drawn through two-tier
# alternatives (`<x> ::= <common> | <x_rare>`) or right-recursive optional lists, so that
# generation terminates and trees stay readable: distribution only, class 1.
#
# Fandango notes: optional parts are written as an empty alternative (no `?`); one production
# per line; no non-terminal is named after a Python keyword (the FROM clause is
# <from_clause_opt>, key words are <kw_...>), because the .fan parser shares Python's keywords
# and reports the error at the rule that USES the name.
#
# ---------------------------------------------------------------------------------------
# DEVIATIONS FROM THE DOCUMENTED LANGUAGE (probed 2026-09-30, engines as pinned in package.json:
# pgsql-ast-parser 12.0.2, sql-parser-cst 0.42.1, sql-formatter 15.8.2)
#
# Classes: 1 language-preserving rewrite / distribution only; 2 restriction to a named profile
# of another spec; 3 finite lexical vocabulary; 4 construct some engine rejects on >= 95% of
# probe statements exercising it (probe: 40 minimal statements per construct, all accepted by
# pglast; counts are rejections out of 40).
#
# | departure                                                         | class | evidence / note
# |-------------------------------------------------------------------|-------|-----------------------------
# | AND / OR / arithmetic / operator chains as right recursion         | 1 | same strings as the left-assoc rules
# | set operations as a flat left-to-right chain                      | 1 | only UNION remains (INTERSECT/EXCEPT class 4), so precedence is moot
# | two-tier alternatives for rare constructs (NOT, signs, casts, AT,  | 1 | distribution only
# |   ^, subscripts, quoted identifiers, compound primaries, whitespace)|   |
# | key-word case: UPPER, lower, Capitalised per key word             | 3 | §4.1.1 key words are case-insensitive; a sample of spellings
# | whitespace: space / tab / newline / "/* c */" / "-- c\n"; optional | 3 | §4.1 whitespace is free; no whitespace around "." and "::"
# |   whitespace only next to ( ) , ;                                  |   |
# | unquoted identifiers over {a-e, _} then {a-e, _, 1}                | 3 | §4.1.1; length free
# | quoted identifiers over {a, B, space, ., ""}                       | 3 | §4.1.1
# | string / escape-string / U&-string / bit-string characters         | 3 | §4.1.2.1-5 samples
# | function names: 17 Chapter 9 names, optionally schema-qualified    | 3 | the raw grammar takes any identifier
# | operators: || ~ !~ ~* !~* ~~ !~~ # & | << >> @> <@ && -> ->>, and   | 3 | §4.1.3 operators are user-definable
# |   OPERATOR(schema.op) over + - * / < > = ||                          |   |
# | type names: 17 Chapter 8 types with modifiers, plus any identifier | 3 | Chapter 8
# | typed literals type 'x' only for date, timestamp, interval, time    | 4 | cst: int/text 40, boolean 40, generic name 40, timestamp with time zone 40
# | no comment directly after NOT, WITH, NULLS                         | oracle | libpg_query 18 (pglast 8.4) rejects "a NOT /* c */ IN (1)"
# |                                                                   |       | and "::timestamp with /* c */ time zone"; a PostgreSQL 14 server
# |                                                                   |       | accepts both.  Kept out so the oracle can score soundness.
# | precedence corners not generated: a completed postfix predicate as | none  | residual gap of the precedence-stratified rewrite (not class 1):
# |   left operand of a tighter operator ("a IS NULL + 1", "a IN (1) || b"),|  | engines reject about half (pgsql 21/40, cst 18/40), so it would
# |   comparison/LIKE-level ANY as an operand ("a = ANY (s) = b")      |       | stay by the rules; not transcribed for time
# | right-operand prefix NOT ("a = NOT b")                             | 4 | pgsql 40, cst 40
# | out of scope, not transcribed: VALUES lists and DML in WITH, SELECT| none  | outside the SELECT synopsis items this subject covers, or
# |   INTO, special-syntax functions (EXTRACT, SUBSTRING, POSITION,    |       | (special functions, JSON/XML) not reached in the time available
# |   TRIM, OVERLAY, CURRENT_DATE...), JSON/XML constructs, IS JSON,   |       |
# |   IS NORMALIZED, IS DOCUMENT, WITHIN GROUP-only aggregates          |       |
#
# Class 4 exclusions (engine: rejections / 40 probe statements):
#   pgsql-ast-parser: NATURAL join 40 (cst 40 too); INTERSECT 40; EXCEPT 40; UNION DISTINCT 40;
#     LIMIT ALL 40; FETCH ... WITH TIES 40; BETWEEN SYMMETRIC 40; LIKE ... ESCAPE 40; SIMILAR TO 40;
#     IS [NOT] DISTINCT FROM 40; IS [NOT] UNKNOWN 40; WINDOW clause 40; OVER window_name 40;
#     window frame clause 40; signed exponent (1e-3) 40; GROUP BY () 40; GROUP BY ALL/DISTINCT 40;
#     GROUPING SETS 40; ONLY table 40; table * 40; TABLESAMPLE 40; FOR ... OF / NOWAIT / SKIP LOCKED 40;
#     repeated locking clauses 40; locking clause before LIMIT 40; WITH column list 40;
#     [NOT] MATERIALIZED 40; SEARCH / CYCLE 40; WITH RECURSIVE without column list 40;
#     WITH RECURSIVE body without UNION 40; WITH body in double parentheses 40; COLLATE 40;
#     field selection (e).f 40; (e).* 40 (cst 40); array slice [a:b] 40; sized array bound followed
#     by more bounds (int[3][]) 40; dollar quoting 40; string continuation across newline 40;
#     prefix operators (~ @ |/) 40; named arguments => 40; VARIADIC 40 (cst 40); ORDER BY ... USING 40;
#     alias on a parenthesised join 40; FROM subquery without alias 40; parenthesised whole statement 40;
#     4-part column reference 40; catalog.schema.table 40; AT LOCAL 40 (cst 40); AT TIME ZONE with a
#     signed zone 40; right-nested join (a JOIN b JOIN c ON .. ON ..) 40 (cst 40); JOIN USING ... AS 40 (cst 40)
#   sql-parser-cst: WITHIN GROUP 40; nested ARRAY[[...]] 40; aggregate ALL 40; t.* outside the select
#     list 40; OFFSET ... ROWS after LIMIT 40; positional parameters $n 40; lowercase e'' prefix 40;
#     typed literals above
#   sql-formatter: hexadecimal / octal / binary integers (0x1F, 0o7, 0b1) 40
#
# Engine judgement: pgsql-ast-parser alone blocks ~48 documented SELECT constructs outright, and
# partially rejects many more (casts of 1_000 / 97e19 literals, a[1]::t, some E'' escapes,
# "a -> b" between identifiers, "Ambiguous SQL syntax").  Those partial ones STAY: the harness
# drops disagreeing inputs per engine pair at scoring time.
# ---------------------------------------------------------------------------------------
# Key words (§4.1.1, Appendix C) are written inline as a group of three spellings,
# ("SELECT" | "select" | "Select"): UPPER, lower and Capitalised, a class 3 sample of the
# case-insensitive spellings.  Inline rather than one rule per key word because
# core/grammar_props.py's per-site expansion bound grows with the cube of the number of
# non-terminals, and 94 key-word rules made one analysis pass take minutes.

# ===================================================================
# Statement.  sql-select Synopsis:
#   [ WITH [ RECURSIVE ] with_query [, ...] ]
#   SELECT ... [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
#   [ ORDER BY ... ] [ LIMIT ... ] [ OFFSET ... ] [ FETCH ... ] [ FOR ... ]
# ===================================================================

# Synopsis, whole statement; one statement terminated by ";" (§4.1.4 special characters).
<start> ::= <select_stmt> <ows> ";"
# Synopsis: optional WITH, the select body with set operations, then ORDER BY, the
# row-limiting clauses and the locking clause, in the synopsis order.
<select_stmt> ::= <with_clause_opt> <select_clause> <order_by_clause_opt> <limit_offset_opt> <locking_clause_opt>

# --- WITH Clause (sql-select "WITH Clause") ---
# Synopsis: [ WITH [ RECURSIVE ] with_query [, ...] ]
<with_clause_opt> ::= "" | ("WITH" | "with" | "With") <ws_nc> <with_query> <more_with_query>* <ws> | ("WITH" | "with" | "With") <ws_nc> ("RECURSIVE" | "recursive" | "Recursive") <ws> <recursive_with_query> <more_recursive_with_query>* <ws>
# WITH RECURSIVE: with_query_name ( column_name [, ...] ) AS ( non_recursive_term UNION [ ALL ] recursive_term ).
# The column list and the UNION are optional in PostgreSQL; RECURSIVE without either is class 4.
<recursive_with_query> ::= <with_query_name> <ows> "(" <ows> <name_list> <ows> ")" <ws> ("AS" | "as" | "As") <ows> "(" <ows> <set_operand> <set_operation>+ <ows> ")"
# [, ...] under RECURSIVE (each query may or may not be recursive; written in the recursive shape).
<more_recursive_with_query> ::= <ows> "," <ows> <recursive_with_query>
# Synopsis: with_query [, ...]
<more_with_query> ::= <ows> "," <ows> <with_query>
# with_query: with_query_name AS ( select ).  Column list, [NOT] MATERIALIZED,
# SEARCH and CYCLE are class 4 (see header).
<with_query> ::= <with_query_name> <ws> ("AS" | "as" | "As") <ows> <select_with_parens>
# with_query_name: a name (§4.1.1 identifiers).
<with_query_name> ::= <col_id>

# --- Set operations (sql-select "UNION Clause", "INTERSECT", "EXCEPT") ---
# select_statement UNION [ ALL | DISTINCT ] select_statement, left-associative chain.
# The first operand is unparenthesised (a whole-statement "( select )" is class 4).
<select_clause> ::= <simple_select> <set_operation>* | <select_with_parens> <set_operation>+
# UNION [ ALL ] select_statement.  INTERSECT, EXCEPT and UNION DISTINCT are class 4.
<set_operation> ::= <ws> ("UNION" | "union" | "Union") <set_quantifier_opt> <ws> <set_operand>
# [ ALL ]: UNION ALL keeps duplicates.
<set_quantifier_opt> ::= "" | <ws> ("ALL" | "all" | "All")
# The operand of a set operation: a SELECT, or a parenthesised select (which may
# carry its own ORDER BY / LIMIT, per "UNION Clause").
<set_operand> ::= <simple_select> | <select_with_parens>
# ( select ): a parenthesised full select, used for subqueries (§4.2.11, §9.23)
# and FROM-clause sub-SELECTs.
<select_with_parens> ::= "(" <ows> <select_stmt> <ows> ")"

# --- SELECT List and main clauses ---
# SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ] [ * | expression [ [ AS ] output_name ] [, ...] ]
#   [ FROM from_item [, ...] ] [ WHERE condition ] [ GROUP BY grouping_element [, ...] ] [ HAVING condition ]
# The select list is optional after SELECT / SELECT ALL, required after DISTINCT.
<simple_select> ::= ("SELECT" | "select" | "Select") <all_opt> <select_list_opt> <from_clause_opt> <where_clause_opt> <group_by_clause_opt> <having_clause_opt> | ("SELECT" | "select" | "Select") <ws> <distinct_clause> <ws> <select_list> <from_clause_opt> <where_clause_opt> <group_by_clause_opt> <having_clause_opt>
# SELECT ALL (the default, written out).
<all_opt> ::= "" | <ws> ("ALL" | "all" | "All")
# "DISTINCT Clause": DISTINCT | DISTINCT ON ( expression [, ...] ).
<distinct_clause> ::= ("DISTINCT" | "distinct" | "Distinct") | ("DISTINCT" | "distinct" | "Distinct") <ws> ("ON" | "on" | "On") <ows> "(" <ows> <expr_list> <ows> ")"
# Optional select list ("SELECT List"; an empty list is allowed).
<select_list_opt> ::= "" | <ws> <select_list>
# "SELECT List": output items separated by commas.
<select_list> ::= <target_el> <more_target_el>*
# [, ...] of the select list.
<more_target_el> ::= <ows> "," <ows> <target_el>
# "SELECT List" items: expression [ [ AS ] output_name ], *, and table_name.* (§4.2.4 / §8.16.5).
<target_el> ::= <a_expr> | <a_expr> <ws> ("AS" | "as" | "As") <ws> <output_name> | <a_expr> <ws> <output_name> | "*" | <col_id> "." "*"
# output_name (a column label).
<output_name> ::= <col_id>

# --- FROM Clause ---
# FROM from_item [, ...]
<from_clause_opt> ::= "" | <ws> ("FROM" | "from" | "From") <ws> <from_item> <more_from_item>*
# [, ...]: comma is a cross join.
<more_from_item> ::= <ows> "," <ows> <from_item>
# from_item join_type from_item ON/USING, from_item CROSS JOIN from_item: a left-deep
# chain of joins on a primary from_item (right-nested joins are class 4).
<from_item> ::= <table_primary> <joined_table>*
# join_type from_item { ON join_condition | USING ( join_column [, ...] ) } | CROSS JOIN from_item.
# NATURAL is class 4.
<joined_table> ::= <ws> <join_type> ("JOIN" | "join" | "Join") <ws> <table_primary> <ws> <join_qual> | <ws> ("CROSS" | "cross" | "Cross") <ws> ("JOIN" | "join" | "Join") <ws> <table_primary>
# join_type: [ INNER ] JOIN | LEFT [ OUTER ] JOIN | RIGHT [ OUTER ] JOIN | FULL [ OUTER ] JOIN.
<join_type> ::= "" | ("INNER" | "inner" | "Inner") <ws> | ("LEFT" | "left" | "Left") <ws> <outer_opt> | ("RIGHT" | "right" | "Right") <ws> <outer_opt> | ("FULL" | "full" | "Full") <ws> <outer_opt>
# OUTER is optional.
<outer_opt> ::= "" | ("OUTER" | "outer" | "Outer") <ws>
# ON join_condition | USING ( join_column [, ...] ).  "USING ... AS join_using_alias" is class 4.
<join_qual> ::= ("ON" | "on" | "On") <ws> <a_expr> | ("USING" | "using" | "Using") <ows> "(" <ows> <name_list> <ows> ")"
# from_item alternatives: table_name [ [ AS ] alias [ ( column_alias [, ...] ) ] ];
# [ LATERAL ] ( select ) [ AS ] alias; [ LATERAL ] function_name ( ... ) [ WITH ORDINALITY ] [ [ AS ] alias ];
# ( from_item join ... ) (a parenthesised join, §7.2.1.1).  ONLY, table *, TABLESAMPLE,
# subquery without alias and an alias on a parenthesised join are class 4.
<table_primary> ::= <table_name> <alias_clause_opt> | <lateral_opt> <select_with_parens> <ws> <alias_clause> | <lateral_opt> <func_application> <with_ordinality_opt> <alias_clause_opt> | "(" <ows> <table_primary> <joined_table>+ <ows> ")"
# [ LATERAL ].
<lateral_opt> ::= "" | ("LATERAL" | "lateral" | "Lateral") <ws>
# WITH ORDINALITY on a function in FROM.
<with_ordinality_opt> ::= "" | <ws> ("WITH" | "with" | "With") <ws_nc> ("ORDINALITY" | "ordinality" | "Ordinality")
# table_name: optionally schema-qualified (§5.10 / §4.1.1); catalog.schema.table is class 4.
<table_name> ::= <col_id> | <col_id> "." <col_id>
# [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
<alias_clause_opt> ::= "" | <ws> <alias_clause>
# [ AS ] alias [ ( column_alias [, ...] ) ]
<alias_clause> ::= <as_opt> <col_id> <column_alias_list_opt>
# AS is optional before an alias.
<as_opt> ::= "" | ("AS" | "as" | "As") <ws>
# ( column_alias [, ...] )
<column_alias_list_opt> ::= "" | <ows> "(" <ows> <name_list> <ows> ")"
# name [, ...] (join_column / column_alias lists).
<name_list> ::= <col_id> <more_name>*
# [, ...] of a name list.
<more_name> ::= <ows> "," <ows> <col_id>

# --- WHERE Clause ---
# WHERE condition (any boolean value expression).
<where_clause_opt> ::= "" | <ws> ("WHERE" | "where" | "Where") <ws> <a_expr>

# --- GROUP BY Clause ---
# GROUP BY grouping_element [, ...].  GROUP BY ALL/DISTINCT, ( ) and GROUPING SETS are class 4.
<group_by_clause_opt> ::= "" | <ws> ("GROUP" | "group" | "Group") <ws> ("BY" | "by" | "By") <ws> <grouping_element> <more_grouping_element>*
# [, ...]
<more_grouping_element> ::= <ows> "," <ows> <grouping_element>
# grouping_element: expression | ( expression [, ...] ) (a row, §4.2.13) | ROLLUP ( ... ) | CUBE ( ... ).
<grouping_element> ::= <a_expr> | ("ROLLUP" | "rollup" | "Rollup") <ows> "(" <ows> <expr_list> <ows> ")" | ("CUBE" | "cube" | "Cube") <ows> "(" <ows> <expr_list> <ows> ")"

# --- HAVING Clause ---
# HAVING condition.  (The WINDOW clause is class 4.)
<having_clause_opt> ::= "" | <ws> ("HAVING" | "having" | "Having") <ws> <a_expr>

# --- ORDER BY Clause ---
# ORDER BY expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...].  USING operator is class 4.
<order_by_clause_opt> ::= "" | <ws> <order_by_clause>
# ORDER BY sortby [, ...] (also used inside aggregates §4.2.7 and windows §4.2.8).
<order_by_clause> ::= ("ORDER" | "order" | "Order") <ws> ("BY" | "by" | "By") <ws> <sortby> <more_sortby>*
# [, ...]
<more_sortby> ::= <ows> "," <ows> <sortby>
# expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ]
<sortby> ::= <a_expr> <asc_desc_opt> <nulls_order_opt>
# [ ASC | DESC ]
<asc_desc_opt> ::= "" | <ws> ("ASC" | "asc" | "Asc") | <ws> ("DESC" | "desc" | "Desc")
# [ NULLS { FIRST | LAST } ]
<nulls_order_opt> ::= "" | <ws> ("NULLS" | "nulls" | "Nulls") <ws_nc> ("FIRST" | "first" | "First") | <ws> ("NULLS" | "nulls" | "Nulls") <ws_nc> ("LAST" | "last" | "Last")

# --- LIMIT Clause ---
# LIMIT { count | ALL } / OFFSET start [ ROW | ROWS ] / FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY.
# PostgreSQL accepts LIMIT and OFFSET in either order, and OFFSET before FETCH.
# LIMIT ALL, WITH TIES, and OFFSET ... ROWS after LIMIT are class 4.
<limit_offset_opt> ::= "" | <ws> <limit_clause> | <ws> <limit_clause> <ws> <offset_clause> | <ws> <offset_clause> | <ws> <offset_rows_clause> | <ws> <offset_clause> <ws> <limit_clause> | <ws> <fetch_clause> | <ws> <offset_rows_clause> <ws> <fetch_clause> | <ws> <offset_clause> <ws> <fetch_clause>
# LIMIT count (count is an expression).
<limit_clause> ::= ("LIMIT" | "limit" | "Limit") <ws> <a_expr>
# OFFSET start.
<offset_clause> ::= ("OFFSET" | "offset" | "Offset") <ws> <a_expr>
# OFFSET start { ROW | ROWS } (start is a constant or c_expr in the grammar; a constant here).
<offset_rows_clause> ::= ("OFFSET" | "offset" | "Offset") <ws> <int32_const> <ws> <row_or_rows>
# FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY
<fetch_clause> ::= ("FETCH" | "fetch" | "Fetch") <ws> <first_or_next> <ws> <fetch_count_opt> <row_or_rows> <ws> ("ONLY" | "only" | "Only")
# FIRST | NEXT
<first_or_next> ::= ("FIRST" | "first" | "First") | ("NEXT" | "next" | "Next")
# [ count ]
<fetch_count_opt> ::= "" | <int32_const> <ws>
# ROW | ROWS
<row_or_rows> ::= ("ROW" | "row" | "Row") | ("ROWS" | "rows" | "Rows")

# --- The Locking Clause ---
# FOR lock_strength (a single clause, not before LIMIT; OF / NOWAIT / SKIP LOCKED and
# repeated clauses are class 4).
<locking_clause_opt> ::= "" | <ws> ("FOR" | "for" | "For") <ws> <lock_strength>
# lock_strength: UPDATE | NO KEY UPDATE | SHARE | KEY SHARE
<lock_strength> ::= ("UPDATE" | "update" | "Update") | ("NO" | "no" | "No") <ws> ("KEY" | "key" | "Key") <ws> ("UPDATE" | "update" | "Update") | ("SHARE" | "share" | "Share") | ("KEY" | "key" | "Key") <ws> ("SHARE" | "share" | "Share")

# ===================================================================
# Value expressions (§4.2) with operator precedence (§4.1.6, Table 4.2),
# lowest precedence first.  Each level is one row of Table 4.2.
# ===================================================================

# §4.2: a value expression; lowest level is OR.
<a_expr> ::= <or_expr>
# Table 4.2 "OR" (left assoc; same strings as a left-recursive chain).
<or_expr> ::= <and_expr> | <and_expr> <ws> ("OR" | "or" | "Or") <ws> <or_expr>
# Table 4.2 "AND".
<and_expr> ::= <not_expr> | <not_expr> <ws> ("AND" | "and" | "And") <ws> <and_expr>
# Table 4.2 "NOT" (right assoc, prefix).
<not_expr> ::= <is_expr> | <not_expr_rare>
# Second tier of the NOT level, so that a prefix NOT is drawn a third of the time (class 1: distribution).
<not_expr_rare> ::= <is_expr> | ("NOT" | "not" | "Not") <ws_nc> <not_expr>
# Table 4.2 "IS, ISNULL, NOTNULL" (non-associative): §9.2 IS [NOT] NULL, ISNULL, NOTNULL,
# IS [NOT] TRUE / FALSE.  IS UNKNOWN and IS [NOT] DISTINCT FROM are class 4.
<is_expr> ::= <comparison_expr> | <comparison_expr> <ws> <is_test>
# §9.2 Table 9.2 comparison predicates of the IS family.
<is_test> ::= ("IS" | "is" | "Is") <ws> <not_opt> ("NULL" | "null" | "Null") | ("ISNULL" | "isnull" | "Isnull") | ("NOTNULL" | "notnull" | "Notnull") | ("IS" | "is" | "Is") <ws> <not_opt> ("TRUE" | "true" | "True") | ("IS" | "is" | "Is") <ws> <not_opt> ("FALSE" | "false" | "False")
# [ NOT ]
<not_opt> ::= "" | ("NOT" | "not" | "Not") <ws_nc>
# Table 4.2 "< > = <= >= <>" (non-associative), §9.2 Table 9.1.
<comparison_expr> ::= <pred_expr> | <pred_expr> <ws> <comp_op> <ws> <pred_expr> | <pred_expr> <ws> <comp_op> <ws> <sub_type> <ows> <sub_operand>
# §9.23.4-5 / §9.24.3-4: ( subquery ) or ( array expression ) after ANY / SOME / ALL.
<sub_operand> ::= <select_with_parens> | "(" <ows> <a_expr> <ows> ")"
# §9.2 Table 9.1 comparison operators (!= is an alias of <>).
<comp_op> ::= "<" | ">" | "=" | "<=" | ">=" | "<>" | "!="
# Table 4.2 "BETWEEN IN LIKE ILIKE SIMILAR" (non-associative):
# §9.2 a [NOT] BETWEEN x AND y; §9.24.1/§9.23.2 [NOT] IN ( list | subquery ); §9.7.1 [NOT] LIKE / ILIKE.
# BETWEEN SYMMETRIC, ESCAPE and SIMILAR TO are class 4.
<pred_expr> ::= <op_expr> | <op_expr> <ws> <not_opt> ("BETWEEN" | "between" | "Between") <ws> <b_op_expr> <ws> ("AND" | "and" | "And") <ws> <op_expr> | <op_expr> <ws> <not_opt> ("IN" | "in" | "In") <ows> <in_expr> | <op_expr> <ws> <not_opt> <like_op> <ws> <op_expr> | <op_expr> <ws> <not_opt> <like_op> <ws> <sub_type> <ows> <sub_operand>
# §9.7.1 LIKE and its case-insensitive form ILIKE.
<like_op> ::= ("LIKE" | "like" | "Like") | ("ILIKE" | "ilike" | "Ilike")
# §9.24.1 IN ( value [, ...] ) and §9.23.2 IN ( subquery ).
<in_expr> ::= <select_with_parens> | "(" <ows> <expr_list> <ows> ")"
# Table 4.2 "(any other operator)" (left assoc), plus §9.23.4/§9.24.3 "expression operator ANY|SOME|ALL (...)"
# for an operator of this level.  ANY/ALL after a comparison operator sits at the comparison level and
# after [NOT] LIKE / ILIKE at the LIKE level: the parser resolves them by the operator token's precedence,
# so "a = b = ANY (s)" is a syntax error, which placing them here would generate.
<op_expr> ::= <add_expr> | <add_expr> <op_tail> <op_tail_more>
# Further steps of the operator chain, as right recursion (geometric length; class 1).
<op_tail_more> ::= "" | <op_tail> <op_tail_more>
# One step of the "any other operator" chain.
<op_tail> ::= <ws> <qual_op> <ws> <add_expr> | <ws> <qual_op> <ws> <sub_type> <ows> <sub_operand>
# The BETWEEN lower bound is a restricted expression (b_expr in gram.y): the operator,
# arithmetic, sign and cast levels only; no ANY/ALL and no AT TIME ZONE.  Right recursion,
# same strings as the left-associative chains (class 1).
<b_op_expr> ::= <b_add_expr> | <b_add_expr> <ws> <qual_op> <ws> <b_op_expr>
# b_expr "+ -" level.
<b_add_expr> ::= <b_mul_expr> | <b_mul_expr> <ws> "+" <ws> <b_add_expr> | <b_mul_expr> <ws> "-" <ws> <b_add_expr>
# b_expr "* / %" level.
<b_mul_expr> ::= <b_exp_expr> | <b_exp_expr> <ws> "*" <ws> <b_mul_expr> | <b_exp_expr> <ws> "/" <ws> <b_mul_expr> | <b_exp_expr> <ws> "%" <ws> <b_mul_expr>
# b_expr "^" level, over signed / cast primaries.
<b_exp_expr> ::= <unary_expr> | <unary_expr> <ws> "^" <ws> <b_exp_expr>
# §4.1.3 operators (user-definable; class 3 vocabulary) and §4.2.5 OPERATOR(schema.op).
<qual_op> ::= "||" | "~" | "!~" | "~*" | "!~*" | "~~" | "!~~" | "#" | "&" | "|" | "<<" | ">>" | "@>" | "<@" | "&&" | "->" | "->>" | ("OPERATOR" | "operator" | "Operator") "(" <col_id> "." <any_operator> ")"
# The operator named inside OPERATOR( ).
<any_operator> ::= "+" | "-" | "*" | "/" | "<" | ">" | "=" | "||"
# ANY | SOME | ALL
<sub_type> ::= ("ANY" | "any" | "Any") | ("SOME" | "some" | "Some") | ("ALL" | "all" | "All")
# Table 4.2 "+ -" (binary, left assoc).
<add_expr> ::= <mul_expr> | <mul_expr> <add_tail> <add_tail_more>
# Further addition steps (right recursion; class 1).
<add_tail_more> ::= "" | <add_tail> <add_tail_more>
# One addition / subtraction step.
<add_tail> ::= <ws> "+" <ws> <mul_expr> | <ws> "-" <ws> <mul_expr>
# Table 4.2 "* / %" (left assoc).
<mul_expr> ::= <exp_expr> | <exp_expr> <mul_tail> <mul_tail_more>
# Further multiplication steps (right recursion; class 1).
<mul_tail_more> ::= "" | <mul_tail> <mul_tail_more>
# One multiplication / division / modulo step.
<mul_tail> ::= <ws> "*" <ws> <exp_expr> | <ws> "/" <ws> <exp_expr> | <ws> "%" <ws> <exp_expr>
# Table 4.2 "^" (left assoc).
<exp_expr> ::= <at_expr> | <exp_expr_rare>
# Second tier: an exponentiation chain a quarter of the time (class 1).
<exp_expr_rare> ::= <at_expr> | <at_expr> <exp_tail> <exp_tail_more>
# Further exponentiation steps.
<exp_tail_more> ::= "" | <exp_tail> <exp_tail_more>
# One exponentiation step.
<exp_tail> ::= <ws> "^" <ws> <at_expr>
# Table 4.2 "AT" (AT TIME ZONE, §9.9.4; left assoc).  AT LOCAL is class 4.  (COLLATE, the row
# above, is class 4.)
<at_expr> ::= <unary_expr> | <at_expr_rare>
# Second tier: AT TIME ZONE a quarter of the time (class 1).
<at_expr_rare> ::= <unary_expr> | <unary_expr> <at_tail> <at_tail_more>
# Further AT TIME ZONE steps.
<at_tail_more> ::= "" | <at_tail> <at_tail_more>
# AT TIME ZONE zone (a signed zone operand is class 4).
<at_tail> ::= <ws> ("AT" | "at" | "At") <ws> ("TIME" | "time" | "Time") <ws> ("ZONE" | "zone" | "Zone") <ws> <cast_expr>
# Table 4.2 "+ -" (unary, right assoc).
<unary_expr> ::= <cast_expr> | <unary_expr_rare>
# Second tier: a sign a third of the time (class 1).
<unary_expr_rare> ::= <cast_expr> | "-" <ws> <unary_expr> | "+" <ws> <unary_expr>
# Table 4.2 "::" (left assoc), §4.2.9 expression::type.
<cast_expr> ::= <c_expr> | <cast_expr_rare>
# Second tier: casts a quarter of the time, chained geometrically (class 1).
<cast_expr_rare> ::= <c_expr> | <c_expr> <typecast> <typecast_more>
# Further ::type steps.
<typecast_more> ::= "" | <typecast> <typecast_more>
# ::type
<typecast> ::= "::" <typename>

# --- Primary expressions (c_expr in gram.y), §4.2.1 - §4.2.13 ---
# §4.2 list: column reference (§4.2.1), constant (§4.1.2), parenthesised expression (§4.2),
# function call (§4.2.6), aggregate (§4.2.7), window call (§4.2.8), CAST (§4.2.9),
# scalar subquery (§4.2.11, subscriptable per §4.2.3), array constructor (§4.2.12), row constructor (§4.2.13),
# CASE (§9.18.1), COALESCE / NULLIF / GREATEST / LEAST (§9.18.2-4), EXISTS (§9.23.1),
# GROUPING (§9.21).  Positional parameters $n are class 4.
<c_expr> ::= <columnref> | <aexpr_const> | <c_expr_compound>
# The compound primaries, drawn a third of the time so that trees terminate (class 1).
<c_expr_compound> ::= <columnref> | <aexpr_const> | "(" <ows> <a_expr> <ows> ")" <subscripts_opt> | <func_expr> | <cast_function> | <select_with_parens> <subscripts_opt> | <array_expr> | <row_expr> | <case_expr> | <conditional_function> | ("EXISTS" | "exists" | "Exists") <ows> <select_with_parens> | ("GROUPING" | "grouping" | "Grouping") <ows> "(" <ows> <expr_list> <ows> ")"
# expression [, ...]
<expr_list> ::= <a_expr> <more_expr>*
# [, ...]
<more_expr> ::= <ows> "," <ows> <a_expr>

# §4.2.1 column reference: correlation.columnname, optionally schema-qualified (at most three
# parts: four and more are class 4), with §4.2.3 subscripts.
<columnref> ::= <col_id> <subscripts_opt> | <col_id> "." <col_id> <subscripts_opt> | <col_id> "." <col_id> "." <col_id> <subscripts_opt>
# §4.2.3 subscripts, geometric: none half the time, then right recursion (class 1).
<subscripts_opt> ::= "" | <subscripts_rare>
# Second tier of subscripts.
<subscripts_rare> ::= "" | <subscript> <subscripts_opt>
# §4.2.3 expression[subscript] (slices are class 4).
<subscript> ::= "[" <ows> <a_expr> <ows> "]"

# §4.2.6 function calls, §4.2.7 aggregate expressions, §4.2.8 window function calls:
# function_name ( ... ) [ FILTER ( WHERE filter_clause ) ] [ OVER ( window_definition ) ].
# WITHIN GROUP, OVER window_name and frame clauses are class 4.
<func_expr> ::= <func_application> <filter_clause_opt> <over_clause_opt>
# §4.2.6 function_name ( [ argument [, ...] ] ); §4.2.7 aggregate_name ( [ DISTINCT ] expression [, ...]
# [ order_by_clause ] ) and aggregate_name ( * ).  ALL, VARIADIC and named arguments are class 4.
<func_application> ::= <func_name> <ows> "(" <ows> ")" | <func_name> <ows> "(" <ows> <expr_list> <agg_order_by_opt> <ows> ")" | <func_name> <ows> "(" <ows> ("DISTINCT" | "distinct" | "Distinct") <ws> <expr_list> <agg_order_by_opt> <ows> ")" | <func_name> <ows> "(" <ows> "*" <ows> ")"
# §4.2.7 the aggregate's [ order_by_clause ].
<agg_order_by_opt> ::= "" | <ws> <order_by_clause>
# §4.2.7 [ FILTER ( WHERE filter_clause ) ]
<filter_clause_opt> ::= "" | <ws> ("FILTER" | "filter" | "Filter") <ows> "(" <ows> ("WHERE" | "where" | "Where") <ws> <a_expr> <ows> ")"
# §4.2.8 OVER ( window_definition )
<over_clause_opt> ::= "" | <ws> ("OVER" | "over" | "Over") <ows> "(" <ows> <window_definition> <ows> ")"
# §4.2.8 window_definition: [ PARTITION BY expression [, ...] ] [ ORDER BY ... ]  (existing_window_name
# and frame_clause are class 4).
<window_definition> ::= "" | <partition_clause> | <order_by_clause> | <partition_clause> <ws> <order_by_clause>
# PARTITION BY expression [, ...]
<partition_clause> ::= ("PARTITION" | "partition" | "Partition") <ws> ("BY" | "by" | "By") <ws> <expr_list>
# §4.2.6 function_name, optionally schema-qualified (class 3 vocabulary: names of built-in
# functions from Chapter 9; the grammar accepts any identifier here).
<func_name> ::= <builtin_func> | <col_id> "." <builtin_func>
# Class 3: a sample of Chapter 9 function names, aggregates (§9.21) and window functions (§9.22).
<builtin_func> ::= "count" | "sum" | "avg" | "min" | "max" | "lower" | "upper" | "abs" | "length" | "round" | "now" | "string_agg" | "array_agg" | "row_number" | "rank" | "Count" | "SUM"

# §4.2.9 CAST ( expression AS type ).
<cast_function> ::= ("CAST" | "cast" | "Cast") <ows> "(" <ows> <a_expr> <ws> ("AS" | "as" | "As") <ws> <typename> <ows> ")"
# §4.2.12 ARRAY[ expression [, ...] ] (possibly empty) and ARRAY( subquery ).  Nested
# ARRAY[[...]] literals are class 4.
<array_expr> ::= ("ARRAY" | "array" | "Array") "[" <ows> "]" | ("ARRAY" | "array" | "Array") "[" <ows> <expr_list> <ows> "]" | ("ARRAY" | "array" | "Array") <ows> <select_with_parens>
# §4.2.13 row constructor: ROW ( [ expression [, ...] ] ) or ( expression , expression [, ...] ).
<row_expr> ::= ("ROW" | "row" | "Row") <ows> "(" <ows> ")" | ("ROW" | "row" | "Row") <ows> "(" <ows> <expr_list> <ows> ")" | "(" <ows> <a_expr> <ows> "," <ows> <expr_list> <ows> ")"
# §9.18.1 CASE WHEN condition THEN result [ WHEN ... ] [ ELSE result ] END, and the simple
# form CASE expression WHEN value THEN result ... END.
<case_expr> ::= ("CASE" | "case" | "Case") <ws> <case_arg_opt> <when_clause>+ <case_default_opt> ("END" | "end" | "End")
# The simple form's expression.
<case_arg_opt> ::= "" | <a_expr> <ws>
# WHEN condition THEN result
<when_clause> ::= ("WHEN" | "when" | "When") <ws> <a_expr> <ws> ("THEN" | "then" | "Then") <ws> <a_expr> <ws>
# [ ELSE result ]
<case_default_opt> ::= "" | ("ELSE" | "else" | "Else") <ws> <a_expr> <ws>
# §9.18.2 COALESCE, §9.18.3 NULLIF, §9.18.4 GREATEST / LEAST.
<conditional_function> ::= ("COALESCE" | "coalesce" | "Coalesce") <ows> "(" <ows> <expr_list> <ows> ")" | ("NULLIF" | "nullif" | "Nullif") <ows> "(" <ows> <a_expr> <ows> "," <ows> <a_expr> <ows> ")" | ("GREATEST" | "greatest" | "Greatest") <ows> "(" <ows> <expr_list> <ows> ")" | ("LEAST" | "least" | "Least") <ows> "(" <ows> <expr_list> <ows> ")"

# --- Constants, §4.1.2 ---
# §4.1.2 constants; plus the keyword constants TRUE, FALSE, NULL (§8.6, §4.1.2.7 context).
# §4.1.2.7 "type 'string'" typed literal.
<aexpr_const> ::= <iconst> | <fconst> | <sconst> | <bconst> | <xconst> | ("TRUE" | "true" | "True") | ("FALSE" | "false" | "False") | ("NULL" | "null" | "Null") | <const_typename> <ws> <sconst>
# §4.1.2.6 numeric constants, integer form: digits, with "_" separators between digits (PG 16+).
# Hexadecimal / octal / binary integers are class 4.
<iconst> ::= <digits> <digit_group>*
# Iconst in gram.y: an integer that fits int32 (2^31-1 has ten digits, so nine are always safe).
# Used where the grammar demands Iconst: array bounds, OFFSET ... ROWS, FETCH count.  A bound
# from the spec, not a cap.
<int32_const> ::= <digit> | <nonzero_digit> <digit>{0,8}
# 1-9
<nonzero_digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
# _digits
<digit_group> ::= "_" <digits>
# §4.1.2.6 digits.[digits][e[+-]digits] | [digits].digits[e...] | digitse[+-]digits.
# A signed exponent is class 4.
<fconst> ::= <digits> "." <digits_opt> <exponent_opt> | "." <digits> <exponent_opt> | <digits> <exponent>
# [ e digits ]
<exponent_opt> ::= "" | <exponent>
# e digits (E or e).
<exponent> ::= "e" <digits> | "E" <digits>
# §4.1.2.6 digits: one or more decimal digits.
<digits> ::= <digit>+
# [ digits ]
<digits_opt> ::= "" | <digits>
# decimal digit
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
# §4.1.2.1 'string' with '' for a quote; §4.1.2.2 E'escape string'; §4.1.2.3 U&'unicode string'.
# Dollar quoting and newline-separated continuation are class 4.
<sconst> ::= "'" <schar>* "'" | <e_prefix> "'" <echar>* "'" | "U&'" <uchar>* "'"
# E (lowercase e is class 4).
<e_prefix> ::= "E"
# Class 3: a sample of string characters, including the doubled quote.
<schar> ::= "x" | "y" | "z" | " " | "''" | "\\"
# Class 3: escape-string characters: plain ones and the §4.1.2.2 Table 4.1 backslash escapes.
<echar> ::= "x" | "y" | " " | "\\n" | "\\t" | "\\\\" | "\\'" | "''" | "\\x41" | "\\101"
# Class 3: Unicode-escape string characters (§4.1.2.3 \XXXX).
<uchar> ::= "x" | "y" | "\\0041" | "''"
# §4.1.2.5 bit-string constants B'1001'.
<bconst> ::= "B'" <bit>* "'" | "b'" <bit>* "'"
# bit
<bit> ::= "0" | "1"
# §4.1.2.5 hexadecimal bit-string X'1FF'.
<xconst> ::= "X'" <hexdigit>* "'" | "x'" <hexdigit>* "'"
# hex digit (class 3 sample)
<hexdigit> ::= "0" | "7" | "a" | "F"
# §4.1.2.7 type 'string': the datetime types (class 3 sample).  Other type names here
# (int, text, boolean, a generic name, timestamp with time zone) are class 4.
<const_typename> ::= ("DATE" | "date" | "Date") | ("TIMESTAMP" | "timestamp" | "Timestamp") | ("INTERVAL" | "interval" | "Interval") | ("TIME" | "time" | "Time")

# --- Type names, §8 (Chapter 8 data types) and §4.2.9 ---
# Typename: a simple type with optional array bounds (§8.15.1 type[] ).
<typename> ::= <simple_typename> | <simple_typename> <array_bounds>
# §8.15.1 dimensions: [] repeated, or [n]; a sized bound followed by further bounds is class 4.
<array_bounds> ::= "[" <ows> "]" | "[" <ows> <int32_const> <ows> "]" | "[" <ows> "]" <array_bounds>
# Class 3 sample of Chapter 8 type names (§8.1 numeric, §8.3 character, §8.5 datetime, §8.6
# boolean), with type modifiers, plus a user-defined type name (an identifier, optionally
# schema-qualified).
<simple_typename> ::= ("INT" | "int" | "Int") | ("INTEGER" | "integer" | "Integer") | ("SMALLINT" | "smallint" | "Smallint") | ("BIGINT" | "bigint" | "Bigint") | ("REAL" | "real" | "Real") | ("DOUBLE" | "double" | "Double") <ws> ("PRECISION" | "precision" | "Precision") | ("NUMERIC" | "numeric" | "Numeric") | ("NUMERIC" | "numeric" | "Numeric") <ows> "(" <ows> <int32_const> <ows> ")" | ("NUMERIC" | "numeric" | "Numeric") <ows> "(" <ows> <int32_const> <ows> "," <ows> <int32_const> <ows> ")" | ("TEXT" | "text" | "Text") | ("VARCHAR" | "varchar" | "Varchar") | ("VARCHAR" | "varchar" | "Varchar") <ows> "(" <ows> <int32_const> <ows> ")" | ("CHARACTER" | "character" | "Character") <ws> ("VARYING" | "varying" | "Varying") | ("BOOLEAN" | "boolean" | "Boolean") | ("DATE" | "date" | "Date") | ("TIMESTAMP" | "timestamp" | "Timestamp") | ("TIMESTAMP" | "timestamp" | "Timestamp") <ws> ("WITH" | "with" | "With") <ws_nc> ("TIME" | "time" | "Time") <ws> ("ZONE" | "zone" | "Zone") | ("INTERVAL" | "interval" | "Interval") | <identifier> | <identifier> "." <identifier>

# --- Identifiers, §4.1.1 ---
# §4.1.1 identifier: unquoted or quoted ("delimited").
<col_id> ::= <col_id_rare>
# Second tier: a quoted identifier a quarter of the time (class 1).
<col_id_rare> ::= <quoted_identifier>
# §4.1.1 unquoted identifier: a letter or underscore, then letters, underscores, digits.
# Class 3 alphabet; length is free.
<identifier> ::= <ident_start> <ident_char>*
# Class 3: first character.
<ident_start> ::= "a" | "b" | "c" | "d" | "e" | "_"
# Class 3: subsequent characters.
<ident_char> ::= "a" | "b" | "c" | "d" | "e" | "_" | "1"
# §4.1.1 quoted identifier: any characters except the zero character, "" for a quote, non-empty.
<quoted_identifier> ::= "\"" <qchar>{3,7} "\""
# Class 3 alphabet of quoted-identifier characters.
<qchar> ::= "a" | "B" | " " | "\"\"" | "."

# --- Whitespace and comments, §4.1 and §4.1.5 ---
# §4.1: tokens are separated by whitespace (space, tab, newline) or comments; required between
# words.  Class 3 sample of separators.
<ws> ::= " " | <ws_1>
# Second tier (class 1: plain single space three quarters of the time).
<ws_1> ::= " " | <ws_2>
# Third tier: a separator other than one space, possibly repeated.
<ws_2> ::= "\n" | "\t" | "  " | <ws_unit> <ws>
# One separator unit: whitespace character, or a §4.1.5 comment (block or line) with a space
# on each side so it cannot glue onto an operator.
<ws_unit> ::= "\n" | "\t" | " /* c */ " | " -- c\n"
# Whitespace without comments, used after NOT, WITH and NULLS.  PostgreSQL's parser looks one
# token ahead after these (NOT_LA, WITH_LA, NULLS_LA); libpg_query 18 (pglast 8.4) then fails on a
# comment in between ("a NOT /* c */ IN (1)") where a PostgreSQL 14 server accepts it.  Oracle
# compatibility, see header.
<ws_nc> ::= " " | <ws_nc_1>
# Second tier.
<ws_nc_1> ::= " " | <ws_nc_unit> <ws_nc>
# Whitespace character only.
<ws_nc_unit> ::= " " | "\n" | "\t"
# Optional whitespace, used only next to the punctuation ( ) , ; (§4.1.4).
<ows> ::= "" | <ws>
