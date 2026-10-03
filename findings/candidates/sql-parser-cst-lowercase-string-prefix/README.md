# sql-parser-cst: lowercase `e'...'` rejected and `u&'...'` misparsed (PostgreSQL dialect)

- **Package**: [sql-parser-cst](https://github.com/nene/sql-parser-cst) 0.42.1, the latest release
  (npm, about 91k downloads/week; the parser behind prettier-plugin-sql-cst, 46k/week)
- **Class**: rejection of valid input (`e'x'`) and a silently wrong syntax tree (`u&'x'`)
- **Dialect**: `{ dialect: "postgresql" }`, which the README marks "experimental (version 16)". The subject's runner
  (`subjects/sql_js/node_runner.js`) uses exactly this option.
- **Status**: candidate, not reported. No matching issue on 2026-10-01. The PostgreSQL tracking issue
  [#42](https://github.com/nene/sql-parser-cst/issues/42) ticks "C-style escapes: `E'foo\nbar'`" and Unicode strings
  as done, with no mention of case.
- **Fixed in latest**: no. The rules are unchanged on `master` (checked `src/parser.pegjs` at the 2026-08-23 head).
- **Reproduce**: `npm install && node poc.js`

## What happens

```
SELECT E'x'    PostgreSQL: string 'x'   sql-parser-cst: string_literal E'x'
SELECT e'x'    PostgreSQL: string 'x'   sql-parser-cst: Syntax Error: Unexpected end of input
SELECT U&'x'   PostgreSQL: string 'x'   sql-parser-cst: string_literal U&'x'
SELECT u&'x'   PostgreSQL: string 'x'   sql-parser-cst: binary_expr  u & 'x'   (identifier u, bitwise AND, string)
SELECT b'1'    accepted by both (bit-string prefix is case-insensitive in sql-parser-cst)
SELECT x'1F'   accepted by both
```

The reference is libpg-query 18.1.5; pglast 8.4 agrees. pgsql-ast-parser 12.0.2 and sql-formatter 15.8.2 accept
`e'x'`.

The `u&'x'` case is the worse one: the parse succeeds, and a formatter or linter built on the tree sees a column
reference `u` and an `&` operator that are not in the query.

## Mechanism

Upstream `src/parser.pegjs` (master; line numbers from the 2026-08-23 head):

```
9107  string_literal_e_single_quoted_bs        = "E"  str:string_literal_single_quoted_qq_bs
9116  string_literal_unicode_single_quoted_qq  = "U&" str:string_literal_single_quoted_qq
9125  string_literal_unicode_double_quoted_qq  = "U&" str:string_literal_double_quoted_qq
```

Peggy string literals are case-sensitive unless suffixed with `i`. The neighbouring bit-string and hex-string rules
use `"B"i` (line 9301) and `"X"i` (line 9451), which is why `b'1'` works. With `"E"` failing on `e`, the lexer
reads `e` as an identifier followed by a string literal, which is a syntax error; with `"U&"` failing on `u&`, it
reads `u`, the operator `&`, and a string, which is valid.

## Specification

PostgreSQL 18 documentation:
- Section 4.1.2.2: "An escape string constant is specified by writing the letter E (upper or lower case) just before
  the opening single quote".
- Section 4.1.2.3: "a Unicode escape string constant starts with U& (upper or lower case letter U followed by
  ampersand) immediately before the opening quote". Section 4.1.1 says the same for `U&"..."` identifiers.

## Suggested fix

Change the three literals to `"E"i` and `"U&"i`, as the `B` and `X` rules already are. The quoted-identifier form
has the same defect: `SELECT u&"x"` parses as `u & "x"` (column `u` AND column `x`) where `U&"x"` is the identifier
`x`; line 9125 covers the double-quoted string form, and the identifier rule should get the same `i`.

## Smaller gaps from the same probe (not in the title; report only if convenient)

| Statement | Cause | Upstream |
|---|---|---|
| `SELECT count(ALL a) FROM t` | `func_args` (parser.pegjs:8373) accepts `DISTINCT` but not `ALL`; PostgreSQL 18 section 4.2.7 allows `aggregate_name (ALL expression ...)` | none found; related open issue [#75](https://github.com/nene/sql-parser-cst/issues/75) (aggregate expressions) |
| `SELECT '10.0.0.0/8'::inet >> ANY (ARRAY[...])`, also `<<=` | `>>` and `<<` are parsed in `bit_shift_expr` (line 7949), which takes no quantifier; PostgreSQL 18 section 9.25 allows `expression operator ANY (array)` for any boolean operator, and `>>`, `<<=` are the inet containment operators | sibling of [#79](https://github.com/nene/sql-parser-cst/issues/79) (`^@ ANY`, closed as fixed for that operator only) |
| `SELECT int '1'`, `SELECT text 'a'` | typed literals only for date/time types | known: unticked item "`type 'string'`" in [#49](https://github.com/nene/sql-parser-cst/issues/49) |
| `SELECT a = ANY (b) BETWEEN 1 AND 2` | quantifier result cannot be a BETWEEN operand | known: unticked "100% correct operator precedence" in #49 |

## Provenance

Surfaced by the `sql_js` grammar-agreement probe on 2026-09-30 (generated inputs, then minimised by hand). The probe
produced `e'x'`; the `u&'x'` misparse was found during triage on 2026-10-01 by reading the neighbouring rule.
