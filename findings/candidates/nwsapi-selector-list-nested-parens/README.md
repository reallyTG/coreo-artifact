# nwsapi: `:is(:is(p), p)` rejected when a nested item precedes a comma (fixed in 2.2.28)

- **Package**: [nwsapi](https://github.com/dperini/nwsapi) 2.2.9 (and likely
  earlier) through 2.2.27. Fixed in 2.2.28, released 2026-09-18.
- **Class**: spurious exception on a valid selector. With the default
  configuration the call throws `TypeError: global.DOMException is not a
  constructor` (the broken `emit()` described in
  `findings/nwsapi-sibling-attribute-selector`), not a `DOMException`.
- **Status**: fixed upstream; not worth a new report. Related upstream:
  [#149](https://github.com/dperini/nwsapi/issues/149) (nested `:is()` fails,
  closed "completed" 2025-07-25, but this shape still failed through 2.2.27)
  and [#137](https://github.com/dperini/nwsapi/issues/137). The split was
  replaced by a top-level-comma scanner in the 2.2.28 line (`splitList()`,
  from PR [#199](https://github.com/dperini/nwsapi/pull/199), merged
  2026-09-06).
- **Why a directory anyway**: the versions most installed are the broken
  ones. npm's per-version counts for the last week: 2.2.23 18.2M, 2.2.24 11.0M,
  2.2.28 6.0M, 2.2.27 4.0M. Lockfiles pinned through jsdom ≤ 26 keep the bug.
- **Reproduce**: `npm install && node poc.js`

## What happens

```
selector                  dom-selector  nwsapi 2.2.9   2.2.23     2.2.24     2.2.27     2.2.28
:is(:is(p), p)            2             TypeError      TypeError  TypeError  TypeError  2
:not(:is(p), p)           4             TypeError      TypeError  TypeError  TypeError  4
:has(:nth-child(1), p)    2             TypeError      TypeError  TypeError  TypeError  2
div, :where(:not(p), p)   6             TypeError      TypeError  TypeError  TypeError  6
:is(p, :is(p))            2             2              2          0          2          2
```

Document: `<p id="a">x</p><p>y</p><div>z</div>`. Chromium 151 agrees with
dom-selector on every row.

A functional pseudo-class fails when its argument list contains an item with
its own parentheses followed by a comma. Moving the nested item to the end
of the list works. The last row is a separate, transient bug: 2.2.24 alone
returns 0 for the working form.

## Mechanism

`parse()` splits the top-level selector list with `REX.SplitGroup`
(`src/nwsapi.js` line 64 in 2.2.27, used at line 1782):

```js
SplitGroup: RegExp('(\\([^)]*\\)|\\[[^[]*\\]|\\\\.|[^,])+', 'g'),
```

`\([^)]*\)` treats a parenthesised group as ending at the first `)`, so in
`:is(:is(p), p)` it consumes `(:is(p)` and the following comma is taken as a
top-level separator. The list becomes `[":is(:is(p)", " p)"]`, and compiling
the first half fails. 2.2.28 splits with `splitList()`, which counts
parenthesis and bracket depth and skips quoted strings.

## Specification

Selectors Level 4, §4.2 and §4.3: `:is()` and `:not()` take a
`<complex-real-selector-list>`, and §4.1 defines a selector list as
comma-separated at the top level only. §4.5 does the same for `:has()` with a
relative selector list.

## Suggested fix

Upgrade to nwsapi 2.2.28. For a project that cannot upgrade, the fix is the
depth-counting split from 2.2.28.

## Provenance

Surfaced by the selectors_js grammar-agreement probe on 2026-09-30 (generated
inputs, then minimised by hand).
