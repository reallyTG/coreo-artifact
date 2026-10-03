"""Systems under test for the JSON parser shootout (differential subject).

Four independent JSON parsers, same input spec: the C-extension engines
(orjson, ujson) vs the pure-Python-ish stdlib json vs simplejson. Each takes the
document as a string and parses it. They are compared on parse *cost* (runtime +
memory), measured in-process by core/coreografa_metrics.

IMPORTANT: these return None, not the parsed object. A parser naturally returns
a dict for object inputs, and _run_once treats a non-empty dict return as
self-reported metrics (the out-of-process convention) — so returning the parsed
value would corrupt the measurement. We parse for the side effect (the work)
and discard the result; the harness times it and catches any parse exception.

WHY THE K-LOOP: a single JSON parse here is sub-microsecond, close enough to
the clock's own resolution that one parse is mostly noise. Parsing K times lifts
the measurement well clear of it. The harness converts the tree to a string
once, outside the timed region, and hands the SUT that string.
"""
import json

import orjson
import ujson
import simplejson

# Parses per measurement, so K * (fastest parse) sits well above clock
# resolution; see module docstring.
K_PARSE = 3000


def json_stdlib(text):
    for _ in range(K_PARSE):
        json.loads(text)


def json_orjson(text):
    for _ in range(K_PARSE):
        orjson.loads(text)


def json_ujson(text):
    for _ in range(K_PARSE):
        ujson.loads(text)


def json_simplejson(text):
    for _ in range(K_PARSE):
        simplejson.loads(text)
