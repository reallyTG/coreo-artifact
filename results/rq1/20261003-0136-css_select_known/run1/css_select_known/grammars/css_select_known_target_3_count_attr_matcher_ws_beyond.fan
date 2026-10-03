from fandango.language.symbols import NonTerminal as _CoreoNT

def _coreografa_count(tree, target):
    n = 1 if tree.symbol == target else 0
    for _c in tree.children:
        n += _coreografa_count(_c, target)
    return n

def count_complex_selector_list(tree):
    return _coreografa_count(tree, _CoreoNT('<complex_selector_list>'))

def count_complex_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<complex_selector>'))

def count_combinator(tree):
    return _coreografa_count(tree, _CoreoNT('<combinator>'))

def count_subclass_selectors(tree):
    return _coreografa_count(tree, _CoreoNT('<subclass_selectors>'))

def count_type_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<type_selector>'))

def count_wq_name(tree):
    return _coreografa_count(tree, _CoreoNT('<wq_name>'))

def count_pseudo_class_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<pseudo_class_selector>'))

def count_id_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<id_selector>'))

def count_class_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<class_selector>'))

def count_attribute_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<attribute_selector>'))

def count_pseudo_class_ident(tree):
    return _coreografa_count(tree, _CoreoNT('<pseudo_class_ident>'))

def count_pseudo_class_function(tree):
    return _coreografa_count(tree, _CoreoNT('<pseudo_class_function>'))

def count_name(tree):
    return _coreografa_count(tree, _CoreoNT('<name>'))

def count_attr_matcher_ws(tree):
    return _coreografa_count(tree, _CoreoNT('<attr_matcher_ws>'))

def count_attr_modifier(tree):
    return _coreografa_count(tree, _CoreoNT('<attr_modifier>'))

def count_attr_value(tree):
    return _coreografa_count(tree, _CoreoNT('<attr_value>'))

def count_lparen(tree):
    return _coreografa_count(tree, _CoreoNT('<lparen>'))

def count_relative_selector_list(tree):
    return _coreografa_count(tree, _CoreoNT('<relative_selector_list>'))

def count_nth_function(tree):
    return _coreografa_count(tree, _CoreoNT('<nth_function>'))

def count_rparen(tree):
    return _coreografa_count(tree, _CoreoNT('<rparen>'))

def count_more_complex_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<more_complex_selector>'))

def count_lang_range(tree):
    return _coreografa_count(tree, _CoreoNT('<lang_range>'))

def count_namechar(tree):
    return _coreografa_count(tree, _CoreoNT('<namechar>'))

def count_attr_value_words(tree):
    return _coreografa_count(tree, _CoreoNT('<attr_value_words>'))

def count_attr_ident(tree):
    return _coreografa_count(tree, _CoreoNT('<attr_ident>'))

def count_more_relative_selector(tree):
    return _coreografa_count(tree, _CoreoNT('<more_relative_selector>'))

def count_comma(tree):
    return _coreografa_count(tree, _CoreoNT('<comma>'))

def count_lang_tag(tree):
    return _coreografa_count(tree, _CoreoNT('<lang_tag>'))

def count_more_value_word(tree):
    return _coreografa_count(tree, _CoreoNT('<more_value_word>'))

def count_relative_combinator(tree):
    return _coreografa_count(tree, _CoreoNT('<relative_combinator>'))

def count_complex_selector_in_has(tree):
    return _coreografa_count(tree, _CoreoNT('<complex_selector_in_has>'))

def count_digits(tree):
    return _coreografa_count(tree, _CoreoNT('<digits>'))

def count_an_a(tree):
    return _coreografa_count(tree, _CoreoNT('<an_a>'))

def count_signed_integer(tree):
    return _coreografa_count(tree, _CoreoNT('<signed_integer>'))

def count_an_b_sign(tree):
    return _coreografa_count(tree, _CoreoNT('<an_b_sign>'))

def count_sign(tree):
    return _coreografa_count(tree, _CoreoNT('<sign>'))

def count_subclass_selectors_in_has(tree):
    return _coreografa_count(tree, _CoreoNT('<subclass_selectors_in_has>'))

def count_pseudo_class_selector_in_has(tree):
    return _coreografa_count(tree, _CoreoNT('<pseudo_class_selector_in_has>'))

def count_pseudo_class_function_in_has(tree):
    return _coreografa_count(tree, _CoreoNT('<pseudo_class_function_in_has>'))

def count_complex_selector_list_in_has(tree):
    return _coreografa_count(tree, _CoreoNT('<complex_selector_list_in_has>'))

def count_more_complex_selector_in_has(tree):
    return _coreografa_count(tree, _CoreoNT('<more_complex_selector_in_has>'))

def count_node(tree):
    return _coreografa_count(tree, _CoreoNT('<node>'))

def count_phrasing_element(tree):
    return _coreografa_count(tree, _CoreoNT('<phrasing_element>'))

def count_em(tree):
    return _coreografa_count(tree, _CoreoNT('<em>'))

def count_phrasing_content(tree):
    return _coreografa_count(tree, _CoreoNT('<phrasing_content>'))

def count_text_run(tree):
    return _coreografa_count(tree, _CoreoNT('<text_run>'))

def count_tchar(tree):
    return _coreografa_count(tree, _CoreoNT('<tchar>'))

def count_phrasing_item(tree):
    return _coreografa_count(tree, _CoreoNT('<phrasing_item>'))

def count_input(tree):
    return _coreografa_count(tree, _CoreoNT('<input>'))

def count_type_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<type_attr>'))

def count_b(tree):
    return _coreografa_count(tree, _CoreoNT('<b>'))

def count_span(tree):
    return _coreografa_count(tree, _CoreoNT('<span>'))

def count_a(tree):
    return _coreografa_count(tree, _CoreoNT('<a>'))

def count_attrs(tree):
    return _coreografa_count(tree, _CoreoNT('<attrs>'))

def count_href_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<href_attr>'))

def count_title_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<title_attr>'))

def count_id_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<id_attr>'))

def count_class_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<class_attr>'))

def count_class_list(tree):
    return _coreografa_count(tree, _CoreoNT('<class_list>'))

def count_lang_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<lang_attr>'))

def count_data_attr(tree):
    return _coreografa_count(tree, _CoreoNT('<data_attr>'))

def count_p(tree):
    return _coreografa_count(tree, _CoreoNT('<p>'))

def count_section(tree):
    return _coreografa_count(tree, _CoreoNT('<section>'))

def count_flow_content(tree):
    return _coreografa_count(tree, _CoreoNT('<flow_content>'))

def count_flow_item(tree):
    return _coreografa_count(tree, _CoreoNT('<flow_item>'))

def count_div(tree):
    return _coreografa_count(tree, _CoreoNT('<div>'))

def count_more_node(tree):
    return _coreografa_count(tree, _CoreoNT('<more_node>'))

"""Input properties for the CSS selector subject.

Occurrence counts of grammar non-terminals (`count_compound`, `count_simple`,
`count_node`, ...) are derived from the grammar by `core/grammar_props.py`.
Declared here is only what no occurrence count measures: document nesting
depth, pseudo-class nesting depth in the selector, and the byte size of each
half.
"""

SEPARATOR = "\n@@@\n"

PROPERTIES = [
    "doc_depth",
    "doc_bytes",
    "selector_len",
    "selector_nesting",
]

# HTML void elements the grammar can emit: a start tag with no end tag.
# A plain string, not a one-element tuple: str.startswith accepts either, and
# the tuple literal ("input",) is rejected by Fandango's embedded-Python parser
# when this file is pasted into a targeted grammar, which killed every targeted
# request in the 2026-10-01 run 1 (see the commit message).
VOID = "input"


def _split(tree):
    selector, _, doc = str(tree).partition(SEPARATOR)
    return selector, doc


def doc_depth(tree):
    """Deepest element nesting, counted over the tag stream.

    Depth is what makes a descendant combinator expensive: matching `a b`
    walks ancestors, so the engines separate most where documents are deep.
    """
    doc = _split(tree)[1]
    depth = best = 0
    i = 0
    while i < len(doc):
        if doc[i] == "<":
            if doc[i + 1:i + 2] == "/":
                depth -= 1
            elif doc[i + 1:i + 2] == "!":
                pass                      # <!DOCTYPE html>
            elif doc.startswith(VOID, i + 1):
                best = max(best, depth + 1)
            else:
                depth += 1
                best = max(best, depth)
            close = doc.find(">", i)
            i = len(doc) if close < 0 else close + 1
        else:
            i += 1
    return best


def doc_bytes(tree):
    return len(_split(tree)[1])


def selector_len(tree):
    return len(_split(tree)[0])


def selector_nesting(tree):
    """Deepest nesting of functional pseudo-classes (:is, :where, :not, :has,
    :nth-*, :lang). The selector alphabet has no parentheses anywhere else, so
    bracket depth is exactly this."""
    sel = _split(tree)[0]
    depth = best = 0
    for ch in sel:
        if ch == "(":
            depth += 1
            best = max(best, depth)
        elif ch == ")":
            depth -= 1
    return best

# CSS selector plus HTML document, for five JavaScript selector engines.
#
# One input encodes both halves, separated by a marker line:
#
#     <selector>
#     @@@
#     <html document>
#
# The runner splits on "\n@@@\n"; the selector is one line and neither half
# can produce "@".
#
# SELECTOR HALF. Transcribes the grammar of W3C Selectors Level 4 (§18
# "Grammar") rule by rule, with the argument grammars of the functional
# pseudo-classes taken from their own sections and An+B from CSS Syntax
# Level 3 §6. Rule names follow the spec's, with `-` written `_`. Every rule
# carries the section it transcribes.
#
# DOCUMENT HALF. A declared subset of HTML syntax (WHATWG HTML §13.1 "Writing
# HTML documents"): a well-formed element tree with matched start and end
# tags, quoted attribute values, no duplicate attributes, one void element
# (<input>), and content models respected so that the HTML tree builder never
# re-parents anything (no block element inside <p>, no <a> inside <a>). Full
# HTML is not a context-free language: the tree builder's error recovery
# (implied end tags, adoption agency, foster parenting) is an algorithm, not
# a grammar. This subset is the part where source nesting equals DOM nesting,
# which is what makes `doc_depth` and the tree measures mean anything.
#
# Everything that can grow uses `*`, `+` or recursion: compounds per complex
# selector, members of every selector list, subclass selectors per compound,
# pseudo-class nesting, An+B digits, class lists, attribute values, element
# children and nesting depth. Sizes come from `max_repetition` and `max_nodes`
# in example.py and from structural requests, never from a cap written here.
#
# DEVIATIONS from the specs above. Classes: 1 language-preserving rewrite
# (distribution only); 2 restriction to a named profile of another spec;
# 3 finite lexical vocabulary; 4 construct some engine does not implement at
# all (rejects or throws on >=95% of per-construct probes, 30-40 probes per
# construct per engine, probed 2026-09-30 with nwsapi 2.2.27/2.2.26/2.2.25,
# dom-selector 9.1.4, css-select 7.0.0).
#
# | Departure                                                       | Class | Evidence / reason |
# |-----------------------------------------------------------------|-------|-------------------|
# | Selector-side repetition (`#` lists, <subclass-selector>*, digits, value words) written as right recursion instead of `*` | 1 | same language; geometric length so the selector does not eat the node budget the document needs (with `*` at max_repetition 12, documents collapsed to one element) |
# | Optional whitespace and optional attributes spelled out as alternatives, never as nullable rules | 1 | same language; Fandango's parser failed on its own output (`:is(a,b)`) with a nullable rule inside parentheses |
# | Element content written as maximal text runs between elements instead of `<child>*` over a nullable text leaf | 1 | same language, one parse per document; the ambiguous form took >60 s to re-parse an 800-byte generated input, which would hang seed parsing |
# | Whitespace between tokens rendered as zero or one space (at combinators, commas, parentheses, brackets, around attr-matchers) | 1 | CSS Syntax §4 tokenizes any whitespace run as one <whitespace-token> |
# | Identifiers (class, id, data-* suffix, lang subtags) from <name> over {a,b,c,d}, length free | 3 | shared alphabet so selectors hit documents |
# | Type selectors from {html,body,div,section,p,span,em,b,a,input}  | 3 | the document half's element set |
# | Attribute names from {class,id,title,lang,href,type,checked,disabled,required,readonly,data-<name>} | 3 | the document half's attribute set |
# | String and ident values from <attr_value_words> ({a-d} words joined by '-' or ' ') | 3 | shared with document attribute values |
# | No escapes, no case variants (ODD, DIV, N), no comments           | 3 | lexical vocabulary |
# | :lang() takes one <ident>; string form, comma list and '*-' wildcard omitted | 4 | nwsapi x3 throw on 100% of each (Chromium 151 rejects them too) |
# | Language tags restricted to subtags of 2+ letters                 | 2 | BCP 47 / RFC 5646 §2.1 well-formed tags (a 1-letter range such as `:lang(c)` is also thrown on by nwsapi x3, 100%) |
# | <attr-modifier> 's' omitted ('i' kept)                           | 4 | nwsapi 2.2.25/2.2.26/2.2.27 throw on 100% |
# | <ns-prefix> omitted (`*|E`, `|E`, `ns|E`, `[*|a]`)               | 4 | `*|E`,`|E`: nwsapi x3 and css-select throw on 100%; `[*|a]`: css-select 100% |
# | Column combinator `||`                                           | 4 | all five engines throw on 100% |
# | <pseudo-compound-selector> / pseudo-elements omitted              | 4 | css-select throws on 100% of ::before/::after/::first-line/:before, nwsapi x3 on 100% of ::marker/::slotted/::part |
# | `of S` in :nth-child()/:nth-last-child() omitted                  | 4 | nwsapi x3 throw on 100% |
# | :focus :focus-within :focus-visible :fullscreen :modal :target :target-within :placeholder-shown :default :indeterminate :valid :invalid :in-range :out-of-range :open :popover-open :defined :playing :paused :autofill :user-valid :user-invalid :local-link :current :past :future :blank :picture-in-picture :host :dir() omitted | 4 | css-select throws "Unknown pseudo-class" on 100% of each; :fullscreen also nwsapi 2.2.25 100%; :target-within :user-valid :user-invalid :local-link :current :past :future :blank :host also nwsapi x3 100% |
# | Document: tags {div,section,p,span,em,b,a,input}, one slot per attribute in fixed order, text over {a,b,c,space} | 3 | finite vocabulary; HTML forbids duplicate attributes, and order has no DOM effect |
# | Document: content-model-respecting subset of HTML syntax          | 2 | WHATWG HTML §13.1 "Writing HTML documents" restricted to trees the §13.2 tree builder builds without error recovery |
#
# Kept although some engines disagree (partial, <95%): :has() with `~`/`+`
# (nwsapi 2.2.25/2.2.26 throw on ~5%); a pseudo-class followed by `+` and an
# attribute selector, or by an unspaced `>`/`~` (nwsapi x3 throw; ~30% of
# generated inputs); a functional pseudo-class in a non-last member of a
# :is/:not/:has list (nwsapi x3 throw); :scope (css-select matches nothing
# where the others match <html>), :read-only, :read-write, :active,
# An+B edge forms. The harness drops disagreeing inputs per engine pair at
# scoring time; partial disagreement is where engine bugs show up.

# Selectors-4 §18: the input is a <selector-list> and a document.
<start> ::= <selector_list> "\n@@@\n" <doc>

# ---------------------------------------------------------------- selectors

# Selectors-4 §18 <selector-list> = <complex-selector-list>
<selector_list> ::= <complex_selector_list>
# Selectors-4 §18 <complex-selector-list> = <complex-selector>#
<complex_selector_list> ::= <complex_selector> | <complex_selector> <more_complex_selector>
# Selectors-4 §18 the `#` multiplier: comma-separated repetition (CSS Values §2.1)
<more_complex_selector> ::= <comma> <complex_selector_list>
# Selectors-4 §18 <complex-selector> = <complex-selector-unit> [ <combinator>? <complex-selector-unit> ]*
# (descendant combinator is the whitespace alternative of <combinator> here)
<complex_selector> ::= <compound> | <compound> <combinator> <complex_selector>
# Selectors-4 §18 <combinator> = '>' | '+' | '~' | [ '|' '|' ], plus the descendant combinator (§16.1, whitespace); '||' is class 4
<combinator> ::= " " | ">" | " >" | "> " | " > " | "+" | " +" | "+ " | " + " | "~" | " ~" | "~ " | " ~ "
# Selectors-4 §18 <compound-selector> = [ <type-selector>? <subclass-selector>* ]!
# A type or universal selector may only lead a compound; `!` means non-empty.
# (Named <compound>, as before, so derived count_compound keeps its meaning.)
<compound> ::= <type_selector> | <type_selector> <subclass_selectors> | <subclass_selectors>
# Selectors-4 §18 <subclass-selector>* (one or more), as right recursion (class 1)
<subclass_selectors> ::= <subclass_selector> | <subclass_selector> <subclass_selectors>
# Selectors-4 §18 <simple-selector> = <type-selector> | <subclass-selector> (not referenced by any production kept here)
# Selectors-4 §18 <type-selector> = <wq-name> | <ns-prefix>? '*' ; <ns-prefix> is class 4
<type_selector> ::= <wq_name> | "*"
# Selectors-4 §18 <wq-name> = <ns-prefix>? <ident-token> ; <ns-prefix> is class 4
<wq_name> ::= <tag>
# Selectors-4 §18 <subclass-selector> = <id-selector> | <class-selector> | <attribute-selector> | <pseudo-class-selector>
<subclass_selector> ::= <id_selector> | <class_selector> | <attribute_selector> | <pseudo_class_selector>
# Selectors-4 §18 <id-selector> = <hash-token>
<id_selector> ::= "#" <name>
# Selectors-4 §18 <class-selector> = '.' <ident-token>
<class_selector> ::= "." <name>
# Selectors-4 §18 <attribute-selector> = '[' <wq-name> ']' | '[' <wq-name> <attr-matcher> [ <string-token> | <ident-token> ] <attr-modifier>? ']'
<attribute_selector> ::= <lbracket> <attr_name> <rbracket> | <lbracket> <attr_name> <attr_matcher_ws> <attr_value> <rbracket> | <lbracket> <attr_name> <attr_matcher_ws> <attr_value> <attr_modifier> <rbracket>
# CSS Syntax-3 §4 '[' with optional whitespace after it
<lbracket> ::= "[" | "[ "
# CSS Syntax-3 §4 ']' with optional whitespace before it
<rbracket> ::= "]" | " ]"
# Selectors-4 §18 <attr-matcher> with optional whitespace on either side
<attr_matcher_ws> ::= <attr_matcher> | " " <attr_matcher> | <attr_matcher> " " | " " <attr_matcher> " "
# Selectors-4 §18 <attr-matcher> = [ '~' | '|' | '^' | '$' | '*' ]? '='
<attr_matcher> ::= "=" | "~=" | "|=" | "^=" | "$=" | "*="
# Selectors-4 §18 [ <string-token> | <ident-token> ]
<attr_value> ::= "\"\"" | "\"" <attr_value_words> "\"" | <attr_ident>
# CSS Syntax-3 §4.3.4 <ident-token> as an attribute value (a hyphenated word over the shared alphabet)
<attr_ident> ::= <name> | <name> "-" <attr_ident>
# Selectors-4 §18 <attr-modifier> = i | s ; 's' is class 4. Whitespace before it is optional after a string, required after an ident.
<attr_modifier> ::= " i"
# Selectors-4 §18 <pseudo-class-selector> = ':' <ident-token> | ':' <function-token> <any-value> ')'
<pseudo_class_selector> ::= ":" <pseudo_class_ident> | ":" <pseudo_class_function>
# Selectors-4 §14 tree-structural (§14.1-14.4), §9 user action (hover, active), §13 input (enabled .. optional), §8.1-8.3 location (link, visited, any-link), §4.5 :scope
<pseudo_class_ident> ::= "root" | "empty" | "first-child" | "last-child" | "only-child" | "first-of-type" | "last-of-type" | "only-of-type" | "hover" | "active" | "enabled" | "disabled" | "checked" | "read-only" | "read-write" | "required" | "optional" | "link" | "visited" | "any-link" | "scope"
# Selectors-4 §4.2 :is(), §4.3 :not(), §4.4 :where(), §4.5 :has(), §14.4 child-indexed, §14.5 typed child-indexed, §7.2 :lang()
<pseudo_class_function> ::= "is" <lparen> <complex_selector_list> <rparen> | "where" <lparen> <complex_selector_list> <rparen> | "not" <lparen> <complex_selector_list> <rparen> | "has" <lparen> <relative_selector_list> <rparen> | <nth_function> | "lang" <lparen> <lang_range> <rparen>
# Selectors-4 §14.4.1-14.4.2, §14.5.1-14.5.2 :nth-child(<An+B>) etc.; `[of S]` is class 4
<nth_function> ::= "nth-child" <lparen> <an_plus_b> <rparen> | "nth-last-child" <lparen> <an_plus_b> <rparen> | "nth-of-type" <lparen> <an_plus_b> <rparen> | "nth-last-of-type" <lparen> <an_plus_b> <rparen>
# Selectors-4 §7.2 :lang() = :lang( [ <ident> | <string> ]# ). Only the single
# <ident> form is kept: the string form, the comma list and the '*-' wildcard
# are class 4 (nwsapi 2.2.25/2.2.26/2.2.27 throw on 100% of each).
<lang_range> ::= <lang_tag>

# Selectors-4 §18 <relative-selector-list> = <relative-selector>#
<relative_selector_list> ::= <relative_selector> | <relative_selector> <more_relative_selector>
# Selectors-4 §18 the `#` multiplier of <relative-selector-list>
<more_relative_selector> ::= <comma> <relative_selector_list>
# Selectors-4 §18 <relative-selector> = <combinator>? <complex-selector>
<relative_selector> ::= <complex_selector_in_has> | <relative_combinator> <complex_selector_in_has>
# Selectors-4 §18 <combinator> as a leading token of a relative selector (the absent case is the descendant combinator)
<relative_combinator> ::= ">" | "> " | "+" | "+ " | "~" | "~ "

# Selectors-4 §4.5: ":has() cannot be nested; :has() is not valid within
# :has()". The rules below repeat <complex-selector> .. <pseudo-class-selector>
# with the :has alternative removed, which is how a CFG states that rule.
# Selectors-4 §18 <complex-selector-list>, inside :has()
<complex_selector_list_in_has> ::= <complex_selector_in_has> | <complex_selector_in_has> <more_complex_selector_in_has>
# Selectors-4 §18 the `#` multiplier, inside :has()
<more_complex_selector_in_has> ::= <comma> <complex_selector_list_in_has>
# Selectors-4 §18 <complex-selector>, inside :has()
<complex_selector_in_has> ::= <compound_in_has> | <compound_in_has> <combinator> <complex_selector_in_has>
# Selectors-4 §18 <compound-selector>, inside :has()
<compound_in_has> ::= <type_selector> | <type_selector> <subclass_selectors_in_has> | <subclass_selectors_in_has>
# Selectors-4 §18 <subclass-selector>* inside :has(), as right recursion (class 1)
<subclass_selectors_in_has> ::= <subclass_selector_in_has> | <subclass_selector_in_has> <subclass_selectors_in_has>
# Selectors-4 §18 <subclass-selector>, inside :has()
<subclass_selector_in_has> ::= <id_selector> | <class_selector> | <attribute_selector> | <pseudo_class_selector_in_has>
# Selectors-4 §18 <pseudo-class-selector>, inside :has()
<pseudo_class_selector_in_has> ::= ":" <pseudo_class_ident> | ":" <pseudo_class_function_in_has>
# Selectors-4 §4.2-4.4, §14.4-14.5, §7.2, inside :has() (no :has alternative)
<pseudo_class_function_in_has> ::= "is" <lparen> <complex_selector_list_in_has> <rparen> | "where" <lparen> <complex_selector_list_in_has> <rparen> | "not" <lparen> <complex_selector_list_in_has> <rparen> | <nth_function> | "lang" <lparen> <lang_range> <rparen>

# CSS Syntax-3 §6.1 <an+b>: 'odd' | 'even' | <integer> | A n [ ['+'|'-'] B ]?
# covering <n-dimension>, '+'?n, -n, <ndashdigit-dimension>, <dashndashdigit-ident>
# and the whitespace-separated sign forms.
<an_plus_b> ::= "odd" | "even" | <signed_integer> | <an_a> | <an_a> <an_b_sign> <digits>
# CSS Syntax-3 §6.1 the A part: [+|-]? digits? 'n' (no whitespace between sign and 'n')
<an_a> ::= "n" | <sign> "n" | <digits> "n" | <sign> <digits> "n"
# CSS Syntax-3 §4.3.12 <integer> with optional sign
<signed_integer> ::= <digits> | <sign> <digits>
# CSS Syntax-3 §6.1 sign
<sign> ::= "+" | "-"
# CSS Syntax-3 §6.1 the sign before B, with optional whitespace on either side
<an_b_sign> ::= "+" | "-" | " +" | " -" | "+ " | "- " | " + " | " - "
# CSS Syntax-3 §4.3.12 digits
<digits> ::= <digit> | <digit> <digits>
# CSS Syntax-3 §4.2 digit
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
# CSS Syntax-3 §4 optional whitespace (a run is one token; class 1) around a comma.
# Optional whitespace is spelled out as alternatives, never as a nullable
# rule: Fandango's parser failed to parse its own output (`:is(a,b)`) when a
# nullable <ows> sat inside a function's parentheses.
<comma> ::= "," | " ," | ", " | " , "
# CSS Syntax-3 §4.3 function-token '(' with optional whitespace after it
<lparen> ::= "(" | "( "
# CSS Syntax-3 §4.3 ')' with optional whitespace before it
<rparen> ::= ")" | " )"

# ----------------------------------------------------------------- document

# HTML §13.1 document: DOCTYPE (§13.1.1; without it the document is in quirks mode), html and body tags written out, head omitted (§13.1.2.4 optional tags)
<doc> ::= "<!DOCTYPE html><html><body>" <node> <more_node>* "</body></html>"
# HTML §3.2.5.2.2 flow content: further top-level children of <body>
<more_node> ::= <node>
# HTML §3.2.5.2.2 flow content. One production per element, so start and end tags always match.
<node> ::= <div> | <section> | <p> | <phrasing_element>
# HTML §4.4.15 div: flow content. <attrs> ends with the start tag's '>'.
<div> ::= "<div" <attrs> "</div>" | "<div" <attrs> <flow_content> "</div>"
# HTML §4.3.3 section: flow content
<section> ::= "<section" <attrs> "</section>" | "<section" <attrs> <flow_content> "</section>"
# HTML §4.4.1 p: phrasing content only (a block start tag would close it implicitly)
<p> ::= "<p" <attrs> "</p>" | "<p" <attrs> <phrasing_content> "</p>"
# HTML §3.2.5.2.2 flow content, as text runs between elements. Every text run
# is maximal (a run is never followed by another run), so each document has
# exactly one parse. Written as `<child>*` over a nullable text leaf, as
# before, a run of text could be cut into leaves in exponentially many ways,
# and Fandango took over 60 s to re-parse an 800-byte input it had generated
# itself (class 1: same language).
<flow_content> ::= <text_run> | <text_run> <flow_item>+ | <flow_item>+
# HTML §3.2.5.2.2 one flow child, with the text run that follows it
<flow_item> ::= <flow_element> | <flow_element> <text_run>
# HTML §3.2.5.2.2 flow elements. The leaves (<input>, <a>, and any element
# with empty content) are what make depth decay: without them every child
# recursed and a large node budget built trees thousands of levels deep, which
# Fandango's tree walk could not survive even at recursionlimit 60000.
<flow_element> ::= <node> | <input> | <a>
# HTML §3.2.5.2.5 phrasing content, as text runs between elements
<phrasing_content> ::= <text_run> | <text_run> <phrasing_item>+ | <phrasing_item>+
# HTML §3.2.5.2.5 one phrasing child, with the text run that follows it
<phrasing_item> ::= <phrasing_leaf> | <phrasing_leaf> <text_run>
# HTML §3.2.5.2.5 phrasing elements
<phrasing_leaf> ::= <phrasing_element> | <input> | <a>
# HTML §4.5 text-level elements with phrasing content
<phrasing_element> ::= <span> | <em> | <b>
# HTML §4.5.26 span
<span> ::= "<span" <attrs> "</span>" | "<span" <attrs> <phrasing_content> "</span>"
# HTML §4.5.2 em
<em> ::= "<em" <attrs> "</em>" | "<em" <attrs> <phrasing_content> "</em>"
# HTML §4.5.21 b
<b> ::= "<b" <attrs> "</b>" | "<b" <attrs> <phrasing_content> "</b>"
# HTML §4.5.1 a: transparent, but must not contain another <a>; text only here. href is what :link and :any-link match.
<a> ::= "<a" <attrs> "</a>" | "<a" <attrs> <text_run> "</a>" | "<a" <href_attr> <attrs> "</a>" | "<a" <href_attr> <attrs> <text_run> "</a>"
# HTML §4.10.5 input: void element, no end tag (§13.1.2.1)
<input> ::= "<input" <input_attrs>

# HTML §13.1.2.3 attributes: each at most once (duplicates are a parse error),
# in a fixed order (class 3). Each slot is optional; the chain ends with the
# start tag's '>' so that no rule is nullable (see <comma>).
<attrs> ::= <attrs_id> | <class_attr> <attrs_id>
# HTML §13.1.2.3 attribute chain after the class slot
<attrs_id> ::= <attrs_title> | <id_attr> <attrs_title>
# HTML §13.1.2.3 attribute chain after the id slot
<attrs_title> ::= <attrs_lang> | <title_attr> <attrs_lang>
# HTML §13.1.2.3 attribute chain after the title slot
<attrs_lang> ::= <attrs_data> | <lang_attr> <attrs_data>
# HTML §13.1.2.3 attribute chain after the lang slot, closing the start tag
<attrs_data> ::= ">" | <data_attr> ">"
# HTML §3.2.6 class: set of space-separated tokens
<class_attr> ::= " class=\"" <class_list> "\""
# HTML §2.3.7 space-separated tokens
<class_list> ::= <name> | <name> " " <class_list>
# HTML §3.2.6 id
<id_attr> ::= " id=\"" <name> "\""
# HTML §3.2.6.1 title
<title_attr> ::= " title=\"\"" | " title=\"" <attr_value_words> "\""
# HTML §3.2.6.2 lang: a BCP 47 tag
<lang_attr> ::= " lang=\"" <lang_tag> "\""
# HTML §3.2.6.6 data-* custom attribute
<data_attr> ::= " data-" <name> "=\"\"" | " data-" <name> "=\"" <attr_value_words> "\""
# HTML §4.6.1 href
<href_attr> ::= " href=\"#" <name> "\""
# HTML §4.10.5 input attributes, then the generic chain
<input_attrs> ::= <input_checked> | <type_attr> <input_checked>
# HTML §4.10.5 input type
<type_attr> ::= " type=\"checkbox\"" | " type=\"radio\"" | " type=\"text\""
# HTML §4.10.5.1 boolean attributes (evaluated by :checked, :disabled, :enabled, :required, :optional, :read-only, :read-write); checked
<input_checked> ::= <input_disabled> | " checked" <input_disabled>
# HTML §4.10.18.5 disabled
<input_disabled> ::= <input_required> | " disabled" <input_required>
# HTML §4.10.5.3.4 required
<input_required> ::= <input_readonly> | " required" <input_readonly>
# HTML §4.10.5.3.3 readonly
<input_readonly> ::= <attrs> | " readonly" <attrs>
# HTML §13.1.3 text: a non-empty run with no '<', '&' or '@' (class 3 alphabet)
<text_run> ::= <tchar>+
# class 3 text alphabet
<tchar> ::= "a" | "b" | "c" | " "

# ------------------------------------------------------- shared vocabulary

# class 3: the element names both halves use
<tag> ::= "div" | "section" | "p" | "span" | "em" | "b" | "a" | "input" | "body" | "html"
# class 3: attribute names both halves use
<attr_name> ::= "class" | "id" | "title" | "lang" | "href" | "type" | "checked" | "disabled" | "required" | "readonly" | "data-" <name>
# class 3: attribute value text, words joined by '-' or ' ' so that ~=, |=,
# ^=, $= and *= all have something to match; the empty value is spelled out
# at each use ("") rather than as a nullable rule. Right recursion (class 1).
<attr_value_words> ::= <name> | <name> <more_value_word>
# class 3: a further word of an attribute value
<more_value_word> ::= "-" <attr_value_words> | " " <attr_value_words>
# BCP 47 (RFC 5646 §2.1) language tag: subtags of two or more letters (class 2),
# over the shared alphabet (class 3)
<lang_tag> ::= <lang_subtag> | <lang_subtag> "-" <lang_tag>
# RFC 5646 §2.1 subtag, two or more letters
<lang_subtag> ::= <namechar> <namechar>+
# class 3: identifiers over a small alphabet, length free
<name> ::= <namechar> | <namechar> <namechar> | <namechar> <namechar> <namechar>+
# class 3
<namechar> ::= "a" | "b" | "c" | "d"

where count_attr_matcher_ws(<start>) >= 14.0
where count_attr_matcher_ws(<start>) <= 26
