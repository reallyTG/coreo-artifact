# pgsql-ast-parser: "Ambiguous SQL syntax" on valid PostgreSQL

- **Package**: [pgsql-ast-parser](https://github.com/oguimbal/pgsql-ast-parser) 12.0.2 (npm, ~811k downloads/week)
- **Class**: parse failure on valid input (its nearley grammar yields more than one parse)
- **Status**: not reported. The library's own error text asks for this report:
  "Ambiguous SQL syntax: Please file an issue stating the request that has failed".
- **Reproduce**: `npm install && node poc.js`

## What happens

```
SELECT FROM t JOIN u ON ('x') AND ad.a IS NULL AND (SELECT FROM de JOIN a ON
(SELECT FROM a JOIN e ON (NOT f(a)) GROUP BY g ORDER BY dc DESC, c ASC,
c.x DESC, e.y DESC) GROUP BY ec, ac)

PostgreSQL grammar (libpg-query)  accepted
sql-parser-cst                    accepted
sql-formatter                     accepted
pgsql-ast-parser                  Ambiguous SQL syntax: Please file an issue...
```

The statement is valid: libpg-query is PostgreSQL's own grammar compiled to
WASM, and it parses it. Two other JavaScript SQL parsers accept it as well.

## How often

In one Coreografa campaign over generated PostgreSQL SELECT statements, 201 of
638 statements (32%) hit this, at a median size of 2.9 KB. The smallest was 812
bytes before reduction; the case above is 185 bytes.

The ingredients, from the reduction: nested subqueries used as predicates
inside `ON`, a parenthesised `NOT`, and `GROUP BY` and `ORDER BY` inside the
nested subquery. Simple versions of any one of them parse fine, so it is the
combination rather than a single construct.

## Reduction method

Delta-debugging over tokens, with the predicate "pgsql-ast-parser reports
Ambiguous AND libpg-query accepts the statement". The second half matters: an
earlier reduction that used sql-parser-cst as the validity oracle drifted into
statements that only a lenient parser accepts, since sql-parser-cst also
accepts things PostgreSQL rejects.

## Impact

A caller gets an exception on input the database itself accepts, so a tool
built on this parser rejects queries that run fine. The `ORDER BY` and
`GROUP BY` lists in the reduced case suggest the ambiguity grows with clause
size, which matches it appearing on a third of a corpus whose statements
average 2.9 KB.

## Provenance

Loop-found. The runner's failure ledger recorded every parse failure during the
`sql_js` campaign (638 statements over three parsers, 8 hours); all 690 failure
rows were this one error, all from pgsql-ast-parser. Reduction was automatic,
with the oracles above.
