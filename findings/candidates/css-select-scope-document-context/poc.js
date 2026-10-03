// css-select 5.x-7.0.0: when the query context is a Document (the usual
// `selectAll(sel, parseDocument(html))`, and what cheerio's `$(sel)` does),
// `:scope` matches nothing at all. Browsers treat `:scope` in
// document.querySelectorAll as the root element, so `:scope`, `html:scope`,
// `:scope > body` and `:scope body` each match one element.
//
//   npm install && node poc.js
const { parseDocument } = require('htmlparser2');
const cheerio = require('cheerio');

const HTML = '<html><head></head><body><p>a</p></body></html>';
// Chromium 151, document.querySelectorAll on the same HTML:
const CHROMIUM = { ':scope': 1, 'html:scope': 1, ':scope > body': 1, ':scope body': 1, ':scope > html': 0, ':root > body': 1 };

const dom = parseDocument(HTML);
const $ = cheerio.load(HTML);
const run = f => { try { return String(f()); } catch (e) { return e.constructor.name; } };
console.log(`document: ${HTML}\n`);
console.log('selector'.padEnd(16) + 'Chromium  css-select 7.0.0  css-select 5.2.2  cheerio 1.2.0');
for (const [sel, expected] of Object.entries(CHROMIUM)) {
  console.log(sel.padEnd(16) + String(expected).padEnd(10) +
    run(() => require('cs7').selectAll(sel, dom).length).padEnd(18) +
    run(() => require('cs5').selectAll(sel, dom).length).padEnd(18) +
    run(() => $(sel).length));
}
