// css-select release series: selectAll(selector-string, tree) cost vs :not() nesting depth.
// Usage: node poc.js            -> depth series for 5.2.2, 6.0.0, 7.0.0
//        node poc.js --ablate   -> 6.0.0 with css-what's CommonJS exports copied to plain
//                                  data properties (one {...spread}), same depth series
'use strict';
const path = require('path');
const parse5 = require('parse5');
const { adapter } = require('parse5-htmlparser2-tree-adapter');

const ablate = process.argv.includes('--ablate');
if (ablate) {
  // css-select 6.0.0's CJS build requires its own css-what 7.0.0 (CJS). Load it, then
  // replace its exports with a plain-object copy before css-select is loaded.
  const csDir = path.dirname(require.resolve('css_select_6_0_0/package.json'));
  const cwPath = require.resolve('css-what', { paths: [csDir] });
  const cw = require(cwPath);
  require.cache[cwPath].exports = { ...cw };
}

const engines = ablate
  ? { '6.0.0 (plain css-what exports)': require('css_select_6_0_0') }
  : { '5.2.2': require('css_select_5_2_2'), '6.0.0': require('css_select_6_0_0'), '7.0.0': require('css_select_7_0_0') };

const doc = '<!DOCTYPE html><html><body>' +
  Array.from({ length: 20 }, (_, i) => `<div class="c${i % 5}" title="t"><p><span>x</span><a href="/${i}">l</a></p></div>`).join('') +
  '</body></html>';
const tree = parse5.parse(doc, { treeAdapter: adapter });

function nest(d) {
  let s = 'span.q[title]';
  for (let i = 0; i < d; i++) s = `a.b${i}[title] > :not(p.c${i}[lang], ${s}) + em`;
  return s;
}
const median = (a) => { a = [...a].sort((x, y) => x - y); return a[a.length >> 1]; };

const names = Object.keys(engines);
console.log(['depth', 'sel_len', ...names.map((n) => `${n} us`)].join('\t'));
for (const d of [0, 2, 4, 8, 16, 32, 64]) {
  const sel = nest(d);
  const row = [d, sel.length];
  for (const n of names) {
    const cs = engines[n];
    for (let i = 0; i < 20; i++) cs.selectAll(sel, tree);
    const t = [];
    for (let i = 0; i < 100; i++) {
      const s = process.hrtime.bigint();
      cs.selectAll(sel, tree);
      t.push(Number(process.hrtime.bigint() - s));
    }
    row.push((median(t) / 1000).toFixed(1));
  }
  console.log(row.join('\t'));
}
