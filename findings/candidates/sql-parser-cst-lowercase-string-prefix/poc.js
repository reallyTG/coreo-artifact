// sql-parser-cst 0.42.1, dialect "postgresql": the string prefixes E'...' and
// U&'...' are matched case-sensitively. PostgreSQL accepts either case.
//   e'x'   -> syntax error
//   u&'x'  -> parses silently as the binary expression  u & 'x'
// libpg-query (PostgreSQL's own grammar, compiled to WASM) is the reference.
//
//   npm install && node poc.js
const cst = require('sql-parser-cst');
const lpq = require('libpg-query');

const strip = (k, v) => (k === 'range' ? undefined : v);
const firstColumn = sql => {
  const stmt = cst.parse(sql, { dialect: 'postgresql' }).statements[0];
  return JSON.stringify(stmt.clauses[0].columns.items[0], strip);
};
const pgColumn = sql => {
  const v = lpq.parseSync(sql).stmts[0].stmt.SelectStmt.targetList[0].ResTarget.val;
  return JSON.stringify(v.A_Const ? { A_Const: v.A_Const.sval ?? v.A_Const.bsval } : v);
};

(async () => {
  await lpq.loadModule();
  for (const sql of ["SELECT E'x'", "SELECT e'x'", "SELECT U&'x'", "SELECT u&'x'", "SELECT b'1'", "SELECT x'1F'"]) {
    let got; try { got = firstColumn(sql); } catch (e) { got = e.message.split('\n')[0]; }
    console.log(`${sql.padEnd(14)} PostgreSQL: ${pgColumn(sql).padEnd(26)} sql-parser-cst: ${got}`);
  }

  // Smaller gaps in the same dialect, from the same probe (see README).
  console.log();
  for (const sql of ['SELECT count(ALL a) FROM t', "SELECT '10.0.0.0/8'::inet >> ANY (ARRAY['10.1.2.3'::inet])"]) {
    let ref; try { lpq.parseSync(sql); ref = 'accepted'; } catch (e) { ref = 'REJECTED'; }
    let got; try { cst.parse(sql, { dialect: 'postgresql' }); got = 'accepted'; } catch (e) { got = e.message.split('\n')[0]; }
    console.log(`${sql.padEnd(62)} PostgreSQL: ${ref}   sql-parser-cst: ${got}`);
  }
})();
