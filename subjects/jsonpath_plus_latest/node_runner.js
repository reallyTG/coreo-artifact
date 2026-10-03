// jsonpath-plus runner for the latest-release-series subject.
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is a package.json alias, jsonpath_plus_<major>_<minor>_<patch>,
// one per preregistered release (eval/latest_series_2026-09-30.json).
//
// Adapted from subjects/jsonpath_js/node_runner.js, `plus` engine, and kept
// identical to it in everything that decides what is observed: the input is
// `query \n@@@\n document`, JSON.parse is outside the timed region, the
// measured operation is one JSONPath({ path, json, wrap: true,
// ignoreEvalErrors: true }) call with the path/script cache reset before each
// call (so query parsing stays inside the timed region), the first call is the
// fail-fast warm-up and the estimate for the 5s repetition budget, failures go
// to a ledger, and `hits` is the result-shape check. Only the engine dispatch
// differs: the alias names the version.

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
const query = text.slice(0, at);
const doc = JSON.parse(text.slice(at + sep.length));

if (!engine || !/^jsonpath_plus_\d+_\d+_\d+$/.test(engine)) {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}
const { JSONPath } = require(engine);
// 11.0.0 moved the memo out of the public JSONPath.cache object into two
// module-level Maps (parsed paths, compiled filter scripts) and added
// JSONPath.clearCache(). Assigning JSONPath.cache = {} is a silent no-op there,
// and would let 11.x time evaluation only while 10.x times parse + evaluate.
// So each version is reset through the mechanism it actually has.
const resetCache = typeof JSONPath.clearCache === 'function'
  ? () => JSONPath.clearCache()
  : () => { JSONPath.cache = {}; };
const queryOnce = () => {
  resetCache();
  return JSONPath({ path: query, json: doc, wrap: true, ignoreEvalErrors: true }).length;
};

// The framework records a failed run as no observation at all, so a crash
// would vanish from the corpus. The runner appends each one to a ledger next
// to the subject's output.
const LEDGER = path.join(__dirname, '..', '..', 'output', 'jsonpath_plus_latest', 'runner_failures.jsonl');

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
      query, doc_bytes: text.length - at - sep.length,
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
