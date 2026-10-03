# pgsql-ast-parser: JSON error on valid escape strings (`E'\''`, `E'\x41'`)

- **Package**: [pgsql-ast-parser](https://github.com/oguimbal/pgsql-ast-parser) 12.0.2, the latest release
  (npm, about 1.3M downloads/week; the parser inside pg-mem, 0.6M/week)
- **Class**: internal error on valid input. The exception is a JSON parse error, not a SQL syntax error
- **Status**: candidate, not reported. No matching issue or PR found on 2026-10-01 (searched "escape", "E'", "JSON", "backslash", "escape string").
- **Fixed in latest**: no. 12.0.2 is the latest release; the lexer rule is unchanged on `master` and in the open PR #174.
- **Reproduce**: `npm install && node poc.js`

## What happens

```
SELECT E'\''       PostgreSQL: "'"   pgsql-ast-parser: Error: Bad escaped character in JSON at position 2
SELECT E'\x41'     PostgreSQL: "A"   pgsql-ast-parser: Error: Bad escaped character in JSON at position 2
SELECT E'\101'     PostgreSQL: "A"   pgsql-ast-parser: Error: Bad escaped character in JSON at position 2
SELECT E'\uXXXX'   PostgreSQL: char  pgsql-ast-parser: Error: Bad Unicode escape in JSON at position 3
SELECT E'\q'       PostgreSQL: "q"   pgsql-ast-parser: Error: Bad escaped character in JSON at position 2
SELECT E'\n'       PostgreSQL: "\n"  pgsql-ast-parser: "\n"   (works: JSON defines \n too)
```

The reference column is libpg-query 18.1.5 (PostgreSQL's own parser compiled to WASM); pglast 8.4 also accepts all
five, and sql-parser-cst 0.42.1 and sql-formatter 15.8.2 accept them. pg-mem 3.0.14, which uses this parser, fails
`SELECT E'\x41' AS s` with the same JSON message.

## Mechanism

`src/lexer.ts:36-44` (compiled: `index.js:137`):

```ts
eString: {
    match: /\b(?:e|E)'(?:[^'\\]|[\r\n\s]|(?:\\\s)|(?:\\\n)|(?:\\.)|(?:\'\'))+'/,
    value: x => x.substring(2, x.length - 1)
            .replace(/''/g, '\'')
            .replace(/\\([\s\n])/g, (_, x) => x)
            .replace(/\\./g, m => JSON.parse('"' + m + '"')),
},
```

The token regex accepts a backslash followed by any character, and the value function decodes each two-character
escape by handing it to `JSON.parse`. JSON defines only `\" \\ \/ \b \f \n \r \t` and `\u` with four hex digits.
Every other escape that PostgreSQL defines, and the "any other character is taken literally" rule, reaches
`JSON.parse` and throws. The `\u` case fails even with valid hex digits because `\\.` passes only two characters
(`\u`) to `JSON.parse`, not six.

The escaped quote `\'` is the most common of these in practice: it is how many client libraries and hand-written
SQL embed a quote in an E-string.

## Specification

PostgreSQL 18 documentation, section 4.1.2.2 "String Constants With C-Style Escapes", Table 4.1: `\b`, `\f`, `\n`,
`\r`, `\t`, octal `\o`, `\oo`, `\ooo`, hex `\xh`, `\xhh`, and 16- and 32-bit Unicode escapes (`\uxxxx`,
`\Uxxxxxxxx`). "Any other character following a backslash is taken literally. Thus, to include a backslash
character, write two backslashes (`\\`). Also, a single quote can be included in an escape string by writing `\'`,
in addition to the normal way of `''`."

## Suggested fix

Replace the `JSON.parse` call with a decoder for PostgreSQL's escape set, and let the regex consume the multi-character
escapes whole:

```js
.replace(/\\(?:x[0-9a-fA-F]{1,2}|[0-7]{1,3}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|[^])/g, m => {
    const c = m[1];
    const map = { b: '\b', f: '\f', n: '\n', r: '\r', t: '\t' };
    if (c in map) return map[c];
    if (m.length > 2 && (c === 'x' || c === 'u' || c === 'U')) return String.fromCodePoint(parseInt(m.slice(2), 16));
    if (/[0-7]/.test(c)) return String.fromCodePoint(parseInt(m.slice(1), 8));
    return c;   // any other character is taken literally, including ' and \
})
```

Applied to a scratch copy of 12.0.2's `index.js`, this decodes all six cases above to PostgreSQL's values and leaves
`E'\\'` and `E'a\nb'` unchanged. It does not add surrogate-pair or `standard_conforming_strings` handling.

## Provenance

Surfaced by the `sql_js` grammar-agreement probe on 2026-09-30 (generated inputs, then minimised by hand).
Triage and mechanism: T1, 2026-10-01.
