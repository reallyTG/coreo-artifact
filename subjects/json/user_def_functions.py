"""Structural properties of a generated JSON tree — the axes targeting reasons
over. All but depth follow the generic "count occurrences of nonterminal X"
pattern.
"""
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

PROPERTIES = ["depth", "num_pairs", "num_arrays", "num_numbers", "total_string_len"]

# Declared properties that are exactly a grammar-derived non-terminal count
# (verified equal on 30 sampled corpus inputs). The alias suppresses the
# derived duplicate so the subject keeps its own column, rather than gaining
# a second axis measuring the same thing. The declared implementation is the
# one that runs.
ALIASES = {
    "num_pairs": "count_member",
    "num_arrays": "count_array",
    "num_numbers": "count_number",
    "total_string_len": "count_char",
}



def _count(tree: DerivationTree, symbol_name: str) -> int:
    """Number of nodes whose symbol is `symbol_name` in the tree."""
    target = NonTerminal(symbol_name)
    count = 1 if tree.symbol == target else 0
    for child in tree.children:
        count += _count(child, symbol_name)
    return count


_CONTAINERS = (NonTerminal("<object>"), NonTerminal("<array>"))


def depth(tree: DerivationTree) -> int:
    """JSON nesting depth: the most <object>/<array> nodes on any root-to-leaf
    path (0 for a scalar document) -- the axis where recursion limits diverge
    across engines.

    This is not the raw derivation-tree depth. The RFC 8259 grammar writes
    `ws` and `*char` as recursion, so derivation depth would mostly measure
    whitespace runs and string length rather than nesting.
    """
    here = 1 if tree.symbol in _CONTAINERS else 0
    if not tree.children:
        return here
    return here + max(depth(child) for child in tree.children)


def num_pairs(tree: DerivationTree) -> int:
    """Total key/value pairs across all objects (document breadth+depth)."""
    return _count(tree, "<member>")


def num_arrays(tree: DerivationTree) -> int:
    return _count(tree, "<array>")


def num_numbers(tree: DerivationTree) -> int:
    return _count(tree, "<number>")


def total_string_len(tree: DerivationTree) -> int:
    """Total string payload = number of <char> nodes across all strings."""
    return _count(tree, "<char>")
