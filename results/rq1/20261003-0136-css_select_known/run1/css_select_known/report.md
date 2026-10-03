# css_select_known

- corpus: 536 rows, 268 inputs, 2 systems
- elapsed: 1922s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 20 | 15 |
| count_complex_selector | 1 | 39 | 28 |
| count_combinator | 0 | 59 | 30 |
| count_subclass_selectors | 0 | 69 | 42 |
| count_type_selector | 0 | 73 | 35 |
| count_wq_name | 0 | 32 | 19 |
| count_pseudo_class_selector | 0 | 29 | 22 |
| count_id_selector | 0 | 45 | 25 |
| count_class_selector | 0 | 22 | 21 |
| count_attribute_selector | 0 | 66 | 25 |
| count_pseudo_class_ident | 0 | 55 | 20 |
| count_pseudo_class_function | 0 | 12 | 12 |
| count_name | 2 | 221 | 115 |
| count_attr_matcher_ws | 0 | 22 | 20 |
| count_attr_modifier | 0 | 10 | 11 |
| count_attr_value | 0 | 22 | 20 |
| count_lparen | 0 | 49 | 18 |
| count_relative_selector_list | 0 | 29 | 15 |
| count_nth_function | 0 | 9 | 8 |
| count_rparen | 0 | 49 | 18 |
| count_more_complex_selector | 0 | 12 | 11 |
| count_lang_range | 0 | 21 | 11 |
| count_namechar | 11 | 12365 | 209 |
| count_attr_value_words | 0 | 69 | 59 |
| count_attr_ident | 0 | 10 | 10 |
| count_more_relative_selector | 0 | 19 | 13 |
| count_comma | 0 | 26 | 18 |
| count_lang_tag | 0 | 67 | 54 |
| count_more_value_word | 0 | 41 | 37 |
| count_relative_combinator | 0 | 11 | 10 |
| count_complex_selector_in_has | 0 | 83 | 23 |
| count_digits | 0 | 6 | 6 |
| count_an_a | 0 | 9 | 8 |
| count_signed_integer | 0 | 1 | 2 |
| count_an_b_sign | 0 | 1 | 2 |
| count_sign | 0 | 1 | 2 |
| count_subclass_selectors_in_has | 0 | 171 | 25 |
| count_pseudo_class_selector_in_has | 0 | 75 | 14 |
| count_pseudo_class_function_in_has | 0 | 37 | 12 |
| count_complex_selector_list_in_has | 0 | 9 | 9 |
| count_more_complex_selector_in_has | 0 | 5 | 3 |
| count_node | 1 | 27 | 24 |
| count_phrasing_element | 0 | 51 | 23 |
| count_em | 0 | 18 | 13 |
| count_phrasing_content | 0 | 16 | 15 |
| count_text_run | 0 | 86 | 54 |
| count_tchar | 0 | 4536 | 113 |
| count_phrasing_item | 0 | 104 | 36 |
| count_input | 0 | 36 | 27 |
| count_type_attr | 0 | 14 | 14 |
| count_b | 0 | 16 | 11 |
| count_span | 0 | 22 | 15 |
| count_a | 0 | 97 | 34 |
| count_attrs | 1 | 144 | 58 |
| count_href_attr | 0 | 14 | 15 |
| count_title_attr | 0 | 60 | 41 |
| count_id_attr | 0 | 55 | 36 |
| count_class_attr | 0 | 33 | 34 |
| count_class_list | 0 | 66 | 56 |
| count_lang_attr | 0 | 32 | 32 |
| count_data_attr | 0 | 33 | 34 |
| count_p | 0 | 11 | 10 |
| count_section | 0 | 8 | 8 |
| count_flow_content | 0 | 26 | 20 |
| count_flow_item | 0 | 143 | 41 |
| count_div | 0 | 27 | 23 |
| count_more_node | 0 | 16 | 14 |
| doc_depth | 3 | 18 | 14 |
| doc_bytes | 67 | 16134 | 209 |
| selector_len | 1 | 2577 | 146 |
| selector_nesting | 0 | 6 | 7 |

## frontier
[css_select_known] grammar frontier (targeting stopped asking here):
  count_attr_ident: pinned at 10 by the SEARCH; 2 escalating request(s) returned nothing further.
  count_more_complex_selector_in_has: pinned at 5 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 212 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_relative_selector_list bins move with count_combinator (1..24 across bins) -- those regions are joint, not count_relative_selector_list findings
[compare] count_complex_selector_list_in_has bins move with count_combinator (3..17 across bins) -- those regions are joint, not count_complex_selector_list_in_has findings
[compare] count_more_complex_selector_in_has bins move with count_combinator (5..17 across bins) -- those regions are joint, not count_more_complex_selector_in_has findings
  css_select_5_1_0 better than css_select_5_2_0 on runtime_ns: 1.13x (95% CI 1.12-1.14, n=176, p=7.03e-27)
      undecided on count_combinator in [1,1.973), [1.973,3.893), [7.681,15.16) -- needs more inputs
[compare] rss: 212 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_relative_selector_list bins move with count_combinator (1..24 across bins) -- those regions are joint, not count_relative_selector_list findings
[compare] count_complex_selector_list_in_has bins move with count_combinator (3..17 across bins) -- those regions are joint, not count_complex_selector_list_in_has findings
[compare] count_more_complex_selector_in_has bins move with count_combinator (5..17 across bins) -- those regions are joint, not count_more_complex_selector_in_has findings
  css_select_5_1_0 and css_select_5_2_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=176)
[compare] dominance across runtime_ns, rss:
  css_select_5_1_0 DOMINATES css_select_5_2_0: better on runtime_ns 1.13x; equivalent on rss
      count_combinator =0 (n=47): css_select_5_1_0 not dominated
      count_combinator [1,1.973) (n=35): css_select_5_1_0, css_select_5_2_0 not dominated
      count_combinator [1.973,3.893) (n=22): css_select_5_1_0, css_select_5_2_0 not dominated
      count_combinator [3.893,7.681) (n=30): css_select_5_1_0 not dominated
      count_combinator [7.681,15.16) (n=23): css_select_5_1_0, css_select_5_2_0 not dominated
      count_combinator [15.16,29.9) (n=97): css_select_5_1_0 not dominated
      count_combinator [29.9,59] (n=14): css_select_5_1_0, css_select_5_2_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in [1,1.973), [1.973,3.893), [7.681,15.16), [29.9,59] on count_combinator -- the global verdict is a statement about this corpus's mix, not about the systems
      count_relative_selector_list =0 (n=135): css_select_5_1_0 not dominated
      count_relative_selector_list [1,1.753) (n=49): css_select_5_1_0, css_select_5_2_0 not dominated
      count_relative_selector_list [1.753,3.072) (n=9): css_select_5_1_0, css_select_5_2_0 not dominated
      count_relative_selector_list [3.072,5.385) (n=39): css_select_5_1_0 not dominated
      count_relative_selector_list [5.385,9.439) (n=14): css_select_5_1_0, css_select_5_2_0 not dominated
      count_relative_selector_list [9.439,16.54) (n=9): css_select_5_1_0, css_select_5_2_0 not dominated
      count_relative_selector_list [16.54,29] (n=13): css_select_5_1_0, css_select_5_2_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in [1,1.753), [1.753,3.072), [5.385,9.439), [9.439,16.54), [16.54,29] on count_relative_selector_list -- the global verdict is a statement about this corpus's mix, not about the systems
      count_complex_selector_list_in_has =0 (n=190): css_select_5_1_0 not dominated
      count_complex_selector_list_in_has [1,2.333) (n=57): css_select_5_1_0 not dominated
      count_complex_selector_list_in_has [7.667,9] (n=12): css_select_5_1_0, css_select_5_2_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in [7.667,9] on count_complex_selector_list_in_has -- the global verdict is a statement about this corpus's mix, not about the systems
      count_more_complex_selector_in_has =0 (n=221): css_select_5_1_0 not dominated
      count_more_complex_selector_in_has [1,1.667) (n=45): css_select_5_1_0 not dominated
