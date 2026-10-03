# jsonpath-ng: indexing a non-list value raises instead of returning no match

- **Package**: [jsonpath-ng](https://github.com/h2non/jsonpath-ng) 1.8.0 (PyPI, ~12.7M downloads/week)
- **Class**: unhandled exception on a valid query (robustness), plus one wrong result
- **Status**: partly known. Issue
  [#93](https://github.com/h2non/jsonpath-ng/issues/93) (open since 2021)
  reports the `KeyError` shape, wildcard followed by an index. The `TypeError`
  shape below was not found in the tracker, and
  [#104](https://github.com/h2non/jsonpath-ng/issues/104) covers a different
  operation. Treat this as a likely duplicate in root cause and check with the
  maintainer before filing.
- **Reproduce**: `python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py`

## What happens

```
query $.a[0]   document {"a": 1}
  jsonpath-ng        TypeError: object of type 'int' has no len()
  jsonpath-rfc9535   0 results

query $.a[0]   document {"a": true}
  jsonpath-ng        TypeError: object of type 'bool' has no len()

query $..a[0]  document {"a": 1}
  jsonpath-ng        TypeError: object of type 'int' has no len()

query $[*][0]  document {"a": 1}
  jsonpath-ng        KeyError: 0

query $.a[*]   document {"a": 1}
  jsonpath-ng        1 result          <- wrong: a wildcard over a scalar
  jsonpath-rfc9535   0 results
```

Asking for element 0 of something that is not a list selects nothing, which is
what python-jsonpath, jsonpath-rfc9535 and jsonpath-python all return. RFC 9535
says an index selector applied to a non-array selects nothing.

## Impact

Applying a caller-supplied path to caller-supplied JSON is the normal use of
this library, and either side is enough to trigger this: the same path crashes
or not depending on the document's shape. A service doing that gets an
exception from `find()` with no documented type to catch, so the failure
surfaces as a 500 rather than an empty result.

## Provenance

Found by the `jsonpath_py` Coreografa subject: `$[*].*[0]` appeared in the
generated corpus, where jsonpath-ng was the only one of four engines to fail.
The reduction to `$.a[0]` over `{"a": 1}` was done by hand.
