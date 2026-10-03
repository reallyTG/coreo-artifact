// pgsql-ast-parser 12.0.2: "Ambiguous SQL syntax" on a valid PostgreSQL
// statement.
//
// The library's own message asks for exactly this report:
//   "💀 Ambiguous SQL syntax: Please file an issue stating the request that
//    has failed"
//
//   node poc.js     (after: npm install)
//
// libpg-query is the real PostgreSQL grammar compiled to WASM; it is here as
// the oracle that the statement is valid, not as a comparison implementation.
const pg = require('pgsql-ast-parser');
const cst = require('sql-parser-cst');
const fmt = require('sql-formatter');
const pgq = require('libpg-query');

const SQL =
  "SELECT FROM t JOIN u ON ('x') AND ad.a IS NULL AND " +
  "(SELECT FROM de JOIN a ON (SELECT FROM a JOIN e ON (NOT f(a)) " +
  "GROUP BY g ORDER BY dc DESC, c ASC, c.x DESC, e.y DESC) GROUP BY ec, ac)";

(async () => {
  console.log('statement (' + SQL.length + ' chars):\n' + SQL + '\n');

  try { await pgq.parse(SQL); console.log('PostgreSQL grammar (libpg-query)  accepted'); }
  catch (e) { console.log('PostgreSQL grammar (libpg-query)  REJECTED: ' + e.message.slice(0, 60)); }

  try { cst.parse(SQL, { dialect: 'postgresql' }); console.log('sql-parser-cst                    accepted'); }
  catch (e) { console.log('sql-parser-cst                    failed: ' + e.message.slice(0, 60)); }

  try { fmt.format(SQL, { language: 'postgresql' }); console.log('sql-formatter                     accepted'); }
  catch (e) { console.log('sql-formatter                     failed: ' + e.message.slice(0, 60)); }

  try { pg.parse(SQL); console.log('pgsql-ast-parser                  accepted'); }
  catch (e) { console.log('pgsql-ast-parser                  ' + e.message.split('\n')[0].slice(0, 90)); }
})();
