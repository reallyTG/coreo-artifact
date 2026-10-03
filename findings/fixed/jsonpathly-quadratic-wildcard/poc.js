// jsonpathly 3.0.0: quadratic time in the number of results.
//
// `concatIndefiniteValuePaths` (dist/index.cjs) gathers results with
// `value: [...acc.value, current.value]`, which copies every result collected
// so far for each new one. Over n results that is O(n^2) copying, although
// each result is found in constant time. `paths` is copied the same way.
//
//   node poc.js            (after: npm install jsonpathly jsonpath-rfc9535)
//
// Expect jsonpathly's time to roughly quadruple each time n doubles, while
// jsonpath-rfc9535, an RFC 9535 implementation in the same language, stays
// linear.
const jsonpathly = require('jsonpathly');
const reference = require('jsonpath-rfc9535');

const QUERY = '$.a[*]';                 // '$..b' and '$.a[*].b' behave the same

const ms = (fn) => { const t = process.hrtime.bigint(); fn(); return Number(process.hrtime.bigint() - t) / 1e6; };

console.log(`query: ${QUERY}\n`);
console.log('elements   document   jsonpathly   growth   jsonpath-rfc9535');
let previous;
for (const n of [2500, 5000, 10000, 20000, 40000]) {
  const doc = { a: Array.from({ length: n }, (_, i) => ({ b: i })) };
  const kb = (JSON.stringify(doc).length / 1024).toFixed(0) + ' KB';
  const slow = ms(() => jsonpathly.query(doc, QUERY, { returnArray: true }));
  const fast = ms(() => reference.query(doc, QUERY));
  const growth = previous ? `x${(slow / previous).toFixed(1)}` : '';
  previous = slow;
  console.log(String(n).padStart(8), kb.padStart(10), `${slow.toFixed(0)} ms`.padStart(12),
              growth.padStart(8), `${fast.toFixed(1)} ms`.padStart(18));
}
