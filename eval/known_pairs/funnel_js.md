# Known performance pairs: JavaScript SUTs (2026-10-01)

Per-commit rows are in `<package>.csv` in this directory. These are `jsonpath-plus`, `jsonpath`, `jsonpathly`, `jsonpath-rfc9535`, `json-p3`, `nwsapi`, `css-select`, `asamuzakjp-dom-selector`, `sql-formatter`, `pgsql-ast-parser` and `sql-parser-cst`. Nothing was installed, timed or committed.

## Collection rule

The rule was applied identically to every package:

- **Commits:** all commits on the default branch since 2024-01-01 whose subject or body matches `perf|performance|speed|faster|slow|optimi[sz]|quadratic|cache|memory|leak|regression`, case-insensitive. The query was `git log --since=2024-01-01 -i -E --grep=...` on a `--filter=blob:none` clone.
- **Changelog entries:** CHANGELOG and GitHub release-note entries from the same window that mention performance and link a commit or PR. These were added to the set.
- **Deduplication:** entries were merged by change, so a branch commit with the same diff as the merged commit counts once (sql-formatter e2ed5ec folded into 6c21ff5).
- **Repositories:** each repository URL was taken from `npm view <pkg> repository.url`.

The rule picks up many false positives, such as "superfluous", PERFORM, CI caches, "regression test" and yarn logs. They are kept as S1 = no rows, so the funnel shows them dropping out.

## Funnel

Each row reads collected → S1 (actual perf change) → S2 (input-dependent) → S3 class.

| Domain / package | Collected | S1 yes | S2 yes | Expressible | Not expressible | Not measurable | Unclear |
|---|---|---|---|---|---|---|---|
| jsonpath-plus | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| jsonpath (dchester) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jsonpathly | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| jsonpath-rfc9535 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| json-p3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| JSONPath total (subjects/jsonpath_js) | 9 | 1 | 1 | 1 | 0 | 0 | 0 |
| nwsapi | 15 | 9 | 7 | 6 | 1 | 0 | 0 |
| css-select | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| @asamuzakjp/dom-selector | 57 | 38 | 31 | 20 | 5 | 5 | 1 |
| Selectors total (subjects/selectors_js) | 73 | 48 | 39 | 27 | 6 | 5 | 1 |
| sql-formatter | 9 | 1 | 1 | 1 | 0 | 0 | 0 |
| sql-parser-cst | 12 | 4 | 2 | 2 | 0 | 0 | 0 |
| pgsql-ast-parser | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SQL total (subjects/sql_js) | 21 | 5 | 3 | 3 | 0 | 0 | 0 |
| All JS | 103 | 54 | 43 | 31 | 6 | 5 | 1 |

Each of the 31 expressible commits maps to a release pair. Some pairs hold more than one commit, which leaves 28 distinct pairs: dom-selector 9.0.4 → 9.1.0 holds two commits, and sql-parser-cst 0.21.2 → 0.22.0 holds two.

### Where pairs drop out

- **JSONPath, S1:** almost nothing in this domain is a perf change.
  - jsonpath-plus: the "cache" hits are security fixes (cache-key collisions and `__proto__` poisoning), type fixes and tests.
  - json-p3 3858099: a crash fix that matched only through a path in the body. It is also a correctness fix, because 2.3.1 throws above about 130k results and 2.3.2 returns them.
  - dchester/jsonpath and jsonpath-rfc9535: no matching commits in the window.
- **Selectors, S2:** nwsapi and dom-selector cache the compiled resolver or AST per selector string. The runner makes one untimed warm-up call and then repeats the same selector, so parse and compile changes land outside the timed loop. Those commits are S2 = no or `not_measurable`.
  - Commits in APIs the runner never calls are `not_measurable`: `querySelector` only, `closest`, `check`, and jsdom idlUtils.
  - Omitted pseudo-classes and document features outside the grammar's declared subset are `not_expressible`.
- **SQL, S1 and S2:** S1 dropped keyword false positives, tests and functional fixes. S2 dropped the two sql-parser-cst commits that only speed up building the parser. pgsql-ast-parser has 15 commits since 2024 and none match the rule.

## Expressible release pairs ready to measure

All versions listed are published on npm and not deprecated. Wiring follows the `subjects/*_latest` pattern: one npm alias per version in a pair subject's `package.json`, plus a runner engine branch where noted.

### JSONPath (subjects/jsonpath_js)

| Package | Before | After | Commit(s) | Wiring | Confounds / notes |
|---|---|---|---|---|---|
| jsonpathly | 3.0.0 (2026-01-10) | 3.0.1 (2026-09-21) | 2879324 (accumulate results in place; quadratic → linear in result count) | alias `npm:jsonpathly@3.0.1`; 3.0.0 is already the pinned version | Low. 62adf0b (sparse-array fix) is unreachable from `JSON.parse` input. The effect needs thousands of result nodes, reached through `..`/wildcard over long `<more_value>*` lists. Not measured: the release fixes a bug the authors reported, so the pair is not independent of the tool. |

### Selectors (subjects/selectors_js)

`nwsapi`: the runner already dispatches any `nwsapi*` dependency name, so each pair needs only aliases.

| Before | After | Commit(s) | Confounds / notes |
|---|---|---|---|
| 2.2.26 | 2.2.27 | 0d54bd5 (:has compile branch) | already wired; the published diff also contains null guards (correctness) |
| 2.2.25 | 2.2.26 | c4055f7 (ES5 LRU resolver cache) | already wired; this release has the #171 slowdown, which is not tied to a commit; also contains focus/display-state rework |
| 2.2.24 | 2.2.25 | 4be8dd8 (Map-based LRU cache) | needs a 2.2.24 alias; :has compiler revision and new omitted pseudo-classes |
| 2.2.23 | 2.2.24 | de99cea (restore combinator state) | correctness fix for #160 that gives back the 3d8f8d2 speedup |
| 2.2.21 | 2.2.22 | 3d8f8d2 (faster combinator resolvers) | introduced the #160 bug, so results are wrong for nested combinators |
| 2.2.20 | 2.2.21 | 47b31b7 (:has resolver rewrite) | 2.2.20 delegates descendant :has to jsdom's querySelector (dom-selector), which mixes two engines |

`@asamuzakjp/dom-selector`: needs aliases plus a runner branch `domselector_<v>`. v5 and later take `new DOMSelector(window)`. The v4 constructor was not checked. v1–v3 export a plain `querySelectorAll(selector, node)` and need an adapter.

| Before | After | Commit(s) | Notes |
|---|---|---|---|
| 9.2.1 | 9.2.2 | c8ccd4b (single-leaf cache skip) | |
| 9.1.1 | 9.1.2 | f9fbf0f (quoted attribute equality) | |
| 9.0.4 | 9.1.0 | c3c816e (:disabled cache), 447efff (unescape cache) | bundled with the AST-cache commits |
| 9.0.3 | 9.0.4 | 0e70971 (`[attr]` presence fast path) | reached only when the whole selector is one attribute selector |
| 8.2.4 | 8.2.5 | 648283e (fix for perf regression #286, nth index cache) | strongest candidate; also consider measuring 8.2.1 vs 8.2.5 |
| 8.0.2 | 8.1.1 | 84885a3 (An+B and :lang traversal caches) | bundled with omitted-construct commits |
| 7.0.5 | 7.0.6 | ffcd5f6 (sibling scans replace TreeWalker) | |
| 7.0.4 | 7.0.5 | 787fa8c (cache selector AST across calls, #221) | |
| 7.0.2 | 7.0.3 | 81fa0c9 (fewer combinator allocations) | also changes which selectors go to the nwsapi fork |
| 6.7.2 | 6.7.3 | 3438ad5 | mixes perf and correctness changes |
| 6.5.5 | 6.5.6 | 6f882a1 (cache filterSelector result) | |
| 4.6.5 | 5.0.0 | 5cd5b0c (cache rework) | major version, confounded |
| 4.6.1 | 4.6.3 | 861eb10 (:is/:not cacheability) | 4.6.2 was never published |
| 4.4.13 | 4.5.0 | 5160532 (content-keyed AST cache) | |
| 4.4.10 | 4.4.11 | 86fee0c | slowdown taken on purpose to fix correctness |
| 4.0.1 | 4.1.0 | 28cab36 (TreeWalker reuse) | |
| 3.0.5 | 4.0.0 | e9131e1 | major version, API change |
| 1.2.4 | 1.2.5 | a09a463 (perf degradation #26) | v1 adapter |
| 1.2.3 | 1.2.4 | 6efbab4 (perf degradation #22) | v1 adapter |

`css-select`:

| Before | After | Commit(s) | Wiring | Notes |
|---|---|---|---|---|
| 5.1.0 | 5.2.0 (2025-06-28) | d4064e4 (PR #1025, :has subtree cache) | one alias; the runner already uses `require` | The commit is dated 2023-04-08 and came in through the in-window release note. The range covers three years. 5.1.0 throws on `:read-only`/`:read-write`, so inputs using them break equivalence. |

### SQL (subjects/sql_js)

| Package | Before | After | Commit(s) | Wiring | Confounds / notes |
|---|---|---|---|---|---|
| sql-formatter | 15.8.2 (2026-06-21) | 15.9.0 (2026-09-23) | 6c21ff5 (PR #963, quadratic expression-list accumulation, issue #840) | none: `subjects/sql_formatter_latest` already aliases both | Reached by long `<select_list>`, `<expr_list>` and OR chains. #972 (alias after AS) and #959 (BETWEEN spacing) are small output changes. |
| sql-parser-cst | 0.21.2 (2024-01-07) | 0.22.0 (2024-01-09) | afba66f (remove PEG backtracking alternatives in expressions), 0596f1b (left-factor `::` cast) | new pair subject with two aliases and a copy of the cst branch of `sql_js/node_runner.js` | The release note cites issue #52, a "serious performance regression" on PostgreSQL. The range also has about 40 PostgreSQL DML and CST-rename commits that the SELECT-only grammar never reaches. 0.21.2 is 20 minors older than the pinned 0.42.1, so expect more inputs rejected on the before side. |

## Caveats

1. **Expressibility is argued, not tested.** Each S3 class comes from matching the diff's code path against the frozen grammar productions and the runner's timed region. No inputs were run through either version.
2. **The selector runner's warm-up hides cache effects.** Caching selector compilation interacts with the untimed warm-up call: the header's claim that selector parsing stays timed holds for css-select but mostly not for nwsapi or dom-selector. Cache-implementation commits were counted as expressible only where :has/:not recompile per element inside the timed loop (nwsapi) or where the cache affects per-element matching.
3. **Which dom-selector path a selector takes was not verified.** dom-selector sends some selectors to its internal nwsapi fork and the rest to its Finder. Several expressible rows reach the changed code only through the Finder path, for example inside :is or :has. The one `unclear` row, 9649304 (8.2.1 cache swap), turns on this question.
4. **nwsapi release mapping is approximate for 2.2.21 and 2.2.26.** The published tarballs do not byte-match any git commit. Mapping used git ancestry of the version-bump commits. The #171 and #172 slowdowns do not match the keyword rule and are not rows.
5. **Correctness fixes are mixed into several pairs.** These pairs break equivalence on some inputs:
   - nwsapi: de99cea, 3d8f8d2, 47b31b7, 0d54bd5 and db1dd3e.
   - dom-selector: 3438ad5, 5107aa2 and 86fee0c.
   - json-p3: 3858099.
   - css-select: the `:read-only`/`:read-write` gap.

   Scoring should drop inputs where the two versions disagree on output.
6. **One pair is not independent of the tool.** jsonpathly 3.0.0 → 3.0.1 fixes a bug the authors reported. The pair is excluded from measurement and the paper says so.
7. **Judgement calls:**
   - jsonpathly 62adf0b entered through the same changelog release as 2879324. Dropping it makes jsonpathly 2 collected, not 3.
   - css-select #1025 was included because its release note is in-window, although its commit is from 2023.
   - sql-parser-cst's v0.38.1 "fix regression" note is functional and was not collected.
8. **jsonpath-plus at 11.0.0 and later needs the other runner.** From 11.0.0 the frozen runner's `JSONPath.cache = {}` reset is a no-op, so any pair crossing 11.0.0 must use the `jsonpath_plus_latest` runner with `clearCache()`. No jsonpath-plus pair survived the funnel.
9. **PR numbers were taken only from commit messages and release notes.** They were not checked against the GitHub API.
