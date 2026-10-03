// SQL parser runner for four JavaScript libraries.
//
// Invoked as:  node node_runner.js <input-file> <k> <engine>
// where engine is one of: nodesql | pgsql | cst | formatter
//
//   nodesql     node-sql-parser, PEG.js, one grammar per dialect
//   pgsql       pgsql-ast-parser, nearley, PostgreSQL only
//   cst         sql-parser-cst, Peggy, keeps comments and whitespace
//   formatter   sql-formatter, nearley; parses and re-prints
//
// All four are given the same PostgreSQL statement and asked to parse it.
// sql-formatter also prints, which is more work than the other three do, so
// read it as a fourth data point rather than a like-for-like ranking; it is
// here because it is the most-downloaded of the four and shares the input
// language exactly.
//
// The whole input is the statement: parsing needs no schema, so nothing is
// split out. `nodes` is reported as the result-shape check: an engine that
// parsed something structurally different would show up there.

'use strict';

const fs = require('fs');
const path = require('path');
const bench = require(path.join(__dirname, '..', '..', 'src', 'core', 'runners', 'bench.js'));

const { text, k, rest } = bench.inputAndK();
const engine = rest[0] || 'pgsql';
const sql = text.trim();

// SQLJS_LEDGER overrides the location (used to keep scratch runs out of output/).
const LEDGER = process.env.SQLJS_LEDGER ||
  path.join(__dirname, '..', '..', 'output', 'sql_js', 'runner_failures.jsonl');

let parseOnce;

if (engine === 'nodesql') {
  const { Parser } = require('node-sql-parser');
  const parser = new Parser();
  parseOnce = () => JSON.stringify(parser.astify(sql, { database: 'postgresql' })).length;
} else if (engine === 'pgsql') {
  const pg = require('pgsql-ast-parser');
  parseOnce = () => JSON.stringify(pg.parse(sql)).length;
} else if (engine === 'cst') {
  const cst = require('sql-parser-cst');
  parseOnce = () => JSON.stringify(cst.parse(sql, { dialect: 'postgresql' })).length;
} else if (engine === 'formatter') {
  const fmt = require('sql-formatter');
  parseOnce = () => fmt.format(sql, { language: 'postgresql' }).length;
} else {
  console.error(`unknown engine: ${engine}`);
  process.exit(2);
}

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
