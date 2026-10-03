// nwsapi 2.2.27: RangeError (stack overflow) on a long selector.
//
// Four selector shapes crash it; a comma-separated list of the same size does
// not. dom-selector, the engine jsdom 30 uses, handles every one of them.
//
//   node poc-stack.js     (after: npm install)
const { JSDOM } = require('jsdom');
const { DOMSelector } = require('@asamuzakjp/dom-selector');

const HTML = '<html><body><div class="a" id="b"><p class="c">x</p></div></body></html>';
const dom = new JSDOM(HTML);
const doc = dom.window.document;
const nw = require('nw2_2_27')({ document: doc });
const ds = new DOMSelector(dom.window);

const SHAPES = {
  'descendant path': (n) => Array.from({ length: n }, (_, i) => `div.c${i}`).join(' '),
  'is() chain':      (n) => 'div' + Array.from({ length: n }, (_, i) => `:is(.c${i}, #d${i})`).join(''),
  'class chain':     (n) => 'div' + Array.from({ length: n }, (_, i) => `.c${i}`).join(''),
  'not() chain':     (n) => 'div' + Array.from({ length: n }, (_, i) => `:not(.c${i})`).join(''),
  'comma list':      (n) => Array.from({ length: n }, (_, i) => `.c${i}`).join(', '),
};

const crashes = (sel) => { try { nw.select(sel, doc); return false; } catch (e) { return e.constructor.name; } };

console.log('shape             smallest crashing size   selector bytes   dom-selector');
for (const [name, make] of Object.entries(SHAPES)) {
  let lo = 1, hi = 20000;
  if (!crashes(make(hi))) { console.log(`${name.padEnd(17)} no crash up to ${hi} parts`); continue; }
  while (lo < hi) { const mid = (lo + hi) >> 1; if (crashes(make(mid))) hi = mid; else lo = mid + 1; }
  const sel = make(lo);
  let other; try { ds.querySelectorAll(sel, doc); other = 'ok'; } catch (e) { other = e.constructor.name; }
  console.log(`${name.padEnd(17)} ${String(lo).padStart(16)} parts ${String(sel.length).padStart(12)}   ${other}`);
}
