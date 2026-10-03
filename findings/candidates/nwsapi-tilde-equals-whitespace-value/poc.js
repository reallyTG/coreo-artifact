// nwsapi >= 2.2.12: an attribute selector [att~="val"] whose value contains a
// space is dropped from the compiled selector instead of matching nothing.
// `p[title~="x y"]` therefore behaves like `p`, and `[title~="x y"]` like `*`.
// Selectors 4 §6.1: "If 'val' contains whitespace, it will never represent
// anything." nwsapi 2.2.9 and dom-selector (jsdom 30) return 0.
//
//   npm install && node poc.js
const { JSDOM } = require('jsdom');
const { DOMSelector } = require('@asamuzakjp/dom-selector');

const HTML = '<p title="x y">a</p><p title="  ">b</p><p>c</p><div class="a b">d</div>';
const SELECTORS = [
  'p[title~="x y"]',          // expected 0
  '[title~=" "]',             // expected 0
  'div[class~="a b"]',        // expected 0
  'p:not([title~="x y"])',    // expected 3 (the negation of nothing)
  'p[title~=""]',             // expected 0 (empty value; separate, smaller bug)
];

const ref = new JSDOM(HTML);
const ds = new DOMSelector(ref.window);
console.log(`document: ${HTML}\n`);
console.log('selector'.padEnd(26) + 'dom-selector  ' + ['2.2.9', '2.2.12', '2.2.24', '2.2.28'].map(v => ('nwsapi ' + v).padEnd(14)).join(''));
for (const sel of SELECTORS) {
  const row = [String(ds.querySelectorAll(sel, ref.window.document).length).padEnd(14)];
  for (const v of ['2.2.9', '2.2.12', '2.2.24', '2.2.28']) {
    const doc = new JSDOM(HTML).window.document;
    const nw = require('nw' + v.replace(/\./g, '_'))({ document: doc });
    let r; try { r = String(nw.select(sel, doc).length); } catch (e) { r = e.constructor.name; }
    row.push(r.padEnd(14));
  }
  console.log(sel.padEnd(26) + row.join(''));
}
