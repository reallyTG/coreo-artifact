# css-select: `:scope` matches nothing when the context is a Document

- **Package**: [css-select](https://github.com/fb55/css-select) 5.2.2 and
  7.0.0 (current release; also current `master` source). About 94M
  downloads/week, most through cheerio (cheerio 1.2.0 depends on css-select
  5.2.2) and svgo. Other versions not checked.
- **Class**: wrong answer, silent. No exception.
- **Status**: not reported. Tracker searched 2026-10-01 (all issues and PRs
  listed, grepped for "scope"). Nearest are
  [#1767](https://github.com/fb55/css-select/issues/1767) /
  [#1770](https://github.com/fb55/css-select/pull/1770) (open: multi-node
  contexts compared by reference instead of the adapter's `equals`), a
  different defect in the same function, and
  [#343](https://github.com/fb55/css-select/issues/343) (2021, request to
  support `:scope`).
- **Reproduce**: `npm install && node poc.js`

## What happens

```
document: <html><head></head><body><p>a</p></body></html>

selector        Chromium  css-select 7.0.0  css-select 5.2.2  cheerio 1.2.0
:scope          1         0                 0                 0
html:scope      1         0                 0                 0
:scope > body   1         0                 0                 0
:scope body     1         0                 0                 0
:scope > html   0         0                 0                 0
:root > body    1         1                 1                 1
```

The call is `CSSselect.selectAll(selector, parseDocument(html))`; cheerio's
`$(selector)` gives the same result. Chromium 151,
dom-selector 9.1.4 and nwsapi 2.2.28 all treat `:scope` in
`document.querySelectorAll()` as the `html` element. css-select matches
nothing for any selector containing `:scope`. That also rules out the reading
in which `:scope` is the Document node itself, since then `:scope > html`
would match.

## Mechanism

css-select 7.0.0, `dist/pseudo-selectors/filters.js` lines 105-115
(`src/pseudo-selectors/filters.ts` line 141 on `master`):

```js
scope(next, rule, options, context) {
    const { equals } = options;
    if (!context || context.length === 0) {
        // Equivalent to :root
        return filters["root"](next, rule, options);
    }
    if (context.length === 1) {
        return (element) => equals(context[0], element) && next(element);
    }
    ...
```

`selectAll(sel, document)` sets the context to `[document]`. The filter then
compares each candidate element with the Document node, which never succeeds.
`:scope > html` fails too, because the child combinator walks up with
`getElementParent()` (`dist/helpers/querying.js:115`), which returns `null`
for a non-element parent, so the Document is never reached.

`absolutize()` in `dist/compile.js:20` already recognises the case; it carries
the comment `// TODO Use better check if the context is a document` and treats
a context of non-elements as no context. The `scope` filter lacks the same
check.

## Specification

Selectors Level 4, §8.4 (`:scope`): "In some contexts, selectors are matched
with respect to one or more scoping roots, such as when calling the
querySelector() method in [DOM]. The :scope pseudo-class represents this
scoping root, and may be either a true element or a virtual one (such as a
DocumentFragment). If there is no scoping root then :scope represents the
root of the tree". For a Document scoping root all three browser-grade
engines above match the root element. Under either reading css-select's
result is wrong: it matches neither the root element nor anything that is a
child of the Document.

## Suggested fix

Fall back to `:root` when the context holds no element:

```js
if (!context || context.length === 0 ||
    !context.some((node) => options.adapter.isTag(node))) {
    // Equivalent to :root
    return filters["root"](next, rule, options);
}
```

Applied to a scratch copy of 7.0.0, all rows match Chromium, and an element
context is unaffected (`selectAll(':scope > p', body)` still returns 1).

## Provenance

Surfaced by the selectors_js grammar-agreement probe on 2026-09-30 (generated
inputs, then minimised by hand).
