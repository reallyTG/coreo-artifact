// sql-formatter runner for the latest-release-series subject.
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is a package.json alias, sql_formatter_<major>_<minor>_<patch>,
// one per preregistered release (eval/latest_series_2026-09-30.json).
//
// Adapted from subjects/sql_js/node_runner.js, `formatter` engine, and kept
// identical to it in everything that decides what is observed: the whole input
// is the statement (trimmed), the measured operation is one
// format(sql, { language: 'postgresql' }) call, the first call is the fail-fast
// warm-up and the estimate for the 5s repetition budget, failures go to a
// ledger, and `nodes` (the output length) is the result-shape check.
// Only the engine dispatch differs: the alias names the version.

'use strict';

const fs = require('fs');
const path = require('path');
const bench = require(path.join(__dirname, '..', '..', 'src', 'core', 'runners', 'bench.js'));

const { text, k, rest } = bench.inputAndK();
const engine = rest[0];
const sql = text.trim();

const LEDGER = path.join(__dirname, '..', '..', 'output', 'sql_formatter_latest', 'runner_failures.jsonl');

if (!engine || !/^sql_formatter_\d+_\d+_\d+$/.test(engine)) {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}
const fmt = require(engine);
const parseOnce = () => fmt.format(sql, { language: 'postgresql' }).length;

let nodes = 0;
let firstNs;
try {
  const t = process.hrtime.bigint();
  nodes = parseOnce();           // fail fast before measuring; doubles as warm-up
  firstNs = Number(process.hrtime.bigint() - t);
} catch (e) {
  const sha1 = require('crypto').createHash('sha1').update(text).digest('hex');
  try {
    fs.mkdirSync(path.dirname(LEDGER), { recursive: true });
    fs.appendFileSync(LEDGER, JSON.stringify({
      engine, sha1, error: e.constructor.name, message: String(e.message).slice(0, 300),
      sql: sql.slice(0, 2000), sql_bytes: sql.length,
    }) + '\n');
  } catch (_) { /* the exit code still signals the failure */ }
  console.error(`parse failed: ${e.message}`);
  process.exit(3);
}

const BUDGET_NS = 5e9;
const kEff = Math.max(1, Math.min(k, Math.floor(BUDGET_NS / Math.max(firstNs, 1))));

bench.report(parseOnce, kEff, 0, () => ({ nodes, k_used: kEff }));
