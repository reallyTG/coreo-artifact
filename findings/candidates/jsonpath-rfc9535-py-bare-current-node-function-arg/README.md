# jsonpath-rfc9535 and python-jsonpath: bare `@` on a scalar is a raw value, not a node

- **Packages** (same author, jg-rp; both latest on PyPI, 2026-10-01):
  - [jsonpath-rfc9535](https://github.com/jg-rp/python-jsonpath-rfc9535)
    1.0.0, about 144,000 downloads/week
  - [python-jsonpath](https://github.com/jg-rp/python-jsonpath) 2.2.1, about
    342,000 downloads/week
- **Class**: silent wrong answers (`$[?@]` drops `0`, `false`, `""`), and
  unhandled exceptions (TypeError, AttributeError) from `find()` when `@` is
  passed to `count()` or `value()`.
- **Status**: not reported. No matching issue found on 2026-10-01 (all issues
  in both repos listed by title). Both masters (`e5ad5a82`, `07e0b32c`) still
  contain the code below.
- **Reproduce**: `python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py`
- **Provenance**: Surfaced by the jsonpath_py grammar-agreement probe on
  2026-09-30 (generated inputs, then minimised by hand). The probe reported the
  `count(@)`/`value(@)` crashes; the existence-test variant was found during
  triage by following the same code path.

## What happens

| Query | Document | RFC 9535 | both Python libraries |
|---|---|---|---|
| `$[?@]` | `[0, false, null, ""]` | 4 nodes | 1 (only `null`) |
| `$[?!@]` | `[0, false]` | 0 | 2 |
| `$[?count(@) == 1]` | `[true]` | 1 | TypeError: object of type 'bool' has no len() |
| `$[?count(@) == 1]` | `[1, [1]]` | 2 | TypeError |
| `$[?value(@) == 1]` | `[1]` | 1 | TypeError: object of type 'int' has no len() |
| `$[?length(value(@)) == 1]` | `["x"]` | 1 | AttributeError ('str' object has no attribute 'value' / 'obj') |
| `$[?count(@) == 1]` | `["ab"]` | 1 | 0 (counts the string's characters) |
| `$[?value(@) == 'ab']` | `["ab"]` | 1 | 0 |
| `$[?count(@) == 1]` (control) | `[[1]]` | 1 | 1 |

jsonpath-rfc9535 (JS) 1.3.0, json-p3 2.3.2 and jsonpathly 3.0.1 return the RFC
result on every row. For the crashing rows, one scalar anywhere in the array
makes the whole query raise.

## Mechanism

`RelativeFilterQuery.evaluate`, `jsonpath_rfc9535/filter_expressions.py:288-295`:

```python
if not isinstance(context.current, (list, dict)):
    if self.query.empty():
        return context.current          # raw value, not a nodelist
    return JSONPathNodeList()
return JSONPathNodeList(self.query.find(context.current))
```

The raw value then reaches two consumers that expect a nodelist:

- Existence tests go through `_is_truthy` (same file, 412-420), which returns
  `bool(obj)` for anything that is not an empty nodelist, `NOTHING` or `None`.
  So `0`, `False` and `""` fail an existence test that the RFC says always
  succeeds for `@`.
- `FunctionExtension._unpack_node_lists` (340-364) passes non-nodelist
  arguments through unchanged, so `Count.__call__` does `len(value)` and
  `Value.__call__` does `len(nodes)` and `nodes[0].value`
  (`function_extensions/value.py:22-24`). A string survives `len()`, which is
  the silent wrong answer.

python-jsonpath has the identical shortcut in `jsonpath/filter.py:531-537`
(async twin at 546-552) and the same function-argument unpacking at 662-663.

## Specification

RFC 9535 Section 2.3.5.1: `rel-query = current-node-identifier segments`, and
`segments` may be empty, so `@` alone is a filter query selecting exactly the
current node. Section 2.3.5.2.1: an existence test "tests whether the query
selects at least one node", which for `@` is always true. Section 2.4.1: a
filter query as a function argument is NodesType. Section 2.4.5 (count) counts
the nodes of that nodelist; Section 2.4.8 (value) returns the value of its
single node.

The compliance test suite's only `$[?@]` test ("filter, existence, without
segments") uses the document `{"a": 1, "b": null}`, whose values are both
truthy under `_is_truthy`, and no test applies `count(@)` or `value(@)` to a
scalar. That is why both libraries pass the suite.

## Suggested fix

Return a one-node nodelist from the scalar shortcut and let comparisons and
ValueType parameters unwrap it, as they already do for `@.a`:

```python
if not isinstance(context.current, (list, dict)):
    if self.query.empty():
        return JSONPathNodeList([JSONPathNode(value=context.current, location=..., parent=..., root=context.root)])
    return JSONPathNodeList()
```

A monkeypatch doing this against jsonpath-rfc9535 1.0.0 made every failing row
above return the RFC result, and left `$[?@ == 1]`, `$[?@ < 2]`,
`$[?length(@) == 2]`, `$[?match(@, 'a.')]` and `$[?@ == @]` unchanged. The full
compliance suite was not rerun against the patch.
