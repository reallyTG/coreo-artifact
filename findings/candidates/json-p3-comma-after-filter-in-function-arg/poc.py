"""jsonpath-rfc9535 1.0.0 (Python): the same bug as poc.js. python-jsonpath
2.2.1 by the same author accepts these queries and is printed as a sibling.

    python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py
"""
import jsonpath                    # python-jsonpath
import jsonpath_rfc9535

ENGINES = {
    "jsonpath-rfc9535 1.0.0": lambda q, d: len(jsonpath_rfc9535.compile(q).find(d)),
    "python-jsonpath 2.2.1": lambda q, d: len(jsonpath.compile(q).findall(d)),
}
CASES = [
    ("$[?count(@[?@, 1]) == 1]", [[1]]),
    ("$[?count(@[?@.a, ?@.b]) > 0]", [[{"a": 1}]]),
    ("$[?count(@[?@ == 1, ?@ == 2]) == 2]", [[1, 2]]),
    ("$[?count(@[1, ?@]) == 1]", [[1]]),
]
for query, doc in CASES:
    print(query)
    for name, run in ENGINES.items():
        try:
            out = f"{run(query, doc)} nodes"
        except Exception as exc:  # noqa: BLE001
            out = f"{type(exc).__name__}: {str(exc).splitlines()[0]}"
        print(f"   {name:24} {out}")
