// Tailored-setting copy (RQ1) of subjects/css_select_known/node_runner.js.
// Identical except the default failure-ledger path (output/cssselect_tailored/);
// node_modules is a symlink to subjects/css_select_known/node_modules. The timed
// region and every metric are unchanged.
//
// css-select runner for the css-select known-pair subject (5.1.0, 5.2.0).
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is a package.json alias, css_select_<major>_<minor>_<patch>.
//
// Adapted from subjects/selectors_js/node_runner.js, `cssselect` engine path
// (the same path subjects/css_select_latest uses), and kept identical to it in
// everything that decides what is observed: the input is
// `selector \n@@@\n html`, the document is parsed once with parse5 into an
// htmlparser2-adapter tree outside the timed region (parse5 and the adapter
// pinned to the domain's versions), the measured operation is one
// CSSselect.selectAll(selector, tree) call with selector parsing inside it,
// the first call is the fail-fast warm-up and the estimate for the 5s
// repetition budget, failures go to a ledger, and `hits` is the result-shape
// check. Only the engine dispatch differs: the alias names the version.
// 5.1.0 throws on :read-only and :read-write; those inputs land in the ledger.

'use strict';

const fs = require('fs');
const path = require('path');
const bench = require(path.join(__dirname, '..', '..', 'src', 'core', 'runners', 'bench.js'));

const { text, k, rest } = bench.inputAndK();
const engine = rest[0];

const sep = '\n@@@\n';
const at = text.indexOf(sep);
if (at < 0) {
  console.error('input missing the \\n@@@\\n separator');
  process.exit(2);
}
const selector = text.slice(0, at);
const html = text.slice(at + sep.length);

// SELECTORS_JS_LEDGER redirects the failure ledger, as in the domain runner.
const LEDGER = process.env.SELECTORS_JS_LEDGER ||
  path.join(__dirname, '..', '..', 'output', 'cssselect_tailored', 'runner_failures.jsonl');

if (!engine || !/^css_select_\d+_\d+_\d+$/.test(engine)) {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}
const parse5 = require('parse5');
const { adapter } = require('parse5-htmlparser2-tree-adapter');
const CSSselect = require(engine);
const tree = parse5.parse(html, { treeAdapter: adapter });
const queryOnce = () => CSSselect.selectAll(selector, tree).length;

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
