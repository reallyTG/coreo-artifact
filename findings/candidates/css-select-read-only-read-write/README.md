# css-select: `:read-only` / `:read-write` cover only typed text controls

- **Package**: [css-select](https://github.com/fb55/css-select) 7.0.0 (current
  release; same source on `master`). Probably 6.0.0 as well, since the aliases
  came in PR [#1497](https://github.com/fb55/css-select/pull/1497) (merged
  2025-02-28) before 6.0.0 was published; not checked. css-select 5.2.2, the
  version cheerio 1.2.0 uses, rejects `:read-only` as an unknown pseudo-class,
  so cheerio users are not affected. 7.0.0 had 3.5M of css-select's 94M
  downloads last week.
- **Class**: wrong answer, silent. Two parts: a partial implementation that
  diverges from the HTML definition by design, and a plain bug inside that
  design (an `<input>` without `type` is not a text control).
- **Status**: not reported. The tracker has only the feature request and PR
  that added these pseudos
  ([#1496](https://github.com/fb55/css-select/issues/1496), #1497); no issue
  about their scope. The css-select README does not list `:read-only` or
  `:read-write` among supported pseudo-classes, so the narrow behaviour is not
  documented anywhere a user would see it.
- **Reproduce**: `npm install && node poc.js`

## What happens

```
selector          Chromium  css-select 7.0.0
input:read-write  1         0                 expected: i1, an untyped input
input:read-only   3         1 (i3)            expected: i2, i3, i4
div:read-write    1         0                 expected: the contenteditable div
p:read-only       1         0                 expected: any non-editable element
:read-only        7         1 (i3)            expected: html, head, body, p, i2, i3, i4
:read-write       3         1 (textarea)      expected: i1, textarea, div
```

Document: `<p>a</p><input id=i1><input id=i2 readonly><input id=i3 type=text
readonly><input id=i4 type=checkbox><textarea></textarea><div
contenteditable>e</div>`. Chromium 151, dom-selector 9.1.4 and nwsapi 2.2.28
agree on every row. The probe's original report, `*:read-only` returning 0
where Chromium returns 6, is the same thing on a document with no readonly
text control.

## Mechanism

`dist/pseudo-selectors/aliases.js` lines 7 and 26-27 in 7.0.0:

```js
const textControl = "input:is([type=text i],[type=search i],[type=url i],...,[type=number i])";
"read-only": `[readonly]:is(textarea, ${textControl})`,
"read-write": `:not([readonly]):is(textarea, ${textControl})`,
```

The comment above it explains the choice: "Only text controls can be made
read-only, since for other controls ... there is no useful distinction". That
reasoning is about which controls honour the `readonly` attribute, which is
right, but HTML's `:read-only` is not "has a readonly attribute": it is the
complement of `:read-write` over all HTML elements. Separately, `textControl`
requires an explicit `type` attribute, so `<input>` and `<input type="">`,
which are in the Text state, match neither pseudo-class. `disabled` is also
ignored, although a disabled text control is not mutable and so is
`:read-only`.

## Specification

HTML Living Standard, §4.16.3 (Pseudo-classes):

- `:read-write` matches `input` elements to which the `readonly` attribute
  applies and that are mutable (not `readonly`, not disabled), `textarea`
  elements that have no `readonly` attribute and are not disabled, and
  elements that are editing hosts or editable and are neither `input` nor
  `textarea`.
- `:read-only` "must match all other HTML elements".

The `type` attribute's missing value default and invalid value default are
the Text state (§4.10.5, the `input` element). Selectors Level 4 §12.1.2
defers to the host language for which elements are mutable.

## Suggested fix

Minimum: treat a missing or invalid `type` as text, so the text-control test
becomes something like
`input:not([type]), input:is([type=text i], ...), input:not(:is([type=hidden i],
[type=checkbox i], ... every other known type))`, and exclude disabled
controls from `:read-write`.

Spec-conformant: define `:read-write` as above (adding `[contenteditable]`
hosts other than `contenteditable="false"`, and `textarea`), and `:read-only`
as `:not(:read-write)` restricted to HTML elements. css-select has no layout
or live editing state, but `contenteditable` is an attribute, so the static
approximation is available. If the maintainer prefers to keep the narrow
meaning, documenting it in the README would at least tell users that
`*:read-only` does not mean what it means in a browser.

## Provenance

Surfaced by the selectors_js grammar-agreement probe on 2026-09-30 (generated
inputs, then minimised by hand).
