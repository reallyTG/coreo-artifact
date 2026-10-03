// CSS selector runner for three JavaScript selector engines (nwsapi in two releases).
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is one of: nwsapi* | domselector | cssselect
//
//   nwsapi        nwsapi 2.2.27, the current release after its 2026 rewrite
//   nwsapi_prev   nwsapi 2.2.25, the release before it
//   nwsapi_<v>    any further nwsapi aliased in package.json
//   domselector   @asamuzakjp/dom-selector 9.1.4, the engine jsdom 30 uses
//   cssselect     css-select 7.0.0 over a parse5 tree, what cheerio uses
//
// All four answer the same question: which elements of this document match
// this selector. Parsing the document happens once, outside the timed region,
// because it is not the thing being compared and the engines do not share a
// tree: nwsapi and dom-selector run on a jsdom document, css-select on a
// parse5 htmlparser2-adapter tree. Selector parsing stays inside the timed
// region, since a selector parser is exactly where a blowup could live.
//
// Both nwsapi copies are loaded in every process but only the requested one is
// used, so the comparison is not affected by which is installed under which
// name (2.2.25 is aliased as `nwsapi_prev` in package.json).

'use strict';

const fs = require('fs');
const path = require('path');
const bench = require(path.join(__dirname, '..', '..', 'src', 'core', 'runners', 'bench.js'));

const { text, k, rest } = bench.inputAndK();
const engine = rest[0] || 'nwsapi';

const sep = '\n@@@\n';
const at = text.indexOf(sep);
if (at < 0) {
  console.error('input missing the \\n@@@\\n separator');
  process.exit(2);
}
const selector = text.slice(0, at);
const html = text.slice(at + sep.length);

// SELECTORS_JS_LEDGER redirects the failure ledger, so a run with --output-dir
// elsewhere does not append to the default output tree.
const LEDGER = process.env.SELECTORS_JS_LEDGER ||
  path.join(__dirname, '..', '..', 'output', 'selectors_js', 'runner_failures.jsonl');

let queryOnce;

if (engine.startsWith('nwsapi')) {
  // Any `nwsapi*` engine name resolves through package.json, so the set of
  // versions is defined there and this file never learns them. The alias
  // is the engine name (nwsapi_prev -> 2.2.25).
  const { JSDOM } = require('jsdom');
  const doc = new JSDOM(html).window.document;
  const nw = require(engine)({ document: doc });
  queryOnce = () => nw.select(selector, doc).length;
} else if (engine === 'domselector') {
  const { JSDOM } = require('jsdom');
  const dom = new JSDOM(html);
  const { DOMSelector } = require('@asamuzakjp/dom-selector');
  const ds = new DOMSelector(dom.window);
  queryOnce = () => ds.querySelectorAll(selector, dom.window.document).length;
} else if (engine === 'cssselect') {
  const parse5 = require('parse5');
  const { adapter } = require('parse5-htmlparser2-tree-adapter');
  const CSSselect = require('css-select');
  const tree = parse5.parse(html, { treeAdapter: adapter });
  queryOnce = () => CSSselect.selectAll(selector, tree).length;
} else {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}

let hits = 0;
let firstNs;
try {
  const t = process.hrtime.bigint();
  hits = queryOnce();            // fail fast before measuring; doubles as warm-up
  firstNs = Number(process.hrtime.bigint() - t);
} catch (e) {
  const sha1 = require('crypto').createHash('sha1').update(text).digest('hex');
  try {
    fs.mkdirSync(path.dirname(LEDGER), { recursive: true });
    fs.appendFileSync(LEDGER, JSON.stringify({
      engine, sha1, error: e.constructor.name, message: String(e.message).slice(0, 300),
      selector, doc_bytes: html.length,
    }) + '\n');
  } catch (_) { /* the exit code still signals the failure */ }
  console.error(`query failed: ${e.message}`);
  process.exit(3);
}

// Cap repetitions at a time budget so a slow input is measured rather than
// killed by the subprocess timeout.
const BUDGET_NS = 5e9;
const kEff = Math.max(1, Math.min(k, Math.floor(BUDGET_NS / Math.max(firstNs, 1))));

bench.report(queryOnce, kEff, 0, () => ({ hits, k_used: kEff }));
