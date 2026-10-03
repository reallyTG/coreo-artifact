# The input language for this subject.
#
# Two rules that are easy to get wrong:
#
#   1. One production per line. A `|` alternative continued on the next line is
#      a syntax error ("no viable alternative at input '|'"), even though it
#      reads naturally. Keep every alternative on the line with its `::=`.
#   2. Bound your repetitions. `<item>{0,50}` gives the stratifier something to
#      band and stops generation from wandering into inputs too large to
#      measure. Unbounded recursion is capped only by max_nodes, which is a
#      blunter instrument.

<start> ::= <item> <more_item>{0,50}
<more_item> ::= "," <item>
<item> ::= <digit> | <digit> <item>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
