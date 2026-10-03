// jsonpathly 3.0.0 / 3.0.1: a descendant segment whose bracket holds a filter
// or a selector list (`..[?...]`, `..[0, 1]`) never applies that bracket to
// arrays, so every match that lives inside an array is dropped. The last case
// is the RFC 9535 Table 16 example `$.a..[0, 1]`.
//
//   npm install && node poc.js
const r9 = require('jsonpath-rfc9535');
const engines = {
  'jsonpathly 3.0.0': (q, d) => require('jsonpathly_3_0_0').query(d, q, { returnArray: true }),
  'jsonpathly 3.0.1': (q, d) => require('jsonpathly').query(d, q, { returnArray: true }),
  'jsonpath-rfc9535 1.3.0 (reference)': (q, d) => r9.query(d, q),
};

const RFC_DOC = { o: { j: 1, k: 2 }, a: [5, 3, [{ j: 4 }, { k: 6 }]] };
const BOOKS = { store: { book: [
  { title: 'Sayings of the Century', price: 8.95 },
  { title: 'Sword of Honour', price: 12.99 },
  { title: 'Moby Dick', isbn: '0-553-21311-3', price: 8.99 },
  { title: 'The Lord of the Rings', isbn: '0-395-19395-8', price: 22.99 },
], bicycle: { color: 'red', price: 399 } } };

const cases = [
  ['$..[?@]', [false]],                  // RFC: 1 node (false exists)
  ['$..[?@]', { a: [false, 1] }],        // RFC: 3 nodes
  ['$..[?@.isbn]', BOOKS],               // RFC: the two books with an isbn
  ['$..[?(@.price < 10)]', BOOKS],       // RFC: 2 (parenthesised form too)
  ['$.a..[0, 1]', RFC_DOC],              // RFC 9535 Table 16: 4 nodes
  ['$..book[?@.isbn]', BOOKS],           // control: RFC Table 3 form works
];

for (const [q, d] of cases) {
  console.log(`${q}   on ${JSON.stringify(d).slice(0, 60)}`);
  for (const [name, f] of Object.entries(engines)) {
    let out;
    try { out = `${f(q, d).length} nodes`; } catch (e) { out = `${e.constructor.name}: ${e.message}`; }
    console.log(`   ${name.padEnd(36)} ${out}`);
  }
}
