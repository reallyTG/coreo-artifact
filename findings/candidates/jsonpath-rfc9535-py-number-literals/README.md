# jsonpath-rfc9535 and python-jsonpath: `0e1` rejected, `1e400` raises OverflowError

- **Packages** (same author, jg-rp; both latest on PyPI, 2026-10-01):
  - [jsonpath-rfc9535](https://github.com/jg-rp/python-jsonpath-rfc9535)
    1.0.0, about 144,000 downloads/week
  - [python-jsonpath](https://github.com/jg-rp/python-jsonpath) 2.2.1, about
    342,000 downloads/week
- **Class**: two bugs in the same function. (a) Rejection of valid number
  literals. (b) Unhandled `OverflowError` from `compile()`, which is not a
  `JSONPathError` subclass, so callers catching the library's errors crash.
- **Status**: not reported. No matching issue found on 2026-10-01 (all issues
  in both repos listed by title; nothing about number literals or overflow).
  Both masters (`e5ad5a82`, `07e0b32c`) still contain the code below.
- **Reproduce**: `python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py`
- **Provenance**: Surfaced by the jsonpath_py grammar-agreement probe on
  2026-09-30 (generated inputs, then minimised by hand).

## What happens

| Query | RFC 9535 | jsonpath-rfc9535 1.0.0 | python-jsonpath 2.2.1 |
|---|---|---|---|
| `$[?@.a == 0e1]` | valid | JSONPathSyntaxError: invalid integer literal | 1 node (strict mode: rejects) |
| `$[?@.a == 0E1]`, `0e+1` | valid | JSONPathSyntaxError | 1 node |
| `$[?@.a == 0e-1]` | valid | JSONPathSyntaxError: invalid float literal | JSONPathSyntaxError |
| `$[?@.a == -0e1]` | valid | 1 node | 1 node |
| `$[?@.a == 1e400]` | valid | OverflowError | OverflowError |
| `$[?@.a < 1e309]` | valid | OverflowError | OverflowError |
| `$[?@.a == 1.0e400]` | valid | 0 nodes | 0 nodes |

jsonpath-rfc9535 (JS) 1.3.0 accepts every row without error. json-p3 by the
same author has the wider version of bug (a); see `../json-p3-zero-number-literal/`.

## Mechanism

Lexer (`jsonpath_rfc9535/lex.py:22-24`, same regexes in
`jsonpath/lex.py:145-147`):

```python
RE_INT = re.compile(r"-?[0-9]+(?:[eE]\+?[0-9]+)?")
RE_FLOAT = re.compile(r"(:?-?[0-9]+\.[0-9]+(?:[eE][+-]?[0-9]+)?)|(-?[0-9]+[eE]-[0-9]+)")
```

`0e1` lexes as INT, `0e-1` as FLOAT. Parser (`jsonpath_rfc9535/parse.py:361-383`):

```python
def parse_integer_literal(self, stream):
    value = stream.current.value
    if value.startswith("0") and len(value) > 1:          # rejects "0e1"
        raise JSONPathSyntaxError("invalid integer literal", ...)
    try:
        return IntegerLiteral(stream.current, value=int(float(value)))  # int(inf)
    except ValueError as err:                             # OverflowError escapes
        raise JSONPathSyntaxError("invalid integer literal", ...) from err

def parse_float_literal(self, stream):
    value = stream.current.value
    if value.startswith("0") and len(value.split(".")[0]) > 1:   # "0e-1" has no "."
        raise JSONPathSyntaxError("invalid float literal", ...)
```

python-jsonpath (`jsonpath/parse.py:624-641`) is the same except that the
integer leading-zero check only runs when `env.strict` is set, and there is no
`try` at all around `int(float(value))`.

Two side notes found while reading:

- The leading-zero checks do not look past a `-`, so `-01` and `-00`, which
  the RFC grammar does not allow, are accepted by both libraries.
- `RE_FLOAT` begins with `(:?` where `(?:` was meant. The group is capturing
  and matches an optional literal colon; harmless for the cases above.

## Specification

RFC 9535 Section 2.3.5.1:

```
number = (int / "-0") [ frac ] [ exp ]
exp    = "e" [ "-" / "+" ] 1*DIGIT
int    = "0" / (["-"] DIGIT1 *DIGIT)
```

`0e1`, `0e+1`, `0e-1` are `int "0"` plus `exp`. ABNF is case-insensitive, so
`0E1` too. `1e400` is well-formed; the RFC leaves comparison of numbers outside
the I-JSON range implementation-defined (Section 2.3.5.2.2), which permits
treating it as infinity or rejecting it with a JSONPath error, but not an
arbitrary Python exception.

The compliance test suite has no valid literal of the form `0eN` and no
overflowing literal, which is how both libraries pass it.

## Suggested fix

- Replace both leading-zero checks with a pattern test on the integer part:
  `re.match(r"-?0[0-9]", value)`.
- In `parse_integer_literal`, catch `OverflowError` alongside `ValueError`, or
  keep the value as a float when `float(value)` is infinite. Note that
  `int(float(value))` also rounds large exact integers written with an
  exponent (`1e23` becomes 99999999999999991611392), so parsing the mantissa
  and exponent with `decimal.Decimal` and converting when integral would be
  more faithful. That rounding is within the RFC's implementation-defined
  range and is not claimed as a bug.
