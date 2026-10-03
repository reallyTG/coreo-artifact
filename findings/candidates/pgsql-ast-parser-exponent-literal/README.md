# pgsql-ast-parser: `SELECT 1e3` parses as `SELECT 1 AS e3`

- **Package**: [pgsql-ast-parser](https://github.com/oguimbal/pgsql-ast-parser) 12.0.2, the latest release
  (npm, about 1.3M downloads/week; the parser inside pg-mem, 0.6M/week)
- **Class**: silently wrong parse tree (select list), and rejection of valid input (everywhere else)
- **Status**: candidate, not reported. No issue or PR found on 2026-10-01 for exponent or scientific-notation
  literals (searched "exponent", "scientific notation", "1e", "1e10", "float", "numeric literal"). Open PR
  [#174](https://github.com/oguimbal/pgsql-ast-parser/pull/174) adds exact-digit `valueText` to numeric nodes but
  does not change the int/float regexes, so it does not fix this.
- **Fixed in latest**: no.
- **Reproduce**: `npm install && node poc.js`

## What happens

```
SELECT 1e3                     PostgreSQL: 1000 (float const)   pgsql-ast-parser: 1 AS e3
SELECT 2.5e3, 7                PostgreSQL: 2500, 7              pgsql-ast-parser: 2.5 AS e3, 7
SELECT 1e3 AS n                PostgreSQL: accepted             pgsql-ast-parser: Syntax error at col 12
SELECT 1e3 ^ 2                 PostgreSQL: accepted             pgsql-ast-parser: Syntax error at col 12
SELECT 97e19::int              PostgreSQL: accepted             pgsql-ast-parser: Syntax error at col 13
SELECT x FROM t WHERE x > 1e3  PostgreSQL: accepted             pgsql-ast-parser: Unexpected end of input
SELECT 2.5E-3                  PostgreSQL: accepted             pgsql-ast-parser: Syntax error at col 12
```

The reference is libpg-query 18.1.5, which reads `SELECT 1e3` as `A_Const{fval: "1e3"}` with no alias; pglast 8.4
agrees, and a PostgreSQL 14.19 server returns `1000` in a column named `?column?`. sql-parser-cst 0.42.1 and
sql-formatter 15.8.2 accept all seven.

The first two rows are the serious ones: the parse succeeds, the AST holds the integer `1` with an alias `e3`, and
`toSql` re-prints it as `SELECT (1) AS e3`. Downstream, pg-mem 3.0.14 answers `SELECT 1e3` with `[{"e3": 1}]`
where PostgreSQL answers `1000`, so a test suite running against pg-mem gets a different value from production with
no error.

## Mechanism

`src/lexer.ts:54-55` (compiled: `index.js:149-150`):

```ts
int: /\-?\d+(?![\.\d])/,
float: /\-?(?:(?:\d*\.\d+)|(?:\d+\.\d*))/,
```

Neither rule has an exponent part. `1e3` therefore lexes as `int(1)` then `word(e3)` (the `word` rule at
`src/lexer.ts:20` explicitly allows a leading `e` not followed by `'`). In a select list, `<expr> <word>` is an
implicit alias, so the statement parses; in any other position the stray word is a syntax error.

## Specification

PostgreSQL 18 documentation, section 4.1.2.6 "Numeric Constants": the accepted forms include `digits e[+-]digits`
and `digits.[digits][e[+-]digits]`, with examples `5e2` and `1.925e-3`. "At least one digit must be before or after
the decimal point, if one is used. At least one digit must follow the exponent marker (e), if one is present."
The exponent form has been part of the PostgreSQL lexer (`real` in `scan.l`) in every release.

## Related: `1_000`

`SELECT 1_000` parses as `1 AS _000` by the same route. That matches PostgreSQL 14 and earlier (checked on a 14.19
server), but PostgreSQL 15 rejects trailing junk after a numeric literal and PostgreSQL 16 reads `1_000` as
`1000` (section 4.1.2.6, underscores as digit separators). This one is a version difference rather than a bug, but
the same lexer change could cover it.

## Suggested fix

```ts
int:   /\-?\d+(?![\.\deE])/,
float: /\-?(?:(?:(?:\d+\.?\d*)|(?:\.\d+))[eE][+\-]?\d+|(?:\d*\.\d+)|(?:\d+\.\d*))/,
```

Applied to a scratch copy of 12.0.2's `index.js`, this parses all seven statements above to numeric nodes with
PostgreSQL's values (`1e3` gives `{type: "numeric", value: 1000}`), and `SELECT 42`, `SELECT 1.5`, `SELECT 3.` and
`SELECT .5e1` still parse as before or correctly. A regression test should also pin `SELECT 1 e3`, which is a
genuine alias and must stay one.

## Provenance

Surfaced by the `sql_js` grammar-agreement probe on 2026-09-30 (generated inputs, then minimised by hand). The
generated statements were rejections (`1e3 ^ 2`, `97e19::int`); the silent misparse in a select list was found
during triage on 2026-10-01 by reading the lexer.
