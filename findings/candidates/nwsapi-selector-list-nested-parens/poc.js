// nwsapi <= 2.2.27: a functional pseudo-class whose argument list has a
// nested parenthesised item before a comma, such as :is(:is(p), p), is
// rejected as invalid. The top-level selector-list split (REX.SplitGroup)
// stops at the first ')' and so splits on the comma inside the argument.
// With the nested item last, :is(p, :is(p)), it works. Fixed in 2.2.28.
//
//   npm install && node poc.js
const { JSDOM } = require('jsdom');
const { DOMSelector } = require('@asamuzakjp/dom-selector');

const HTML = '<p id="a">x</p><p>y</p><div>z</div>';
const SELECTORS = [':is(:is(p), p)', ':not(:is(p), p)', ':has(:nth-child(1), p)', 'div, :where(:not(p), p)', ':is(p, :is(p))'];
const VERSIONS = ['2.2.9', '2.2.23', '2.2.24', '2.2.27', '2.2.28'];

const ref = new JSDOM(HTML);
const ds = new DOMSelector(ref.window);
console.log(`document: ${HTML}\n`);
console.log('selector'.padEnd(26) + 'dom-selector  ' + VERSIONS.map(v => ('nwsapi ' + v).padEnd(15)).join(''));
for (const sel of SELECTORS) {
  const row = [String(ds.querySelectorAll(sel, ref.window.document).length).padEnd(14)];
  for (const v of VERSIONS) {
    const doc = new JSDOM(HTML).window.document;
    const nw = require('nw' + v.replace(/\./g, '_'))({ document: doc });
    let r; try { r = String(nw.select(sel, doc).length); } catch (e) { r = e.constructor.name; }
    row.push(r.padEnd(15));
  }
  console.log(sel.padEnd(26) + row.join(''));
}

// The split itself, with the regular expression copied from 2.2.27 line 64:
const SplitGroup = /(\([^)]*\)|\[[^[]*\]|\\.|[^,])+/g;
console.log('\nREX.SplitGroup on ":is(:is(p), p)" ->', JSON.stringify(':is(:is(p), p)'.match(SplitGroup)));
