"""jsonpath-ng 1.8.0: indexing a non-list value raises instead of not matching.

`$.a[0]` against `{"a": 1}` asks for element 0 of something that is not a
list. Three other Python JSONPath libraries return no matches. jsonpath-ng
raises an uncaught TypeError out of `find()`, so a caller applying a
user-supplied path to user-supplied JSON gets an exception it has no reason to
expect and, in a service, a failed request.

    python -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/python poc.py

python-jsonpath and jsonpath-python both provide a module named `jsonpath` and
cannot share an environment, so this script reports whichever of the four are
importable and skips the rest. Installing jsonpath-ng alone is enough to see
the bug; the others are there as the comparison.
"""
import json

CASES = [
    ("$.a[0]", {"a": 1}),        # index into an int
    ("$.a[0]", {"a": True}),     # index into a bool
    ("$..a[0]", {"a": 1}),       # same, reached by a descendant segment
    ("$[*][0]", {"a": 1}),       # wildcard then index (issue #93)
    ("$.a[*]", {"a": 1}),        # wildcard over a non-list: a wrong result, not a crash
]


def engines():
    out = {}
    try:
        import jsonpath_ng.ext as ng
        out["jsonpath-ng"] = lambda q, d: len(ng.parse(q).find(d))
    except ImportError:
        pass
    try:
        import jsonpath_rfc9535 as r9
        out["jsonpath-rfc9535"] = lambda q, d: len(r9.find(q, d))
    except ImportError:
        pass
    try:
        import jsonpath as pj              # python-jsonpath
        if hasattr(pj, "findall"):
            out["python-jsonpath"] = lambda q, d: len(pj.findall(q, d))
        else:                              # jsonpath-python
            out["jsonpath-python"] = lambda q, d: len(pj.JSONPath(q).parse(d) or [])
    except ImportError:
        pass
    return out


def main():
    libs = engines()
    print("libraries:", ", ".join(libs) or "none installed")
    for query, doc in CASES:
        print(f"\nquery {query}   document {json.dumps(doc)}")
        for name, fn in libs.items():
            try:
                print(f"  {name:<18} {fn(query, doc)} results")
            except Exception as exc:                      # noqa: BLE001
                print(f"  {name:<18} {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
