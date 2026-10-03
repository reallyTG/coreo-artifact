// json-p3 >= 1.3.4: every number literal that starts with "0" and is longer
// than one character is a syntax error, including valid ones such as 0.5 and
// 0e1. The check meant to reject leading zeros (01, 00) also rejects a zero
// integer part.
//
//   npm install && node poc.js
const r9 = require('jsonpath-rfc9535');
const engines = {
  'json-p3 1.3.3': (q, d) => require('json-p3_1_3_3').jsonpath.query(q, d).values().length,
  'json-p3 2.3.0': (q, d) => require('json-p3_2_3_0').jsonpath.query(q, d).values().length,
  'json-p3 2.3.2 (latest)': (q, d) => require('json-p3').jsonpath.query(q, d).values().length,
  'jsonpath-rfc9535 1.3.0': (q, d) => r9.query(d, q).length,
};
const cases = [
  ['$[?@.price < 0.5]', [{ price: 0.25 }, { price: 3 }]],  // valid, 1
  ['$[?@.a == 0.25]', [{ a: 0.25 }]],                      // valid, 1
  ['$[?@.a == 0e1]', [{ a: 0 }]],                          // valid, 1
  ['$[?@.a == 0e-1]', [{ a: 0 }]],                         // valid, 1
  ['$[?@.a == -0.5]', [{ a: -0.5 }]],                      // control: works
  ['$[?@.a == 01]', [{ a: 1 }]],                           // invalid: must be rejected
  ['$[?@.a == -01]', [{ a: -1 }]],                         // invalid: must be rejected
];
for (const [q, d] of cases) {
  console.log(q);
  for (const [name, f] of Object.entries(engines)) {
    let out;
    try { out = `${f(q, d)} nodes`; } catch (e) { out = `${e.constructor.name}: ${e.message}`; }
    console.log(`   ${name.padEnd(24)} ${out}`);
  }
}
