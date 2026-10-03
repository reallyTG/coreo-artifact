// jsonpath-rfc9535 (JS) 1.3.0: a chain of three or more && terms without
// parentheses evaluates wrongly. json-p3 is the RFC-conformant sibling.
const rfc = require("jsonpath-rfc9535");
const p3 = require("json-p3");
const doc = [{ x: 1, y: 2, z: 3 }];
for (const q of [
  "$[?@.x==1 && @.y==2 && @.z==9]",   // RFC: [] (z is 3)
  "$[?@.x==1 && @.y==9 && @.z==3]",   // RFC: [] (y is 2)
  "$[?@.x==1 && (@.y==2 && @.z==9)]", // RFC: [] (parenthesised control)
]) {
  console.log(q.padEnd(36),
    "rfc9535:", JSON.stringify(rfc.query(doc, q)).padEnd(24),
    "json-p3:", JSON.stringify(p3.jsonpath.query(q, doc).values()));
}
