# jsonpathly: `..[?filter]` and `..[a, b]` skip every array

- **Package**: [jsonpathly](https://github.com/atamano/jsonpathly) 3.0.0 and
  3.0.1 (latest), npm, about 727,000 downloads/week. The README claims RFC 9535
  compliance.
- **Class**: wrong answer, silently. No exception, results are missing.
- **Status**: not reported. No matching issue found on 2026-10-01 (15 issues in
  total, all read by title; #14 is related, see below).
- **Reproduce**: `npm install && node poc.js`
- **Provenance**: Surfaced by the jsonpath_js grammar-agreement probe on
  2026-09-30 (generated inputs, then minimised by hand).

## What happens

A descendant segment whose bracket holds a filter selector or a selector list
applies that bracket to objects only. Arrays reached by the descent are
skipped, so every match whose parent is an array is dropped:

| Query | Document | RFC 9535 result | jsonpathly 3.0.1 |
|---|---|---|---|
| `$..[?@]` | `[false]` | 1 node | 0 |
| `$..[?@]` | `{"a":[false,1]}` | 3 nodes | 1 |
| `$..[?@.isbn]` | the RFC's bookstore document | 2 books | 0 |
| `$..[?(@.price < 10)]` | the RFC's bookstore document | 2 books | 0 |
| `$.a..[0, 1]` | RFC 9535 Table 16 document | 4 nodes | 0 |
| `$..book[?@.isbn]` (control) | the RFC's bookstore document | 2 books | 2 |

The fifth row is an example printed in the RFC itself (Section 2.5.2.3,
Table 16). jsonpath-rfc9535 1.3.0 and json-p3 2.3.2 return the RFC result on
every row.

## Mechanism

`collectDotdot` in `src/handler/Handler.ts` (line 295 on master, `ed16c97f`;
`dist/index.cjs` around line 4436 in the published 3.0.1 package):

```ts
case 'bracketExpression': {
  if (isPlainObject(value) || (isArray(value) && treeValue.value.type === 'wildcard')) {
    appendAll(results, this.handleBracketExpressionContent(payload, treeValue.value));
  }
  break;
}
```

`bracketExpression` covers three node types from the grammar
(`src/parser/jsonpath.peggy`): `wildcard`, `filterExpression` and `unions`.
The guard lets arrays through only for `wildcard`. `handleBracketExpressionContent`
already handles arrays correctly for filters (it iterates array elements), so
the guard is simply too narrow.

## Versions

- 3.0.0 and 3.0.1: filter and selector-list cases both fail.
- 2.0.2 and 2.0.3 (the ANTLR-based line): `$..[?(@.a)]` on `[{"a":1}]` returns
  the correct 1, so the filter case is a regression introduced with the 3.0.0
  RFC 9535 rewrite. `$.a..[0,1]` already returned 0 in 2.0.x.

## Specification

RFC 9535 Section 2.5.2.2 (descendant segment semantics): the segment visits
the input node and each of its descendants, arrays included, and applies the
bracketed selection to each. Section 2.3.5.2: a filter selector iterates over
the elements of an array or the members of an object. Table 16 in Section
2.5.2.3 gives `$.a..[0, 1]` with four results.

## Related issue

[#14](https://github.com/atamano/jsonpathly/issues/14) (closed) reported
`$.paths..[?(@.tags ...)]` on an OpenAPI document returning nothing. Its
example descends through objects only, which the 3.0.0 rewrite handles; the
array case was not covered by that fix. Mention #14 when reporting.

## Suggested fix

Drop the type condition and let `handleBracketExpressionContent` decide:

```ts
case 'bracketExpression': {
  if (isPlainObject(value) || isArray(value)) {
    appendAll(results, this.handleBracketExpressionContent(payload, treeValue.value));
  }
  break;
}
```

Applying this change to a scratch copy of the 3.0.1 `dist/index.cjs` (line
4437) makes all five failing rows above return the RFC result, and `$..[*]`
and `$[0,1]` are unchanged.

Add `$.a..[0, 1]` and `$..[?@]` on `[false]` to the tests. Running the
jsonpath-compliance-test-suite would catch this class of issue.
