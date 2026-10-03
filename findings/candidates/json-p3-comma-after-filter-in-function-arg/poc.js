// json-p3 (all 2.x, and 1.x with a different error): inside a function call,
// a nested bracketed selection that starts with a filter selector cannot be
// followed by further selectors. The comma is taken as a function-argument
// separator. See poc.py for the same bug in jsonpath-rfc9535 (Python).
//
//   npm install && node poc.js
const r9 = require('jsonpath-rfc9535');
const engines = {
  'json-p3 2.3.0': (q, d) => require('json-p3_2_3_0').jsonpath.query(q, d).values().length,
  'json-p3 2.3.2 (latest)': (q, d) => require('json-p3').jsonpath.query(q, d).values().length,
  'jsonpath-rfc9535 1.3.0': (q, d) => r9.query(d, q).length,
};
const cases = [
  ['$[?count(@[?@, 1]) == 1]', [[1]]],                 // valid, 1
  ['$[?count(@[?@.a, ?@.b]) > 0]', [[{ a: 1 }]]],       // valid, 1
  ['$[?count(@[?@ == 1, ?@ == 2]) == 2]', [[1, 2]]],    // valid, 1
  ['$[?count(@[1, ?@]) == 1]', [[1]]],                 // control: filter last works
  ['$[?@[?@, 1]]', [[1], [0]]],                        // control: no function call works
];
for (const [q, d] of cases) {
  console.log(q);
  for (const [name, f] of Object.entries(engines)) {
    let out;
    try { out = `${f(q, d)} nodes`; } catch (e) { out = `${e.constructor.name}: ${e.message}`; }
    console.log(`   ${name.padEnd(24)} ${out}`);
  }
}
