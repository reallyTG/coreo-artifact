"""Input properties for the tailored orjson subject.

Occurrence counts of the grammar's non-terminals (`count_member`,
`count_str_latin1`, `count_str_one_wide`, `count_key_latin1`, `count_null`,
...) are derived from orjson_tailored.fan by core/grammar_props.py and
need no function here. Declared here is what no occurrence count measures:
document size in bytes and how densely it packs member names, the axis the
3.10.2 change is expected to scale with, and the share of non-ASCII string
content in the Latin-1 range, the axis of the 3.10.6 change.

`PROPERTIES` declares which functions are features; the rest are helpers.
"""

PROPERTIES = ["num_pairs", "doc_bytes", "key_density", "latin1_char_share"]

# num_pairs is exactly the derived member count; keep the domain's column name.
ALIASES = {"num_pairs": ["count_member", "count_more_member"]}


def _decoded_strings(text):
    """Every member name and string value, decoded. The tailored grammar has
    no escapes, so a string is the text between two quotes."""
    return text.split('"')[1::2]


def num_pairs(tree):
    """Members of the root object."""
    return str(tree).count('":')


def doc_bytes(tree):
    """UTF-8 size of the document."""
    return len(str(tree).encode("utf-8"))


def key_density(tree):
    """Member names per byte of document."""
    text = str(tree)
    return text.count('":') / max(1, len(text.encode("utf-8")))


def latin1_char_share(tree):
    """Fraction of non-ASCII string characters that are below U+0100."""
    wide = [c for s in _decoded_strings(str(tree)) for c in s if ord(c) >= 0x80]
    if not wide:
        return 0.0
    return sum(1 for c in wide if ord(c) < 0x100) / len(wide)
