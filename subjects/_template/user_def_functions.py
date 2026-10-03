"""Input properties: the features the models relate to measured cost.

Each property takes a derivation tree and returns a number. Prefer properties
that describe the *shape* of the input, not only its size — size is usually the
obvious driver, and shape is where two implementations actually part company.

`PROPERTIES` declares which functions are features. Anything else defined here
is treated as a helper, so utilities can live alongside without polluting the
model.
"""

PROPERTIES = ["n_items", "max_item_len"]


def _items(tree):
    return [x for x in str(tree).split(",") if x]


def n_items(tree):
    """A size property: how much input there is."""
    return len(_items(tree))


def max_item_len(tree):
    """A shape property: how the input is distributed, not just how big."""
    items = _items(tree)
    return max((len(x) for x in items), default=0)
