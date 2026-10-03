// json-p3 2.3.1: RangeError on a large result set.
//
// `ChildSegment.resolve` and `DescendantSegment.resolve` (dist/json-p3.cjs.js)
// both collect with `rv.push(...selector.resolve(node))`. The spread passes
// every result as a separate argument, and an argument list lives on the call
// stack, so one selector returning enough nodes from one node exceeds the
// engine's limit and throws `RangeError: Maximum call stack size exceeded`.
// The generator paths in the same classes (`lazyResolve`, which use `yield*`)
// are not affected, so `jsonpath.lazyQuery` returns every result.
//
//   node poc.js            (after: npm install)
//
// 100k elements succeed and 130k throw, so this is a cliff rather than a slope.
// `$..b` over the same documents does not throw: each `resolve` there returns
// at most one node, so the limit is on one selector's output from one node,
// not on the total result count.
const { jsonpath } = require('json-p3');
const reference = require('jsonpath-rfc9535');

const QUERIES = [
  '$.a[*]', // ChildSegment.resolve
  '$..[*]', // DescendantSegment.resolve
  '$..b', // descendant, one node per resolve: not affected
];

function run(fn) {
  try {
    return `${fn()} results`;
  } catch (e) {
    return `${e.constructor.name}: ${e.message}`;
  }
}

for (const query of QUERIES) {
  console.log(`query: ${query}`);
  console.log('elements   document   json-p3 query   json-p3 lazyQuery   jsonpath-rfc9535');
  for (const n of [100000, 130000, 200000]) {
    const doc = { a: Array.from({ length: n }, (_, i) => ({ b: i })) };
    const mb = (JSON.stringify(doc).length / 1048576).toFixed(1) + ' MB';
    const eager = run(() => jsonpath.query(query, doc).values().length);
    const lazy = run(() => Array.from(jsonpath.lazyQuery(query, doc)).length);
    const ok = run(() => reference.query(doc, query).length);
    console.log(`${String(n).padStart(8)} ${mb.padStart(10)}   ${eager}   ${lazy}   ${ok}`);
  }
  console.log();
}
