# jsonpath-rfc9535 (JS): unparenthesised && chains of three or more terms evaluate wrongly

**Package:** jsonpath-rfc9535 1.3.0 (npm, latest at 2026-10-01). Other versions not checked.
**Class:** correctness (silent wrong answer). **Reported:** no. **Duplicate search:** not yet done.

## Evidence

On `[{"x":1,"y":2,"z":3}]`:

| Query | RFC 9535 result | jsonpath-rfc9535 1.3.0 | json-p3 2.3.0 |
|---|---|---|---|
| `$[?@.x==1 && @.y==2 && @.z==9]` | `[]` | the element (wrong) | `[]` |
| `$[?@.x==1 && @.y==9 && @.z==3]` | `[]` | the element (wrong) | `[]` |
| `$[?@.x==1 && (@.y==2 && @.z==9)]` | `[]` | `[]` | `[]` |

RFC 9535 s2.3.5.1: `logical-and-expr = basic-expr *(S "&&" S basic-expr)`, so every
term must hold. The observed behaviour matches `a && (b || c ...)`: the chain
holds if the first term and any later term hold. Mechanism not yet located in source.

## Provenance

Found incidentally during triage on 2026-10-01 while building a scaling
series of `&&` chains for a jsonpath-plus lead from the jsonpath_plus_latest run
(rfc9535 returned hits=1 where every other engine returned 0). Reproduced
with `node poc.js`. Hand-constructed input, so not
loop-attributable, although the jsonpath_js grammar does generate such chains.

## Run

    npm install && node poc.js
