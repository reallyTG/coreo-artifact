// pgsql-ast-parser 12.0.2 rejects valid PostgreSQL in several grammar rules.
// Each group below has a one-line cause in the nearley grammar (see README).
// libpg-query (PostgreSQL's own grammar, compiled to WASM) is the reference.
//
//   npm install && node poc.js
const pg = require('pgsql-ast-parser');
const lpq = require('libpg-query');

const GROUPS = {
  'A. HAVING without GROUP BY (no issue found)': [
    'SELECT count(*) FROM t HAVING count(*) > 1',
    'SELECT HAVING TRUE',
  ],
  'B. subscript followed by :: or -> (no issue found)': [
    'SELECT a[1]::real',
    "SELECT a[1]->'x'",
  ],
  'C. -> / ->> with a non-literal right operand (no issue found)': [
    'SELECT a -> b',
    "SELECT a ->> ('k' || 'x')",
  ],
  'D. parenthesised join with an alias, or nested on the right (#153)': [
    'SELECT * FROM (a JOIN b ON TRUE) AS d',
    'SELECT * FROM a LEFT JOIN (b JOIN c ON TRUE) ON TRUE',
  ],
  'Known: INTERSECT / EXCEPT (#117)': ['SELECT a FROM t INTERSECT SELECT b FROM u'],
  'Known: WITH RECURSIVE without a column list (#174, open PR)': ['WITH RECURSIVE a AS (SELECT 1 UNION SELECT 2) SELECT 1'],
  'Known: redundant parentheses around a SELECT (#146, open PR)': ['WITH a AS ((SELECT 1)) SELECT 1'],
};

(async () => {
  await lpq.loadModule();
  for (const [group, stmts] of Object.entries(GROUPS)) {
    console.log(group);
    for (const sql of stmts) {
      let ref; try { lpq.parseSync(sql); ref = 'accepted'; } catch (e) { ref = 'REJECTED'; }
      let got; try { pg.parse(sql); got = 'accepted'; } catch (e) { got = e.message.split('\n')[0]; }
      console.log(`  ${sql.padEnd(56)} PostgreSQL: ${ref}   pgsql-ast-parser: ${got}`);
    }
  }
})();
