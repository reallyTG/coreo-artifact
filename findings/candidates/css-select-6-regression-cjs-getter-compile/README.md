# css-select 6.0.0: selector compilation slows down with `:not()` nesting, through css-what's CommonJS getters

- **Package**: [css-select](https://github.com/fb55/css-select) 6.0.0
  (2025-06-29), compared with 5.2.2 (2025-06-28) and 7.0.0 (2026-03-22).
- **Class**: performance regression between consecutive releases. Every
  `selectAll(selectorString, ...)` call compiles the selector, and in 6.0.0
  compilation costs up to 3x as much as in 5.2.2 on nested `:not()`/`:is()`
  selectors. A smaller slowdown of 1.3x to 1.5x on matching over large
  documents is present as well and was not dissected.
- **Status**: not reported. 7.0.0 is faster than 5.2.2 on every input
  tried, so users on 7.0.0 are not affected. Users who `require()`
  css-select 5.2.0, 5.2.1 or 6.0.0 are.
- **Reproduce**: `npm install && node poc.js && node poc.js --ablate`
  (Node 26.5.0 used below).

## Provenance

Flagged blind by the preregistered css-select latest series
(`eval/latest_series_2026-09-30.json`), final run 2026-10-02
(`results/rq1/20261002-0054-final-css_select_latest`). The mechanism was
worked out by hand.

The run reported 5.2.2 vs 6.0.0 as 22 of 27 regions decided, all with 5.2.2
cheaper, best ratio 1.457 on `count_href_attr` in region 1 to 1.513. Per
input over the 175 inputs measured on all engines, 6.0.0 / 5.2.2 has a
geometric mean of 1.217 (10th to 90th percentile 1.07 to 1.43). The reported
property is a correlate rather than the driver: the per-input log ratio has
Spearman -0.24 with `count_href_attr` and +0.23 to +0.25 with
`selector_nesting`, `count_lparen` and `selector_len`. The median ratio rises
from 1.23 at `selector_nesting` 0 to 1.52 to 1.54 at nesting 6 to 7.

## Re-timing with the harness runner

`subjects/css_select_latest/node_runner.js`, k=200, median of 3 runs, the 8
corpus inputs with the largest 6.0.0 / 5.2.2 ratio plus 8 random ones:

| comparison      | geometric mean over 16 inputs | top 7 inputs (930-1,085 char nested `:not` selectors) |
|-----------------|------------------------------:|------------------------------------------------------:|
| 6.0.0 / 5.2.2   | 1.42                          | 1.63 to 1.73                                          |
| 5.2.0 / 5.2.2   | 1.30                          | 1.56 to 1.62                                          |
| 7.0.0 / 6.0.0   | 0.54                          | 0.41 to 0.44                                          |
| 7.0.0 / 5.2.2   | 0.77                          | 0.70 to 0.73                                          |

On the top input (`9c6425ab...`), splitting the call shows the cost is in
compilation: 5.2.2 spends 111 us compiling and 4.5 us matching, 6.0.0
spends 197 us compiling and 4.9 us matching.

## Scaling series (`poc.js`)

The selector nests `a.bN[title] > :not(p.cN[lang], <inner>) + em` d times
over a fixed 20-`<div>` document. Microseconds per `selectAll` call, median
of 100:

| depth | selector chars | 5.2.2 | 6.0.0 | 7.0.0 | 6.0.0 with plain css-what exports |
|------:|---------------:|------:|------:|------:|----------------------------------:|
|     0 |             13 |  12.6 |  15.5 |   9.7 |                              14.8 |
|     4 |            161 |  25.4 |  44.4 |  20.6 |                              26.3 |
|    16 |            617 | 123.8 | 283.8 |  81.1 |                              85.4 |
|    64 |          2,489 | 1,137 | 3,418 |   785 |                               720 |

Compilation is quadratic in nesting depth on all three releases. The 6.0.0 /
5.2.2 ratio grows with depth, from 1.2 at depth 0 to 3.0 at depth 64,
because 6.0.0 has a larger quadratic coefficient. Selector-list width at
depth 1 (`:not(a.x0[title], ..., a.xN[title])`, N up to 128) keeps a flat
ratio of 1.28 to 1.33. The number of `href` attributes in the document has no
effect: on a 640-paragraph document, the ratio falls from 1.48 to 1.33 as
`href` count rises from 0 to 640.

## Mechanism

Release history: the 5.2.2 tag is the 5.1.0 code with only `package.json`
and the lockfile changed (`git diff v5.1.0 v5.2.2`), published after 5.2.0
and 5.2.1. 6.0.0 is built from the 5.2.x line plus the tshy/vitest/Biome
switch (`f7fd5fc`). The "6.0.0 regression" against 5.2.2 is therefore mostly
the 5.2.0 source changes coming back after the 5.2.2 rollback, plus about
5-10% from 6.0.0's build output.

1. Source bisect over 5.1.0..5.2.0, with every commit's `src/` transpiled
   the same way (TypeScript 5.4 `transpileModule`, CommonJS, ES2019) and
   timed on the top corpus input: 5.1.0 137 us, `52adfc8` (tsconfig module
   resolution) 146 us, `5dfd4b0` (helpers subdirectory) 168 us, `cccdeb9`
   ("Limit cacheing to expensive selectors", #1033) 224 us, 5.2.0 223 us,
   6.0.0 222 us. `cccdeb9` is the largest single step (+39%). It moves the
   rule loop into `compileToken` and calls `getQuality(rule)` on every rule
   at every nesting level. `getQuality` recurses through the whole `:not`/
   `:is` subtree, so compilation does an extra subtree walk per level.
2. Each step of that walk reads `SelectorType.*`, `AttributeAction.*` and
   `isTraversal` from css-what. css-what's CommonJS build (6.2.2 used by
   5.x, 7.0.0 used by 6.0.0) re-exports these through TypeScript's
   `__exportStar`/`__createBinding`, which defines accessor properties, so
   each read is a getter call. Copying css-what's exports to plain data
   properties (`require.cache[cssWhat].exports = {...cssWhat}`, the
   `--ablate` mode) brings 6.0.0 at depth 64 from 3,418 us to 720 us, below
   5.2.2. Replacing only the `types.js` re-export (the enums) recovers most
   of it at depth 16 (307 to 159 us). Replacing only the function getters
   recovers nothing. Swapping css-what 6 for 7 under 6.0.0 changes nothing
   (within 2%), so the css-what version bump is not the cause.
3. 7.0.0's speedup on nesting comes from its dependencies. The 7.0.0 source
   built against the 6.0.0 dependency set is as slow as 6.0.0 at depth 16
   (301 vs 306 us). With css-what 8.0.0 alone swapped in it takes 102 us.
   css-what 8.0.0 has no source change over 7.0.0 beyond going ESM-only
   (`56044b5`), and loading css-what 7.0.0's own ESM build gives the same
   102 us. The ESM namespace object has no getter re-exports.

The matching-side slowdown on large documents (640 `<p>`, 1.33x to 1.48x) is
separate. It is already present at commit `357eecc` and is fixed by the
7.0.0 source even with the old dependencies (118 vs 214 us). Its cause was
not bisected.

## Limits

- One machine (Apple Silicon, macOS, Node 26.5.0). V8's handling of accessor
  properties differs across versions, so the size of the getter effect may
  differ on other Node releases.
- The bisect transpiles each commit with one fixed configuration rather than
  the project's own build, which isolates source changes from build changes
  but is not the published artifact for intermediate commits.
- `hits` (result count) agreed across all engines and builds on every input
  timed.
