# jsonpathly: filter and slice selectors rejected inside a selector list

- **Package**: [jsonpathly](https://github.com/atamano/jsonpathly) 3.0.0 and
  3.0.1 (latest); 2.0.2 also rejects a list of two filters. npm, about 727,000
  downloads/week. The README claims RFC 9535 compliance and lists
  `[<expr>, <expr>]` as "Union - multiple selectors" without restriction.
- **Class**: rejection of valid input (JSONPathSyntaxError).
- **Status**: not reported. No matching issue found on 2026-10-01 (all 15
  issues read by title).
- **Reproduce**: `npm install && node poc.js`
- **Provenance**: Surfaced by the jsonpath_js grammar-agreement probe on
  2026-09-30 (generated inputs, then minimised by hand). The probe first saw it
  as `$[?count(@[?@,1])==1]`; the function argument turned out to be
  irrelevant for jsonpathly.

## What happens

| Query | RFC 9535 result | jsonpathly 3.0.1 |
|---|---|---|
| `$.o[?@<3, ?@<3]` (RFC Table 12 document) | 4 nodes | JSONPathSyntaxError |
| `$[?@.a, ?@.b]` on `[{"a":1},{"b":2}]` | 2 | JSONPathSyntaxError |
| `$[?@, 1]` on `[1,2]` | 3 | JSONPathSyntaxError |
| `$[1, ?@]` on `[1,2]` | 3 | JSONPathSyntaxError |
| `$[0:1, 2]` on `[1,2,3]` | 2 | JSONPathSyntaxError |
| `$[0, 2]` (control) | 2 | 2 |

The first row is an example printed in RFC 9535 (Section 2.3.5.3, Table 12).
jsonpath-rfc9535 1.3.0 and json-p3 2.3.2 accept all of them.

## Mechanism

`src/parser/jsonpath.peggy` on master (`ed16c97f`):

```
bracketContent
  = filterExpression
  / slices
  / selectorList
  ...
selectorList
  = head:selector tail:(_ COMMA _ selector)+ { ... type: 'unions' ... }
selector
  = STAR / NUMBER / STRING / identifier
```

A filter or slice is only accepted as the whole bracket content. The
`selector` rule used inside lists has no filter or slice alternative, and the
comment above it ("Selector list allows mixed types (strings, numbers,
wildcards)") shows the omission is structural, not a precedence accident.

## Specification

RFC 9535 Section 2.5.1.1:
`bracketed-selection = "[" S selector *(S "," S selector) S "]"`, and Section
2.3: `selector = name-selector / wildcard-selector / slice-selector /
index-selector / filter-selector`. The paragraph after Table 12 discusses the
two-filter example explicitly.

## Suggested fix

Add `filterExpression`-without-brackets and `slices` alternatives to
`selector`, and extend `handleUnions` to evaluate them per element. The slice
and filter evaluation already exists in `handleBracketExpressionContent`, so
`handleUnions` can delegate each list member to it and concatenate in order.
This is a feature-sized change rather than a one-liner; the report should say
so and offer the RFC example as the test.

## Classification note

This could be read as undocumented non-support. It is filed as a candidate
because the README asserts RFC 9535 compliance and documents unions without
restriction, and because the RFC's own example fails.
