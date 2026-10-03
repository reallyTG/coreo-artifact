# nwsapi: `[att~="a b"]` matches every element instead of none

- **Package**: [nwsapi](https://github.com/dperini/nwsapi) 2.2.12 through 2.2.28
  (current release, and current `master`). About 58M downloads/week; the
  selector engine of jsdom up to 26.x, which is the jsdom that
  jest-environment-jsdom 30 depends on (`jsdom ^26.1.0` → `nwsapi ^2.2.16`, so a
  fresh install gets 2.2.28).
- **Class**: wrong answer, silent. No exception.
- **Status**: not reported. No matching issue or PR in the tracker on
  2026-10-01 (all 226 issues and PRs listed and searched for `~=`,
  "whitespace", "space"; the nearest is #84, about escaped values, closed 2023).
- **Reproduce**: `npm install && node poc.js`

## What happens

```
document: <p title="x y">a</p><p title="  ">b</p><p>c</p><div class="a b">d</div>

selector                  dom-selector  nwsapi 2.2.9  nwsapi 2.2.12 nwsapi 2.2.24 nwsapi 2.2.28
p[title~="x y"]           0             0             3             3             3
[title~=" "]              0             0             7             7             7
div[class~="a b"]         0             0             1             1             1
p:not([title~="x y"])     3             3             0             0             0
p[title~=""]              0             1             1             1             1
```

When the value of a `~=` attribute selector contains a space, nwsapi drops the
attribute test and keeps the rest of the compound. `p[title~="x y"]` selects
every `p`, including ones with no `title` at all, and `:not([title~="x y"])`
selects nothing. Chromium 151 (Playwright's Chrome for Testing), dom-selector
9.1.4 and css-select 7.0.0 all return 0 for the first three rows.

## Mechanism

`src/nwsapi.js` in 2.2.27, the attribute resolver in `compileSelector()`
(line 1110 onwards; line 1275 in 2.2.28, line 1366 on `master`):

```js
} else if (match[2] == '~=' && match[4].includes(' ')) {
  // whitespace separated list but value contains space
  break;
}
```

The `break` leaves the `switch` before `source` is wrapped in the attribute
condition, so the compound compiles as if the attribute selector were absent.
The comment shows the intent was "this can never match", but the code
implements "this always matches". The check also looks only for U+0020, so a
tab or newline in the value takes the regex path instead.

A second, smaller bug sits two lines above: for an empty value (`~=""`) the
resolver substitutes the regex `^\s+$`, so an attribute consisting only of
whitespace matches (`p[title~=""]` selects `<p title="  ">`). This one is
present in 2.2.9 as well.

## Versions

2.2.9 and 2.2.10 return 0; 2.2.12, 2.2.13, 2.2.16, 2.2.20, 2.2.23, 2.2.24,
2.2.25, 2.2.27 and 2.2.28 return every element. The regression arrived in 2.2.12,
the same release as the `pseudo + [attr]` regression in
`findings/nwsapi-sibling-attribute-selector`.

## Specification

Selectors Level 4, §6.1 (Attribute presence and value selectors), on
`[att~=val]`: "If 'val' contains whitespace, it will never represent anything
(since the words are separated by spaces). Also if 'val' is the empty string,
it will never represent anything."

## Suggested fix

Emit a condition that is always false instead of breaking out, and test for
any whitespace and for the empty string:

```js
} else if (match[2] == '~=' && (match[4] === '' || /\s/.test(match[4]))) {
  // Selectors 4 §6.1: never represents anything
  source = 'if(false){' + source + '}';
  break;
}
```

(with the `match[4] === ''` branch above it removed for `~=`). Applied to a
scratch copy of 2.2.27, this gives 0, 0, 0, 3 and 0 for the five rows above,
and leaves `p[title~="x"]` (1) and `p[title]` (2) unchanged.

## Impact

Any jsdom ≤ 26 user, including jest's default DOM environment, gets extra
matches from a `~=` selector whose value has a space. Such values come from
building a selector out of data, for example
`[class~="${className}"]` with a multi-class string, where the correct answer
is zero matches. With `:not()` the error inverts and hides everything.

## Provenance

Surfaced by the selectors_js grammar-agreement probe on 2026-09-30 (generated
inputs, then minimised by hand). It was found during triage while
checking a css-select `[title~=""]` candidate against the
other engines; `[title~=" "]` returned 9 matches from nwsapi where Chromium
returned 0.
