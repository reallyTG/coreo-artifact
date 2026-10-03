// jsonpathly 3.0.x: a bracketed selection with more than one selector may only
// contain names, indexes and wildcards. A filter or slice selector anywhere in
// the list is a JSONPathSyntaxError. The first case is the RFC 9535 Table 12
// example `$.o[?@<3, ?@<3]`.
//
//   npm install && node poc.js
const r9 = require('jsonpath-rfc9535');
const engines = {
  'jsonpathly 3.0.0': (q, d) => require('jsonpathly_3_0_0').query(d, q, { returnArray: true }),
  'jsonpathly 3.0.1': (q, d) => require('jsonpathly').query(d, q, { returnArray: true }),
  'jsonpath-rfc9535 1.3.0 (reference)': (q, d) => r9.query(d, q),
};
const RFC_DOC = { a: [3, 5, 1, 2, 4, 6, { b: 'j' }, { b: 'k' }, { b: {} }, { b: 'kilo' }],
                  o: { p: 1, q: 2, r: 3, s: 5, t: { u: 6 } }, e: 'f' };
const cases = [
  ['$.o[?@<3, ?@<3]', RFC_DOC],          // RFC 9535 Table 12: 4 nodes
  ['$[?@.a, ?@.b]', [{ a: 1 }, { b: 2 }]], // 2
  ['$[?@, 1]', [1, 2]],                  // 3
  ['$[1, ?@]', [1, 2]],                  // 3
  ['$[0:1, 2]', [1, 2, 3]],              // 2
  ['$[1, 0:1]', [1, 2, 3]],              // 2
  ['$[0, 2]', [1, 2, 3]],                // control: 2
];
for (const [q, d] of cases) {
  console.log(q);
  for (const [name, f] of Object.entries(engines)) {
    let out;
    try { out = `${f(q, d).length} nodes`; } catch (e) { out = `${e.constructor.name}: ${e.message.slice(0, 70)}`; }
    console.log(`   ${name.padEnd(36)} ${out}`);
  }
}
