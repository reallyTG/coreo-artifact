"""jsonpath-rfc9535 1.0.0 and python-jsonpath 2.2.1 (both latest, same author):
number literals in filters.

1. Valid literals with a zero integer part and an exponent are rejected:
   jsonpath-rfc9535 rejects 0e1, 0E1, 0e+1 and 0e-1; python-jsonpath rejects 0e-1.
2. An integer-shaped literal too large for a double (1e400, 1e309) makes
   compile() raise OverflowError instead of a JSONPathError.

    python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py
"""
import jsonpath                    # python-jsonpath
import jsonpath_rfc9535

ENGINES = {
    "jsonpath-rfc9535 1.0.0": lambda q, d: len(jsonpath_rfc9535.compile(q).find(d)),
    "python-jsonpath 2.2.1": lambda q, d: len(jsonpath.compile(q).findall(d)),
}

CASES = [
    ("$[?@.a == 0e1]", [{"a": 0}]),       # valid per RFC 9535 2.3.5.1, 1 node
    ("$[?@.a == 0E1]", [{"a": 0}]),       # valid, 1
    ("$[?@.a == 0e+1]", [{"a": 0}]),      # valid, 1
    ("$[?@.a == 0e-1]", [{"a": 0}]),      # valid, 1
    ("$[?@.a == -0e1]", [{"a": 0}]),      # control: accepted by both
    ("$[?@.a == 1e400]", [{"a": 1}]),     # valid, 0 nodes (no crash)
    ("$[?@.a < 1e309]", [{"a": 1}]),      # valid, 1 node
    ("$[?@.a == 1.0e400]", [{"a": 1}]),   # control: float-shaped literal does not crash
]

for query, doc in CASES:
    print(query)
    for name, run in ENGINES.items():
        try:
            out = f"{run(query, doc)} nodes"
        except Exception as exc:  # noqa: BLE001
            out = f"{type(exc).__name__}: {str(exc).splitlines()[0]}"
        print(f"   {name:24} {out}")
