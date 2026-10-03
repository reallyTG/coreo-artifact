// nwsapi >= 2.2.12: a valid selector of the form
//
//     <compound with a pseudo-class> + [attribute="value"]
//
// is rejected as invalid. With the default VERBOSITY the rejection throws;
// with VERBOSITY off it silently returns zero matches, which is the worse
// outcome. nwsapi 2.2.9 and earlier return the correct result.
//
//   node poc.js     (after: npm install)
//
// The adjacent-sibling combinator `+` is required: `~`, `>` and descendant all
// work. So is the attribute selector on the right: `+ div` works. So is a
// pseudo-class on the left: `section + [class="cb"]` works.
const { JSDOM } = require('jsdom');
const { DOMSelector } = require('@asamuzakjp/dom-selector');

const HTML = '<html><body><p class="a">x</p><div class="cb">y</div></body></html>';
const SELECTOR = 'p:not(.x) + [class="cb"]';   // matches the div

const dom = new JSDOM(HTML);
const reference = new DOMSelector(dom.window).querySelectorAll(SELECTOR, dom.window.document).length;

console.log(`selector: ${SELECTOR}`);
console.log(`document: ${HTML}`);
console.log(`expected: ${reference} match (dom-selector, the engine jsdom 30 uses)\n`);

for (const version of ['2.2.9', '2.2.12', '2.2.27']) {
  const doc = new JSDOM(HTML).window.document;
  const nw = require('nw' + version.replace(/\./g, '_'))({ document: doc });
  let thrown = null, quiet = null;
  try { thrown = `${nw.select(SELECTOR, doc).length} matches`; } catch (e) { thrown = `${e.constructor.name}: ${e.message}`; }
  nw.configure({ VERBOSITY: false, LOGERRORS: false });
  try { quiet = `${nw.select(SELECTOR, doc).length} matches`; } catch (e) { quiet = `${e.constructor.name}`; }
  console.log(`nwsapi ${version.padEnd(7)} default: ${thrown.padEnd(46)} VERBOSITY off: ${quiet}`);
}

// Variants, on the current release, showing what is and is not affected.
const doc = new JSDOM(HTML).window.document;
const nw = require('nw2_2_27')({ document: doc });
console.log();
for (const s of ['p:not(.x) + [class="cb"]', 'p:nth-child(1) + [class="cb"]', 'p:first-child + [class="cb"]',
                 'p + [class="cb"]', 'p:not(.x) ~ [class="cb"]', 'p:not(.x) + div']) {
  let r;
  try { r = `${nw.select(s, doc).length} matches`; } catch (e) { r = `${e.constructor.name}`; }
  console.log('  ', s.padEnd(32), r);
}
