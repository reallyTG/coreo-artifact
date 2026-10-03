// css-select 7.0.0 implements :read-only as "a text control with a readonly
// attribute" and :read-write as its complement among text controls. HTML
// defines :read-write as mutable text controls, non-readonly textareas and
// editable content, and :read-only as every other HTML element. The text
// control test also requires an explicit type attribute, so a plain <input>
// (whose missing type means Text) is neither.
//
//   npm install && node poc.js
const { parseDocument } = require('htmlparser2');
const CSSselect = require('css-select');

const HTML = '<html><body><p>a</p><input id="i1"><input id="i2" readonly>' +
  '<input id="i3" type="text" readonly><input id="i4" type="checkbox">' +
  '<textarea></textarea><div contenteditable>e</div></body></html>';
// Chromium 151, document.querySelectorAll on the same HTML (dom-selector 9.1.4
// and nwsapi 2.2.28 agree on every row):
const CHROMIUM = [
  ['input:read-write', 1, 'i1: untyped input is a mutable Text control'],
  ['input:read-only', 3, 'i2, i3, i4'],
  ['div:read-write', 1, 'contenteditable host'],
  ['p:read-only', 1, 'any non-editable element'],
  [':read-only', 7, 'html, head, body, p, i2, i3, i4'],
  [':read-write', 3, 'i1, textarea, div'],
];

const dom = parseDocument(HTML);
console.log(`document: ${HTML}\n`);
console.log('selector'.padEnd(18) + 'Chromium  css-select 7.0.0');
for (const [sel, expected, why] of CHROMIUM) {
  let r; try { r = CSSselect.selectAll(sel, dom).map(e => e.attribs.id || e.name).join(','); } catch (e) { r = e.constructor.name; }
  console.log(sel.padEnd(18) + String(expected).padEnd(10) + (r === '' ? '0' : `${r.split(',').length} (${r})`).padEnd(24) + '  expected: ' + why);
}
