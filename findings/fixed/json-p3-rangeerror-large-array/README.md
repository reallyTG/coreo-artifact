# json-p3: RangeError on a large result set

- **Package**: [json-p3](https://github.com/jg-rp/json-p3) 2.3.0 and 2.3.1 (npm)
- **Class**: unhandled exception on a valid query (robustness), not a slowdown.
  The error is catchable and costs no more than the input does, so this is a
  robustness bug and not a denial of service.
- **Status**: fixed upstream in 2.3.2 (2026-09-22).
- **Reproduce**: `npm install && node poc.js`

## What happens

A query throws instead of returning when a single selector selects about
130,000 or more nodes from a single node:

```
query: $.a[*]
elements   document   json-p3 query                                  json-p3 lazyQuery   jsonpath-rfc9535
  100000     1.1 MB   100000 results                                 100000 results      100000 results
  130000     1.5 MB   RangeError: Maximum call stack size exceeded   130000 results      130000 results
  200000     2.4 MB   RangeError: Maximum call stack size exceeded   200000 results      200000 results

query: $..[*]
  100000     1.1 MB   200001 results                                 200001 results      200001 results
  130000     1.5 MB   RangeError: Maximum call stack size exceeded   260001 results      260001 results
  200000     2.4 MB   RangeError: Maximum call stack size exceeded   400001 results      400001 results

query: $..b
  100000     1.1 MB   100000 results                                 100000 results      100000 results
  130000     1.5 MB   130000 results                                 130000 results      130000 results
  200000     2.4 MB   200000 results                                 200000 results      200000 results
```

100k succeeds and 130k throws, so there is a cliff rather than a gradient. The
exact threshold depends on the JavaScript engine's argument limit.

`$..b` returns 200,000 results without error because each `resolve` call there
returns at most one node. The limit is on what one selector returns from one
node, not on the total result count.

Measured on json-p3 2.3.1, Node v26.5.0, macOS 15 (Darwin 25.5.0), Apple
silicon. 2.3.0 behaves the same.

## Mechanism

Two segment classes collect results with a spread into `push`
(`src/path/segments.ts` lines 44 and 88 on `main`; `dist/json-p3.cjs.js` in the
published package):

```js
// ChildSegment.resolve
rv.push(...selector.resolve(node));

// DescendantSegment.resolve
rv.push(...selector.resolve(_node));
```

The spread passes each result as its own argument to `push`, and an argument
list is built on the call stack, so a large enough array from one `resolve`
call exceeds the engine's limit. `$.a[*]` reaches the first site and `$..[*]`,
which has only a descendant segment, reaches the second. The `lazyResolve`
methods in both classes use `yield*` and are not affected, which is why
`jsonpath.lazyQuery` returns every result.

## Suggested fix

Append with a loop at both sites:

```js
for (const n of selector.resolve(node)) rv.push(n);
```

Verified by patching the published `dist/json-p3.cjs.js` of 2.3.1 with exactly
this at both sites: all nine cases in the PoC then return the same counts as
jsonpath-rfc9535. On 2.3.1 and earlier, `jsonpath.lazyQuery` is a workaround.

## Impact

A caller handling a large document gets an exception that reads as a stack
overflow rather than a size limit, which is hard to attribute and, unlike the
library's own `JSONPathRecursionLimitError`, is not a documented limit. An
input roughly 1.5 MB in size is enough.

It is not a denial of service in the usual sense. The `RangeError` is thrown
synchronously from `query()` and can be caught, the process survives, and the
library fails fast rather than spending time out of proportion to the input.
