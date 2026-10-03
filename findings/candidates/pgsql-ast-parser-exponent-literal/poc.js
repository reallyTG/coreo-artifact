// pgsql-ast-parser 12.0.2 has no exponent form in its numeric lexer. `1e3`
// lexes as the integer 1 followed by the word `e3`, so in a select list it
// parses silently as `1 AS e3`; anywhere else it is a syntax error.
// libpg-query (PostgreSQL's own grammar, compiled to WASM) is the reference.
//
//   npm install && node poc.js
const pg = require('pgsql-ast-parser');
const lpq = require('libpg-query');

const CASES = [
  'SELECT 1e3',                     // silently wrong: 1 AS e3
  'SELECT 2.5e3, 7',                // silently wrong: 2.5 AS e3
  'SELECT 1e3 AS n',                // rejected
  'SELECT 1e3 ^ 2',                 // rejected
  'SELECT 97e19::int',              // rejected
  'SELECT x FROM t WHERE x > 1e3',  // rejected
  'SELECT 2.5E-3',                  // rejected
];

(async () => {
  await lpq.loadModule();
  for (const sql of CASES) {
    const ref = lpq.parseSync(sql).stmts.length ? 'accepted' : '?';
    let got;
    try { got = 'parsed, re-printed as: ' + pg.toSql.statement(pg.parse(sql)[0]); }
    catch (e) { got = `${e.constructor.name}: ${e.message.split('\n')[0]}`; }
    console.log(`${sql.padEnd(32)} PostgreSQL: ${ref}   pgsql-ast-parser: ${got}`);
  }
  const t = lpq.parseSync('SELECT 1e3').stmts[0].stmt.SelectStmt.targetList[0].ResTarget;
  console.log('\nPostgreSQL reads SELECT 1e3 as', JSON.stringify(t.val), 'with no alias');
  console.log('pgsql-ast-parser reads it as  ', JSON.stringify(pg.parse('SELECT 1e3')[0].columns[0]));
})();
