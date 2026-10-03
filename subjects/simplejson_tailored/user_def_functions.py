"""Input properties for the tailored simplejson subject.

Occurrence counts of the grammar's non-terminals (`count_member`,
`count_number`, `count_string`, `count_null`, ...) are derived from
simplejson_tailored.fan by core/grammar_props.py and need no function here.
Declared here is what no occurrence count measures: document size in bytes
and how densely it packs member names, the quantity the e2e5f0b change
(one memo-dict operation per member name) is expected to scale with.

`PROPERTIES` declares which functions are features; the rest are helpers.
"""

PROPERTIES = ["num_pairs", "doc_bytes", "key_density"]

# num_pairs is exactly the derived member count; keep the domain's column name.
ALIASES = {"num_pairs": ["count_member", "count_more_member"]}


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
