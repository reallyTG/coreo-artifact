# TAILORED grammar (RQ1, tailored setting) for @asamuzakjp/dom-selector
# 8.2.4 .. 9.2.2. A SUB-LANGUAGE of subjects/selectors_js/selectors_js.fan:
# every string this grammar derives is derivable there. The only operations
# used are removing alternatives, restricting vocabularies (to subsets of the
# spec grammar's own vocabularies), and fixing repetition bounds inside what
# the spec's `*`/`+` allow. Rule names follow the spec grammar's where the
# rule is the same rule restricted; new names are only for restricted copies
# of a spec rule (noted per rule). Input format unchanged: selector, the
# marker line "\n@@@\n", then the HTML document.
#
# WHY THIS SHAPE (derived from the diffs of the mined pairs, as a developer
# investigating each commit would write it):
#
# - 9.0.3 -> 9.0.4, 0e70971 (attribute-presence fast path): querySelectorAll
#   tests the WHOLE selector string against /^\[([a-z][a-z0-9_-]*)\]$/ and,
#   when it matches and the name is not `lang`, walks the tree with a
#   TreeWalker instead of running the matcher. Only a bare, unspaced `[name]`
#   as the entire selector list takes it. Hence <bare_attribute>: one
#   top-level alternative that is exactly "[" <attr_name> "]". `[lang]` stays
#   in the vocabulary because the fast path excludes it (a control the diff
#   names), and spaced brackets stay inside compounds, where they miss the
#   fast path.
# - 9.1.1 -> 9.1.2, f9fbf0f (faster attribute equality): matcher.js gains a
#   shortcut for `[name="value"]` with matcher '=', no `i` flag, a STRING
#   value (quoted, not an ident), a name matching /^[a-z][a-z\d_-]*$/ that is
#   not `lang` and not in the case-insensitive set (type, checked, ...); and
#   finder.js routes a compound-less attribute leaf to the walker. The spec
#   grammar's compounds lead with a type, id or class far more often than with
#   an attribute, so attribute matching was never the hot test. Here every
#   compound's FIRST subclass selector is an attribute selector or a
#   child-indexed pseudo-class (<lead_subclass>), the matcher is '=' only, the
#   value is quoted or an ident, and the `i` modifier is kept as the control
#   that turns the shortcut off.
# - 8.2.4 -> 8.2.5, 648283e (perf regression #286, nthIndexCache): the
#   evaluator caches, per parent and per An+B AST, the index of every child,
#   so :nth-child/:nth-last-child/:nth-of-type/:nth-last-of-type over a
#   parent with n children costs O(n) once instead of O(n) per child. The
#   cache lives on the DOMSelector instance, so the effect shows with cold
#   caches (the subject's second metric, fresh_ns) and grows with sibling
#   count. Hence the child-indexed pseudo-classes in <lead_subclass> and the
#   document shape below.
# - 9.2.1 -> 9.2.2, c8ccd4b (skip cache checks for uncached single
#   selectors): a compound of exactly one attribute or id selector (or
#   :link/:any-link/:scope) bypasses the result cache. Single-attribute
#   compounds are already the commonest compound here; id selectors stay in
#   the trailing set.
# - 9.0.4 -> 9.1.0 (disabled-state cache, unescaped-name cache): :disabled
#   and :enabled stay in the trailing pseudo-class set and <input> with
#   `disabled` stays in the document. Measured effect by hand was below 3%;
#   a null is a valid outcome.
#
# DOCUMENT SHAPE. The body holds a WIDE sibling list: <node> then
# <more_node>{19,49}, so 20 to 2000 children under one parent (the
# subject's example.py bands this in five narrow log-spaced bands, 20-50,
# 50-150, 150-400, 400-1000, 1000-2000 children, for
# exploration). Each sibling is a shallow element (one level of phrasing
# content at most) so the node budget goes into width, not depth. The title
# attribute is always present (the spec's optional slot with the absent
# alternative removed), and attribute values, ids, classes and data-* names
# come from <short_name> (one or two letters over {a,b,c,d}, a subset of the
# spec's <name>), so equality selectors hit a useful fraction of elements.
#
# GRAMMAR DIFF against selectors_js.fan (everything else is identical):
# | Rule                     | Change                                                        |
# |--------------------------|---------------------------------------------------------------|
# | <selector_list>          | adds <bare_attribute> ("[" <attr_name> "]", unspaced), itself a one-member <complex_selector_list> |
# | <compound>               | bare <type_selector> alternative removed; <subclass_selectors> must lead with <lead_subclass> |
# | <subclass_selectors>     | first item <lead_subclass> (attribute or nth pseudo), rest <trailing_subclass> |
# | <trailing_subclass>      | restricted <subclass_selector>: id, class, attribute, nth pseudo, :disabled/:enabled/:checked/:first-child/:last-child |
# | <attr_matcher>           | '=' only                                                      |
# | <attribute_selector>     | '=' forms take <eq_attr_name> (title, class, id, lang, type, data-*) |
# | <attr_value>             | quoted <short_name> or ident <short_name> (empty string and multi-word values removed) |
# | <pseudo_class_function>  | only <nth_function>; :is/:where/:not/:has/:lang removed        |
# | :has-only rules          | removed (unreachable without :has)                            |
# | <type_selector>          | <wq_name> only ('*' removed)                                  |
# | <doc>                    | <more_node>{19,49} bounded to {19,1999}                              |
# | <node> / elements        | shallow: div/section/p/span/em/b with phrasing content of leaves only |
# | <attrs_title>            | title always present; values <short_name>                      |
# | <class_list>/<id_attr>/<data_attr> | <short_name> values; class list of one or two names  |
# | <text_run>               | <tchar>{1,3}                                                  |
# | <a>                      | href form only                                                |

<start> ::= <selector_list> "\n@@@\n" <doc>

# ---------------------------------------------------------------- selectors

# Selectors-4 §18 <selector-list>; the first alternative is the one-member list
# `[name]` written without whitespace (9.0.4's fast-path shape)
<selector_list> ::= <bare_attribute> | <complex_selector> | <complex_selector> <more_complex_selector>
# restricted <attribute_selector>: '[' <wq-name> ']' with no whitespace
<bare_attribute> ::= "[" <attr_name> "]"
<complex_selector_list> ::= <complex_selector> | <complex_selector> <more_complex_selector>
<more_complex_selector> ::= <comma> <complex_selector_list>
<complex_selector> ::= <compound> | <compound> <combinator> <complex_selector>
<combinator> ::= " " | ">" | " >" | "> " | " > " | "+" | " +" | "+ " | " + " | "~" | " ~" | "~ " | " ~ "
# Selectors-4 §18 <compound-selector>, restricted: a subclass selector always
# present and led by an attribute selector or a child-indexed pseudo-class
<compound> ::= <type_selector> <subclass_selectors> | <subclass_selectors>
<subclass_selectors> ::= <lead_subclass> | <lead_subclass> <trailing_subclasses>
<trailing_subclasses> ::= <trailing_subclass> | <trailing_subclass> <trailing_subclasses>
# restricted <subclass-selector>: the leading one
<lead_subclass> ::= <attribute_selector> | ":" <nth_function>
# restricted <subclass-selector>: the ones after it
<trailing_subclass> ::= <id_selector> | <class_selector> | <attribute_selector> | ":" <nth_function> | ":" <pseudo_class_ident>
<type_selector> ::= <wq_name>
<wq_name> ::= <tag>
<id_selector> ::= "#" <short_name>
<class_selector> ::= "." <short_name>
<attribute_selector> ::= <lbracket> <attr_name> <rbracket> | <lbracket> <eq_attr_name> <attr_matcher_ws> <attr_value> <rbracket> | <lbracket> <eq_attr_name> <attr_matcher_ws> <attr_value> <attr_modifier> <rbracket>
<lbracket> ::= "[" | "[ "
<rbracket> ::= "]" | " ]"
<attr_matcher_ws> ::= <attr_matcher> | " " <attr_matcher> | <attr_matcher> " " | " " <attr_matcher> " "
# restricted: '=' only (the matcher f9fbf0f's shortcut covers)
<attr_matcher> ::= "="
# restricted: a quoted string (the shortcut's case) or an ident (its control)
<attr_value> ::= "\"" <short_name> "\"" | <short_name>
<attr_modifier> ::= " i"
# restricted <pseudo_class_ident>: the states 9.1.0 caches, and two
# tree-structural ones
<pseudo_class_ident> ::= "disabled" | "enabled" | "checked" | "first-child" | "last-child"
<nth_function> ::= "nth-child" <lparen> <an_plus_b> <rparen> | "nth-last-child" <lparen> <an_plus_b> <rparen> | "nth-of-type" <lparen> <an_plus_b> <rparen> | "nth-last-of-type" <lparen> <an_plus_b> <rparen>

<an_plus_b> ::= "odd" | "even" | <signed_integer> | <an_a> | <an_a> <an_b_sign> <digits>
<an_a> ::= "n" | <sign> "n" | <digits> "n" | <sign> <digits> "n"
<signed_integer> ::= <digits> | <sign> <digits>
<sign> ::= "+" | "-"
<an_b_sign> ::= "+" | "-" | " +" | " -" | "+ " | "- " | " + " | " - "
<digits> ::= <digit> | <digit> <digits>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<comma> ::= "," | " ," | ", " | " , "
<lparen> ::= "(" | "( "
<rparen> ::= ")" | " )"

# ----------------------------------------------------------------- document

# HTML §13.1 document; <more_node>{19,49} bounded to 19..1999 further children of <body>
<doc> ::= "<!DOCTYPE html><html><body>" <node> <more_node>{19,49} "</body></html>"
<more_node> ::= <node>
<node> ::= <div> | <section> | <p> | <phrasing_element>
# restricted: flow content of phrasing leaves only (no nested blocks), so the
# document is wide rather than deep
<div> ::= "<div" <attrs> "</div>" | "<div" <attrs> <phrasing_content> "</div>"
<section> ::= "<section" <attrs> "</section>" | "<section" <attrs> <phrasing_content> "</section>"
<p> ::= "<p" <attrs> "</p>" | "<p" <attrs> <phrasing_content> "</p>"
# restricted: at most one phrasing leaf, with text around it
<phrasing_content> ::= <text_run> | <text_run> <phrasing_item> | <phrasing_item>
<phrasing_item> ::= <phrasing_leaf> | <phrasing_leaf> <text_run>
<phrasing_leaf> ::= <leaf_span> | <input> | <a>
<phrasing_element> ::= <span> | <em> | <b>
<span> ::= "<span" <attrs> "</span>" | "<span" <attrs> <text_run> "</span>"
<em> ::= "<em" <attrs> "</em>" | "<em" <attrs> <text_run> "</em>"
<b> ::= "<b" <attrs> "</b>" | "<b" <attrs> <text_run> "</b>"
# restricted <span>: text content only (a leaf)
<leaf_span> ::= "<span" <attrs> "</span>" | "<span" <attrs> <text_run> "</span>"
<a> ::= "<a" <href_attr> <attrs> "</a>" | "<a" <href_attr> <attrs> <text_run> "</a>"
<input> ::= "<input" <input_attrs>

<attrs> ::= <attrs_id> | <class_attr> <attrs_id>
<attrs_id> ::= <attrs_title> | <id_attr> <attrs_title>
# restricted: the title slot is always filled
<attrs_title> ::= <title_attr> <attrs_lang>
<attrs_lang> ::= <attrs_data> | <lang_attr> <attrs_data>
<attrs_data> ::= ">" | <data_attr> ">"
<class_attr> ::= " class=\"" <class_list> "\""
<class_list> ::= <short_name> | <short_name> " " <short_name>
<id_attr> ::= " id=\"" <short_name> "\""
<title_attr> ::= " title=\"" <short_name> "\""
<lang_attr> ::= " lang=\"" <lang_tag> "\""
<data_attr> ::= " data-" <short_name> "=\"" <short_name> "\""
<href_attr> ::= " href=\"#" <short_name> "\""
<input_attrs> ::= <input_checked> | <type_attr> <input_checked>
<type_attr> ::= " type=\"checkbox\"" | " type=\"radio\"" | " type=\"text\""
<input_checked> ::= <input_disabled> | " checked" <input_disabled>
<input_disabled> ::= <input_required> | " disabled" <input_required>
<input_required> ::= <input_readonly> | " required" <input_readonly>
<input_readonly> ::= <attrs> | " readonly" <attrs>
<text_run> ::= <tchar>{1,3}
<tchar> ::= "a" | "b" | "c" | " "

# ------------------------------------------------------- shared vocabulary

<tag> ::= "div" | "section" | "p" | "span" | "em" | "b" | "a" | "input" | "body" | "html"
# restricted <attr_name> for '=' selectors: the valued attributes every
# document element can carry (title always, class/id/lang/data-* optionally),
# plus `type`, which f9fbf0f's shortcut excludes (case-insensitive set), as a
# control. The valueless booleans stay in <attr_name> for presence selectors.
<eq_attr_name> ::= "title" | "class" | "id" | "lang" | "type" | "data-" <short_name>
# restricted: data-* names from <short_name>
<attr_name> ::= "class" | "id" | "title" | "lang" | "href" | "type" | "checked" | "disabled" | "required" | "readonly" | "data-" <short_name>
<lang_tag> ::= <lang_subtag> | <lang_subtag> "-" <lang_subtag>
<lang_subtag> ::= <namechar> <namechar>
# restricted <name>: one or two letters, so values recur across elements
<short_name> ::= <namechar> | <namechar> <namechar>
<namechar> ::= "a" | "b" | "c" | "d"
