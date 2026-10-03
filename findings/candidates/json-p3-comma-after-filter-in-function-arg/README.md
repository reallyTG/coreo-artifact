# json-p3 and jsonpath-rfc9535 (Python): `count(@[?f, x])` rejected

- **Packages** (same author, jg-rp; same lexer design):
  - [json-p3](https://github.com/jg-rp/json-p3) 2.x through 2.3.2 (latest),
    npm, about 125,000 downloads/week. 1.0.0 fails too, with "unbalanced
    parentheses".
  - [jsonpath-rfc9535](https://github.com/jg-rp/python-jsonpath-rfc9535)
    1.0.0 (latest), PyPI, about 144,000 downloads/week.
  - python-jsonpath 2.2.1, by the same author with a different lexer, accepts
    these queries.
- **Class**: rejection of valid input (JSONPathSyntaxError).
- **Status**: not reported. No matching issue found on 2026-10-01. Related:
  python-jsonpath-rfc9535 [#13](https://github.com/jg-rp/python-jsonpath-rfc9535/issues/13)
  (closed), "Using a filter in a count() function results in 'unbalanced
  parentheses' error", fixed by #14 by adding the paren counting that this bug
  lives in. Both masters (`74ef87f9`, `e5ad5a82`) still have the code below.
- **Reproduce**: `npm install && node poc.js` and
  `python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py`
- **Provenance**: Surfaced by the jsonpath_js and jsonpath_py grammar-agreement
  probes on 2026-09-30 (generated inputs, then minimised by hand).

## What happens

| Query | RFC 9535 | json-p3 2.3.2 / jsonpath-rfc9535 (Py) 1.0.0 |
|---|---|---|
| `$[?count(@[?@, 1]) == 1]` on `[[1]]` | valid, 1 node | JSONPathSyntaxError: unexpected token in bracketed selection |
| `$[?count(@[?@.a, ?@.b]) > 0]` on `[[{"a":1}]]` | valid, 1 | JSONPathSyntaxError: unexpected filter selector token '?' |
| `$[?count(@[?@ == 1, ?@ == 2]) == 2]` on `[[1,2]]` | valid, 1 | JSONPathSyntaxError |
| `$[?count(@[1, ?@]) == 1]` (filter last) | valid, 1 | 1 |
| `$[?@[?@, 1]]` (no function call) | valid, 2 | 2 |

jsonpath-rfc9535 (JS) 1.3.0 and python-jsonpath 2.2.1 accept all rows and
agree on the results. Low real-world frequency: it needs a function argument
whose query has a bracket with a filter followed by another selector.

## Mechanism

Inside a filter the lexer decides what a comma means from one flag, "are we
inside any function call". json-p3 `src/path/lex.ts:468-474` (master):

```ts
case ",":
  l.emit(TokenKind.COMMA);
  // If we have unbalanced parens, we are inside a function call and a
  // comma separates arguments. Otherwise a comma separates selectors.
  if (l.funcCallStack.length) continue;
  l.filterLevel -= 1;
  return lexInsideBracketedSelection;
```

jsonpath-rfc9535 `jsonpath_rfc9535/lex.py:359-366` is the same logic with
`self.func_call_stack`. In `count(@[?@, 1])` the innermost open construct at
the comma is the nested filter's `[`, not the call's `(`, so the comma should
end the nested filter and return to the bracketed selection. Instead the lexer
stays in filter state, emits `1` as a filter-expression number, and the parser
rejects it. The question the lexer needs to answer is whether the function
call was opened inside the current filter, not whether any function call is
open.

## Specification

RFC 9535 Section 2.4 (function-argument = literal / filter-query / ...),
Section 2.3.5.1 (filter-query = rel-query / jsonpath-query;
rel-query = current-node-identifier segments), and Section 2.5.1.1
(bracketed-selection = "[" S selector *(S "," S selector) S "]", where a
selector may be a filter selector). Nothing restricts the selectors of a
nested query inside a function argument.

## Suggested fix

Record the function-call depth when each filter starts (push it on a stack in
the `?` branch, pop it when the filter ends), and treat a comma as an argument
separator only when `funcCallStack.length` is greater than the depth recorded
for the innermost filter. Not tested against the libraries' suites.
