// pgsql-ast-parser 12.0.2: an escape string constant (E'...') containing any
// backslash escape that JSON does not also define makes the lexer call
// JSON.parse on it and throw a JSON SyntaxError. PostgreSQL accepts all of
// these; libpg-query (PostgreSQL's own grammar, compiled to WASM) is the
// reference and prints the decoded value.
//
//   npm install && node poc.js
const pg = require('pgsql-ast-parser');
const lpq = require('libpg-query');

const CASES = [
  String.raw`SELECT E'\''`,      // escaped quote          -> '
  String.raw`SELECT E'\x41'`,    // hex escape             -> A
  String.raw`SELECT E'\101'`,    // octal escape           -> A
  "SELECT E'" + "\\" + "u0041'",  // 16-bit Unicode escape  -> A
  String.raw`SELECT E'\q'`,      // other char: literal    -> q
  String.raw`SELECT E'\n'`,      // control: JSON has it too, so it works
];

(async () => {
  await lpq.loadModule();
  for (const sql of CASES) {
    const ref = lpq.parseSync(sql).stmts[0].stmt.SelectStmt.targetList[0].ResTarget.val.A_Const.sval.sval;
    let got;
    try { got = 'value ' + JSON.stringify(pg.parse(sql)[0].columns[0].expr.value); }
    catch (e) { got = `${e.constructor.name}: ${e.message.split('\n')[0]}`; }
    console.log(`${sql.padEnd(20)} PostgreSQL: ${JSON.stringify(ref).padEnd(6)} pgsql-ast-parser: ${got}`);
  }
})();
