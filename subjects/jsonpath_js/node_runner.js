// JSONPath runner for five JavaScript implementations.
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is one of: plus | dchester | jsonpathly | rfc9535 | p3
//
//   plus        jsonpath-plus     Goessner dialect, own safe JS evaluator
//   dchester    jsonpath          Goessner dialect, static-eval filters
//   jsonpathly  jsonpathly        claims RFC 9535
//   rfc9535     jsonpath-rfc9535  RFC 9535, passes the compliance suite
//   p3          json-p3           RFC 9535, runs the compliance suite
//
// The measured operation is one call of the library's one-shot query API with
// a string query and an already-parsed document, which is how the libraries
// are used. JSON.parse is outside the timed region because it is the same
// V8 builtin for every engine.
//
// Query parsing stays inside the timed region. jsonpath-plus memoises parsed
// paths and compiled filter scripts in JSONPath.cache, so after the warm-up
// call it would time evaluation only and a slow query parser would never
// show. The cache is reset before every call to keep all five engines doing
// the same work.
//
// jsonpath-plus runs with ignoreEvalErrors, so a filter that reads a property
// of a missing value (`@.a.b` where there is no `a`) evaluates to false instead
// of throwing. That matches the other four on the filters the grammar emits.

'use strict';

const fs = require('fs');
const path = require('path');
const bench = require(path.join(__dirname, '..', '..', 'src', 'core', 'runners', 'bench.js'));

const { text, k, rest } = bench.inputAndK();
const engine = rest[0] || 'p3';

const sep = '\n@@@\n';
const at = text.indexOf(sep);
if (at < 0) {
  console.error('input missing the \\n@@@\\n separator');
  process.exit(2);
}
const query = text.slice(0, at);
const doc = JSON.parse(text.slice(at + sep.length));

let queryOnce;

if (engine === 'plus') {
  const { JSONPath } = require('jsonpath-plus');
  queryOnce = () => {
    JSONPath.cache = {};
    return JSONPath({ path: query, json: doc, wrap: true, ignoreEvalErrors: true }).length;
  };
} else if (engine === 'dchester') {
  const jp = require('jsonpath');
  queryOnce = () => jp.query(doc, query).length;
} else if (engine === 'jsonpathly') {
  const jl = require('jsonpathly');
  queryOnce = () => jl.query(doc, query, { returnArray: true }).length;
} else if (engine === 'rfc9535') {
  const r9 = require('jsonpath-rfc9535');
  queryOnce = () => r9.query(doc, query).length;
} else if (engine === 'p3') {
  const p3 = require('json-p3');
  queryOnce = () => p3.jsonpath.query(query, doc).values().length;
} else {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}

// The framework records a failed run as no observation at all, so a crash
// would vanish from the corpus. The framework does not report rejections,
// so the runner appends each one to a ledger next to the subject's output.
// JSONPATH_JS_LEDGER redirects it, so a scratch run with --output-dir stays out of output/.
const LEDGER = process.env.JSONPATH_JS_LEDGER ||
  path.join(__dirname, '..', '..', 'output', 'jsonpath_js', 'runner_failures.jsonl');

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

// K is a precision knob for fast queries. On a slow input, K full repetitions
// would outlast the subprocess timeout and the input would be dropped as a
// failure, exactly where a superlinear engine is worth measuring. So the
// repetitions are capped at a time budget, with the first call as the estimate.
const BUDGET_NS = 5e9;
const kEff = Math.max(1, Math.min(k, Math.floor(BUDGET_NS / Math.max(firstNs, 1))));

bench.report(queryOnce, kEff, 0, () => ({ hits, k_used: kEff }));
