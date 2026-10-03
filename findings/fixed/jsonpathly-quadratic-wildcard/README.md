# jsonpathly: quadratic time in the number of results

- **Package**: [jsonpathly](https://github.com/atamano/jsonpathly) (npm,
  ~434k downloads/week). `$..b` is quadratic in every published version
  (1.0.0 through 3.0.0), `$.a[*]` from 1.5.0.
- **Class**: algorithmic complexity, O(n^2) in the size of the result set;
  a denial-of-service issue (CWE-407)
- **Status**: fixed upstream in 3.0.1 (2026-09-21), which appends results in place
  at both accumulation sites (`concatIndefiniteValuePaths` and `handleDotdot`).
- **Reproduce**: `npm install && node poc.js`

## What happens

A query whose result set is large takes time quadratic in the number of
results, while two other JSONPath libraries for JavaScript handle the same
input in linear time.

| Elements | Document | jsonpathly | Growth | jsonpath-rfc9535 |
|---|---|---|---|---|
| 2,500 | 26 KB | 8 ms | | 1.1 ms |
| 5,000 | 53 KB | 21 ms | x2.6 | 0.7 ms |
| 10,000 | 106 KB | 86 ms | x4.0 | 0.5 ms |
| 20,000 | 224 KB | 538 ms | x6.2 | 1.4 ms |
| 40,000 | 458 KB | 2,360 ms | x4.4 | 4.4 ms |

Each doubling of the element count multiplies the time by roughly 4, which is
the quadratic signature. Beyond the table: 100k elements take 22s and 200k take
83s. `$.a[*]`, `$..b` and `$.a[*].b` all show it.

Measured on Node v26.5.0, macOS 15 (Darwin 25.5.0), Apple silicon.

## Mechanism

`dist/index.cjs`, in `concatIndefiniteValuePaths`:

```js
payload.reduce((acc, current) => ({
  isIndefinite: true,
  value: [...acc.value, current.value],
  paths: [...acc.paths, current.paths],
}), { value: [], paths: [], isIndefinite: true })
```

`[...acc.value, current.value]` allocates a new array holding every result so
far and appends one element, so gathering n results copies 1+2+...+n elements.
`paths` is copied the same way, doubling the constant. The loop lower in the
same function accumulates with `paths2 = paths2.concat(result.paths)` per item,
which has the same shape.

## Suggested fix

Accumulate in place (`acc.value.push(current.value)`) or collect into an array
once and concatenate at the end. Both keep the result order.

## Impact

Libraries like this one are commonly applied to JSON arriving from outside the
process, in API gateways, config pipelines and log processing, where a 500 KB
document is unremarkable. There, one query costs seconds of CPU, so an attacker
who controls the document size, or an operator who grows it, can exhaust a
worker.
