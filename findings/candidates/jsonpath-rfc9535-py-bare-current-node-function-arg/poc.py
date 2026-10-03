"""jsonpath-rfc9535 1.0.0 and python-jsonpath 2.2.1 (both latest): a bare `@`
evaluates to the raw JSON value instead of a one-node nodelist when the current
node is a scalar. As an existence test (`$[?@]`) that value is then judged by
Python truthiness, so 0, false and "" are dropped. Passed to a NodesType
function parameter (count(), value()) it is handed over as-is. Depending on the value this crashes (TypeError, AttributeError) or
silently gives the wrong answer (strings: len() of the string is used).

    python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py
"""
import jsonpath                    # python-jsonpath
import jsonpath_rfc9535

ENGINES = {
    "jsonpath-rfc9535 1.0.0": lambda q, d: len(jsonpath_rfc9535.compile(q).find(d)),
    "python-jsonpath 2.2.1": lambda q, d: len(jsonpath.compile(q).findall(d)),
}

# Expected results per RFC 9535 (2.4.5 count, 2.4.8 value); jsonpath-rfc9535
# (JS) 1.3.0, json-p3 2.3.2 and jsonpathly 3.0.1 all return these.
CASES = [
    ("$[?@]", [0, False, None, ""], 4),        # existence test: silent wrong answer, 1
    ("$[?!@]", [0, False], 0),                 # silent wrong answer, 2
    ("$[?count(@) == 1]", [True], 1),
    ("$[?count(@) == 1]", [1, [1]], 2),
    ("$[?count(@) == 1]", ["ab"], 1),           # silent wrong answer: 0
    ("$[?value(@) == 1]", [1], 1),
    ("$[?value(@) == 'ab']", ["ab"], 1),        # silent wrong answer: 0
    ("$[?length(value(@)) == 1]", ["x"], 1),
    ("$[?count(@) == 1]", [[1]], 1),            # control: container current node works
]

for query, doc, expected in CASES:
    print(f"{query}  on {doc}  (RFC: {expected})")
    for name, run in ENGINES.items():
        try:
            out = f"{run(query, doc)} nodes"
        except Exception as exc:  # noqa: BLE001
            out = f"{type(exc).__name__}: {exc}"
        print(f"   {name:24} {out}")
