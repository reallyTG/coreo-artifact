// dom-selector runner for the tailored dom-selector subject (RQ1, tailored
// setting): subjects/domselector_known/node_runner.js plus one declared
// addition, the second metric `fresh_ns`.
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is a package.json alias, domselector_<major>_<minor>_<patch>,
// one per release from 8.2.4 to 9.2.2 (node_modules is a symlink to
// subjects/domselector_known/node_modules, so the installs are the same).
//
// runtime_ns is computed exactly as in domselector_known: jsdom parses the
// document outside the timed region, the first ds.querySelectorAll call is the
// fail-fast warm-up and the estimate for the 5s repetition budget, and
// bench.report times kEff calls on the same warm DOMSelector instance. That
// path is identical in both runners.
//
// fresh_ns: after the runtime_ns measurement has finished (bench.report
// calls the extra-metrics function only after its own timed loop), the median
// over kFresh calls, each made on a NEW DOMSelector(dom.window) instance in the
// already-warm process: the instance's caches are cold (nthIndexCache, result
// and AST caches live on the instance), the JIT is warm. Constructing the
// instance is outside each timed call. kFresh is capped by the same 5s budget,
// estimated from the first call (itself a cold-instance call). The rationale is
// the 8.2.5 change (648283e, #286): its nthIndexCache fix shows only with
// cold caches (0.54x fresh vs 1.0x warm at corpus scale, 0.01x on a
// 3,000-sibling document).

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
  path.join(__dirname, '..', '..', 'output', 'domselector_tailored', 'runner_failures.jsonl');

if (!engine || !/^domselector_\d+_\d+_\d+$/.test(engine)) {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}
const { JSDOM } = require('jsdom');
const dom = new JSDOM(html);
const { DOMSelector } = require(engine);
const ds = new DOMSelector(dom.window);
const queryOnce = () => ds.querySelectorAll(selector, dom.window.document).length;

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

// fresh_ns: one query per new instance, timed per call, after the warm loop.
function freshNs() {
  const kFresh = kEff;
  const times = [];
  for (let i = 0; i < kFresh; i++) {
    const fresh = new DOMSelector(dom.window);
    const t = process.hrtime.bigint();
    fresh.querySelectorAll(selector, dom.window.document);
    times.push(Number(process.hrtime.bigint() - t));
  }
  return { fresh_ns: bench.median(times), k_fresh: kFresh };
}

bench.report(queryOnce, kEff, 0, () => ({ hits, k_used: kEff, ...freshNs() }));
