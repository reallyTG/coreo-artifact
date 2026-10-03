# nwsapi: valid `pseudo-class + [attribute]` selectors rejected since 2.2.12

- **Package**: [nwsapi](https://github.com/dperini/nwsapi) 2.2.12 through 2.2.27
  (npm, ~35M downloads/week; the selector engine jsdom used before v30, and so
  the one behind jest's DOM environment)
- **Class**: correctness regression. Wrong results, or a spurious exception
- **Status**: not reported. No matching issue found on 2026-09-17.
- **Reproduce**: `npm install && node poc.js`

## What happens

A selector combining a pseudo-class, the adjacent-sibling combinator and an
attribute selector is treated as a syntax error:

```
selector: p:not(.x) + [class="cb"]
document: <html><body><p class="a">x</p><div class="cb">y</div></body></html>
expected: 1 match

nwsapi 2.2.9    1 match                                       (correct)
nwsapi 2.2.12   TypeError                                     (see below)
nwsapi 2.2.27   TypeError; 0 matches with VERBOSITY off       (silently wrong)
```

With nwsapi's default configuration the call throws. With `VERBOSITY: false`,
which suppresses exceptions, it returns zero matches instead, so a caller gets
a wrong answer with no signal at all.

Internally the selector has been mangled before parsing. With `LOGERRORS` on,
nwsapi reports:

```
'p:not(.x)+[class,,,cb,,' is not a valid selector
```

The `="` and `"]` of the attribute selector have become commas, which suggests
the placeholder substitution nwsapi applies before parsing is restoring the
wrong spans for this shape.

## Scope

On 2.2.27, with the same document:

| Selector | Result |
|---|---|
| `p:not(.x) + [class="cb"]` | TypeError |
| `p:nth-child(1) + [class="cb"]` | TypeError |
| `p:first-child + [class="cb"]` | TypeError |
| `p + [class="cb"]` | 1 match |
| `p:not(.x) ~ [class="cb"]` | 1 match |
| `p:not(.x) + div` | 1 match |

All three pieces are needed: a pseudo-class on the left compound, the `+`
combinator, and an attribute selector on the right. `~`, `>` and descendant
combinators are unaffected, as is any right-hand side that is not an attribute
selector.

## Versions

Bisected over releases with jsdom 30 as the DOM: 2.2.0, 2.2.2, 2.2.5, 2.2.7 and
2.2.9 all return the correct result; 2.2.12 and every release after it fail.
(2.2.14 fails differently, with `ReferenceError: document is not defined`,
which looks like a separate packaging problem in that release.)

## A second, smaller bug on the same path

`emit()` in `src/nwsapi.js` builds its exception as:

```js
err = new global.DOMException(message, 'SyntaxError');
```

`global` here is the value captured by the module wrapper, which under
CommonJS in Node is not the global object, so `global.DOMException` is
undefined and callers get `TypeError: global.DOMException is not a
constructor` instead of the intended `DOMException`. A caller that catches
`DOMException`, as the DOM specification would lead them to, does not catch
this.

## Impact

jsdom moved to a different engine in v30, but every jsdom before that, and
therefore jest's `jsdom` test environment, resolves selectors through nwsapi.
A test or scraper using `:not(...) + [data-x="y"]` gets an exception or, worse,
a silent zero-match result.

## Provenance

Found while building the `selectors_js` Coreografa subject: 5 of 100
grammar-generated selectors made nwsapi throw where dom-selector and css-select
both succeeded. The 975-character original was reduced to the 24-character case
above by dropping whole compounds and qualifiers.

## A third bug in the same library: stack overflow on long selectors

`node poc-stack.js` in this directory. nwsapi 2.2.27 throws
`RangeError: Maximum call stack size exceeded` once a selector passes a size
that depends on its shape:

| Shape | Smallest crashing size | Selector bytes | dom-selector |
|---|---|---|---|
| descendant path (`div.c0 div.c1 ...`) | 486 steps | 4,263 | ok |
| `:is()` chain | 797 parts | 13,332 | ok |
| class chain (`div.c0.c1...`) | 1,553 parts | 8,211 | ok |
| `:not()` chain | 1,553 parts | 17,529 | ok |
| comma-separated list | no crash up to 20,000 parts | | ok |

dom-selector handles a 119 KB selector in 0.07ms, so this is recursion depth
in nwsapi's matcher rather than an inherent limit. A 4 KB selector is small
enough to arrive from a configuration file or a user-supplied query, and the
crash is a `RangeError`, not the `DOMException` a caller would guard against.

Related: nwsapi issue #172 reports a stack overflow through `:modal`, a
different trigger for what may be the same recursion.
