# json-p3: valid number literals starting with `0` rejected (`0.5`, `0e1`)

- **Package**: [json-p3](https://github.com/jg-rp/json-p3) 1.3.4 through
  2.3.2 (latest). npm, about 125,000 downloads/week. 1.3.3 is correct.
- **Class**: rejection of valid input (JSONPathSyntaxError), plus acceptance of
  invalid input (`-01`) from the same check.
- **Status**: not reported. No matching issue found on 2026-10-01 (all json-p3
  issues listed; searches for "number literal", "float", "leading zero",
  "exponent" returned nothing).
- **Reproduce**: `npm install && node poc.js`
- **Provenance**: Surfaced by the jsonpath_js grammar-agreement probe on
  2026-09-30 (generated inputs, then minimised by hand).

## What happens

| Query | RFC 9535 | json-p3 1.3.3 | json-p3 2.3.2 |
|---|---|---|---|
| `$[?@.price < 0.5]` | valid | 1 node | JSONPathSyntaxError: invalid number literal '0.5' |
| `$[?@.a == 0.25]` | valid | 1 | JSONPathSyntaxError |
| `$[?@.a == 0e1]` | valid | 1 | JSONPathSyntaxError |
| `$[?@.a == 0e-1]` | valid | 1 | JSONPathSyntaxError |
| `$[?@.a == -0.5]` | valid | 1 | 1 |
| `$[?@.a == 01]` | invalid | 1 (accepted) | JSONPathSyntaxError (correct) |
| `$[?@.a == -01]` | invalid | 1 (accepted) | 1 (still accepted) |

Any positive decimal below 1 written the ordinary way (`0.5`, `0.01`) cannot
appear in a filter. That is a common literal in price or ratio filters.
jsonpath-rfc9535 1.3.0 accepts every valid row and rejects both invalid ones.

## Mechanism

`parseNumber` in `src/path/parse.ts` (line 365 on master, `74ef87f9`;
`dist/json-p3.cjs.js:4126` in 2.3.2):

```ts
const value = stream.current.value;
if (value.startsWith("0") && value.length > 1) {
  throw new JSONPathSyntaxError(`invalid number literal '${value}'`, stream.current);
}
```

The lexer hands the whole literal (`0.5`, `0e1`) to this check, so any literal
with a zero integer part and anything after it fails. A leading `-` bypasses
the check, so `-01` and `-00` are accepted. The check arrived in 1.3.4 with the
changelog entry "Fixed handling of invalid JSONPath integer and float literals
with extra minus signs, leading zeros or too many zeros".

The same author's Python libraries have the same shape of check and the same
class of bug for `0e1`/`0e-1`; see `../jsonpath-rfc9535-py-number-literals/`.

## Specification

RFC 9535 Section 2.3.5.1:

```
number = (int / "-0") [ frac ] [ exp ]
frac   = "." 1*DIGIT
exp    = "e" [ "-" / "+" ] 1*DIGIT
int    = "0" / (["-"] DIGIT1 *DIGIT)
```

`0.5`, `0e1`, `0e-1` are `int "0"` followed by `frac` or `exp`. ABNF literals
are case-insensitive, so `0E1` is also valid. `-01` is not derivable.

The compliance test suite (706 tests, main branch, checked 2026-10-01) has no
valid test with a literal of the form `0.x` or `0eN`, only the invalid `00` and
`01`, which is how this passed json-p3's CTS run. A CTS addition would be a
useful companion report.

## Suggested fix

Reject a zero followed by another digit, with or without a sign:

```ts
if (/^-?0\d/.test(value)) {
  throw new JSONPathSyntaxError(`invalid number literal '${value}'`, stream.current);
}
```

This accepts `0`, `-0`, `0.5`, `0e1`, `-0.5` and rejects `00`, `01`, `-01`,
`-00`, matching the ABNF.
