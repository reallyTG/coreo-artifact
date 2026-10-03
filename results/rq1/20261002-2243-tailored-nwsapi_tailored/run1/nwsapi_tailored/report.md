# nwsapi_tailored

- corpus: 1134 rows, 162 inputs, 7 systems
- elapsed: 3513s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 25 | 15 |
| count_complex_selector | 1 | 52 | 24 |
| count_type_selector | 0 | 46 | 25 |
| count_wq_name | 0 | 23 | 15 |
| count_subclass_selectors | 0 | 91 | 31 |
| count_attribute_selector | 0 | 19 | 15 |
| count_pseudo_class_selector | 0 | 28 | 14 |
| count_id_selector | 0 | 24 | 17 |
| count_class_selector | 0 | 26 | 17 |
| count_attr_matcher_ws | 0 | 14 | 12 |
| count_attr_modifier | 0 | 7 | 8 |
| count_attr_value | 0 | 14 | 12 |
| count_pseudo_class_ident | 0 | 11 | 10 |
| count_pseudo_class_function | 0 | 18 | 11 |
| count_sel_name | 0 | 71 | 31 |
| count_name | 52 | 592 | 104 |
| count_sel_value_words | 0 | 15 | 12 |
| count_attr_ident | 0 | 11 | 11 |
| count_nth_function | 0 | 5 | 5 |
| count_more_complex_selector | 0 | 14 | 11 |
| count_rparen | 0 | 20 | 13 |
| count_lparen | 0 | 20 | 13 |
| count_relative_selector_list | 0 | 10 | 10 |
| count_lang_range | 0 | 3 | 4 |
| count_sel_namechar | 0 | 436 | 64 |
| count_namechar | 629 | 12799 | 141 |
| count_more_sel_value_word | 0 | 11 | 10 |
| count_combinator | 0 | 33 | 19 |
| count_comma | 0 | 19 | 13 |
| count_more_relative_selector | 0 | 8 | 7 |
| count_lang_tag | 17 | 169 | 70 |
| count_escape | 0 | 200 | 48 |
| count_signed_integer | 0 | 1 | 2 |
| count_an_a | 0 | 3 | 3 |
| count_digits | 0 | 7 | 6 |
| count_an_b_sign | 0 | 1 | 2 |
| count_relative_combinator | 0 | 7 | 6 |
| count_complex_selector_in_has | 0 | 48 | 16 |
| count_hex_pad | 0 | 101 | 33 |
| count_sign | 0 | 2 | 3 |
| count_subclass_selectors_in_has | 0 | 66 | 17 |
| count_pseudo_class_selector_in_has | 0 | 13 | 9 |
| count_pseudo_class_function_in_has | 0 | 10 | 7 |
| count_complex_selector_list_in_has | 0 | 13 | 7 |
| count_more_complex_selector_in_has | 0 | 8 | 4 |
| count_node | 20 | 211 | 54 |
| count_p | 2 | 75 | 47 |
| count_phrasing_content | 1 | 46 | 36 |
| count_phrasing_item | 0 | 163 | 72 |
| count_text_run | 10 | 138 | 56 |
| count_tchar | 270 | 1836 | 119 |
| count_input | 1 | 51 | 35 |
| count_type_attr | 0 | 27 | 23 |
| count_attrs | 37 | 240 | 71 |
| count_id_attr | 16 | 92 | 41 |
| count_class_attr | 10 | 104 | 39 |
| count_class_list | 13 | 201 | 72 |
| count_a | 1 | 50 | 36 |
| count_href_attr | 0 | 25 | 23 |
| count_title_attr | 11 | 123 | 55 |
| count_attr_value_words | 11 | 184 | 78 |
| count_more_value_word | 3 | 92 | 58 |
| count_data_attr | 9 | 91 | 44 |
| count_lang_attr | 8 | 87 | 44 |
| count_phrasing_element | 3 | 74 | 51 |
| count_b | 1 | 27 | 22 |
| count_em | 0 | 25 | 25 |
| count_span | 1 | 24 | 23 |
| count_div | 0 | 72 | 49 |
| count_flow_content | 0 | 43 | 34 |
| count_flow_item | 0 | 71 | 48 |
| count_section | 2 | 69 | 45 |
| count_more_node | 19 | 200 | 14 |
| doc_depth | 4 | 20 | 14 |
| doc_bytes | 4175 | 15816 | 143 |
| selector_len | 1 | 2110 | 111 |
| selector_nesting | 0 | 9 | 8 |

## comparison
[compare] runtime_ns: 110 inputs, 7 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_type_selector bins move with count_sel_namechar (1.5..23 across bins) -- those regions are joint, not count_type_selector findings
[compare] count_class_selector bins move with count_type_selector (1.5..5 across bins); count_sel_namechar (2..37 across bins) -- those regions are joint, not count_class_selector findings
[compare] count_more_complex_selector bins move with count_type_selector (1..6 across bins); count_sel_namechar (2..24 across bins) -- those regions are joint, not count_more_complex_selector findings
[compare] count_sel_namechar bins move with count_type_selector (1..5 across bins) -- those regions are joint, not count_sel_namechar findings
  nwsapi_2_2_21 and nwsapi_2_2_22 equivalent: ratio 0.98x within the equivalence band (95% CI 0.96-1.00, n=110)
      undecided on count_type_selector (confounded) in [3.583,6.782) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962), [2.962,5.099) -- needs more inputs
      undecided on count_more_complex_selector (confounded) in [1,1.552), [1.552,2.41) -- needs more inputs
      undecided on count_sel_namechar (confounded) in [20.88,57.5) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_23 equivalent: ratio 0.99x within the equivalence band (95% CI 0.97-1.00, n=110)
      undecided on count_type_selector (confounded) in [3.583,6.782) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962), [2.962,5.099) -- needs more inputs
      undecided on count_more_complex_selector (confounded) in [1.552,2.41) -- needs more inputs
      undecided on count_sel_namechar (confounded) in [20.88,57.5) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_24 equivalent: ratio 0.98x within the equivalence band (95% CI 0.97-1.00, n=109)
      undecided on count_type_selector (confounded) in [3.583,6.782) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962), [2.962,5.099) -- needs more inputs
      undecided on count_more_complex_selector (confounded) in [1.552,2.41) -- needs more inputs
      undecided on count_sel_namechar (confounded) in [20.88,57.5) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=110)
      undecided on count_class_selector (confounded) in [2.962,5.099) -- needs more inputs
      undecided on count_more_complex_selector (confounded) in [1.552,2.41) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_26 equivalent: ratio 1.02x within the equivalence band (95% CI 1.00-1.03, n=110)
      undecided on count_type_selector (confounded) in [1,1.893) -- needs more inputs
      undecided on count_class_selector (confounded) in [2.962,5.099) -- needs more inputs
      undecided on count_more_complex_selector (confounded) in [1.552,2.41) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_27 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.02, n=110)
      undecided on count_type_selector (confounded) in [1,1.893) -- needs more inputs
      undecided on count_class_selector (confounded) in [2.962,5.099) -- needs more inputs
      undecided on count_more_complex_selector (confounded) in [1.552,2.41) -- needs more inputs
  nwsapi_2_2_22 and nwsapi_2_2_23 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.01, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.02, n=109)
  nwsapi_2_2_22 and nwsapi_2_2_25 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.03, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_26 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.05, n=110)
      undecided on count_type_selector (confounded) in [1,1.893) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962) -- needs more inputs
  nwsapi_2_2_22 and nwsapi_2_2_27 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.05, n=110)
      undecided on count_type_selector (confounded) in [1,1.893) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962) -- needs more inputs
  nwsapi_2_2_23 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.00, n=109)
  nwsapi_2_2_23 and nwsapi_2_2_25 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.02, n=110)
  nwsapi_2_2_23 and nwsapi_2_2_26 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.04, n=110)
      undecided on count_type_selector (confounded) in [1,1.893) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962) -- needs more inputs
      undecided on count_sel_namechar (confounded) in [1,2.754) -- needs more inputs
  nwsapi_2_2_23 and nwsapi_2_2_27 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.03, n=110)
  nwsapi_2_2_24 and nwsapi_2_2_25 equivalent: ratio 1.02x within the equivalence band (95% CI 1.00-1.03, n=109)
      undecided on count_class_selector (confounded) in [1.721,2.962) -- needs more inputs
  nwsapi_2_2_24 and nwsapi_2_2_26 equivalent: ratio 1.02x within the equivalence band (95% CI 1.02-1.04, n=109)
      undecided on count_type_selector (confounded) in [1,1.893) -- needs more inputs
      undecided on count_class_selector (confounded) in [1.721,2.962) -- needs more inputs
  nwsapi_2_2_24 and nwsapi_2_2_27 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.03, n=109)
      undecided on count_class_selector (confounded) in [1.721,2.962) -- needs more inputs
  nwsapi_2_2_25 and nwsapi_2_2_26 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.03, n=110)
      undecided on count_sel_namechar (confounded) in [1,2.754) -- needs more inputs
  nwsapi_2_2_25 and nwsapi_2_2_27 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=110)
  nwsapi_2_2_26 and nwsapi_2_2_27 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=110)
[compare] rss: 110 inputs, 7 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_type_selector bins move with count_sel_namechar (1.5..23 across bins) -- those regions are joint, not count_type_selector findings
[compare] count_class_selector bins move with count_type_selector (1.5..5 across bins); count_sel_namechar (2..37 across bins) -- those regions are joint, not count_class_selector findings
[compare] count_more_complex_selector bins move with count_type_selector (1..6 across bins); count_sel_namechar (2..24 across bins) -- those regions are joint, not count_more_complex_selector findings
[compare] count_sel_namechar bins move with count_type_selector (1..5 across bins) -- those regions are joint, not count_sel_namechar findings
  nwsapi_2_2_21 and nwsapi_2_2_22 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_21 and nwsapi_2_2_23 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_21 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=109)
  nwsapi_2_2_21 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_21 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_21 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_23 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=109)
  nwsapi_2_2_22 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_23 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=109)
  nwsapi_2_2_23 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_23 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_23 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_24 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=109)
  nwsapi_2_2_24 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=109)
  nwsapi_2_2_24 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=109)
  nwsapi_2_2_25 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_25 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_26 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
[compare] dominance across runtime_ns, rss:
  nwsapi_2_2_21 and nwsapi_2_2_22 EQUIVALENT on every metric
  nwsapi_2_2_21 and nwsapi_2_2_23 EQUIVALENT on every metric
  nwsapi_2_2_21 and nwsapi_2_2_24 EQUIVALENT on every metric
  nwsapi_2_2_21 and nwsapi_2_2_25 EQUIVALENT on every metric
  nwsapi_2_2_21 and nwsapi_2_2_26 EQUIVALENT on every metric
  nwsapi_2_2_21 and nwsapi_2_2_27 EQUIVALENT on every metric
  nwsapi_2_2_22 and nwsapi_2_2_23 EQUIVALENT on every metric
  nwsapi_2_2_22 and nwsapi_2_2_24 EQUIVALENT on every metric
  nwsapi_2_2_22 and nwsapi_2_2_25 EQUIVALENT on every metric
  nwsapi_2_2_22 and nwsapi_2_2_26 EQUIVALENT on every metric
  nwsapi_2_2_22 and nwsapi_2_2_27 EQUIVALENT on every metric
  nwsapi_2_2_23 and nwsapi_2_2_24 EQUIVALENT on every metric
  nwsapi_2_2_23 and nwsapi_2_2_25 EQUIVALENT on every metric
  nwsapi_2_2_23 and nwsapi_2_2_26 EQUIVALENT on every metric
  nwsapi_2_2_23 and nwsapi_2_2_27 EQUIVALENT on every metric
  nwsapi_2_2_24 and nwsapi_2_2_25 EQUIVALENT on every metric
  nwsapi_2_2_24 and nwsapi_2_2_26 EQUIVALENT on every metric
  nwsapi_2_2_24 and nwsapi_2_2_27 EQUIVALENT on every metric
  nwsapi_2_2_25 and nwsapi_2_2_26 EQUIVALENT on every metric
  nwsapi_2_2_25 and nwsapi_2_2_27 EQUIVALENT on every metric
  nwsapi_2_2_26 and nwsapi_2_2_27 EQUIVALENT on every metric
      count_type_selector =0 (n=16): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_type_selector [1,1.893) (n=26): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_type_selector [1.893,3.583) (n=47): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_type_selector [3.583,6.782) (n=37): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_type_selector [6.782,12.84) (n=17): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_type_selector [12.84,24.3) (n=10): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_type_selector [24.3,46] (n=9): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_class_selector =0 (n=50): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_class_selector [1,1.721) (n=40): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_class_selector [1.721,2.962) (n=20): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_class_selector [2.962,5.099) (n=29): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_class_selector [5.099,8.776) (n=11): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_class_selector [8.776,15.11) (n=8): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector =0 (n=63): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [1,1.552) (n=37): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [1.552,2.41) (n=32): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [2.41,3.742) (n=10): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [3.742,5.809) (n=13): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar =0 (n=21): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar [1,2.754) (n=20): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar [2.754,7.583) (n=17): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar [7.583,20.88) (n=34): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar [20.88,57.5) (n=40): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar [57.5,158.3) (n=22): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_sel_namechar [158.3,436] (n=8): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
[interference] 6 property pair(s) tested over 1134 rows; 5 show a dependence
  count_class_selector vs runtime_ns changes with count_sel_namechar: rho by count_sel_namechar stratum = [-0.48, -0.20, -0.10, +0.18], spread 0.66, p=0.003
  count_more_complex_selector vs runtime_ns changes with count_sel_namechar: rho by count_sel_namechar stratum = [+0.32, +0.53, +0.67, +0.78], spread 0.47, p=0.003
  count_more_complex_selector vs runtime_ns changes with count_type_selector: rho by count_type_selector stratum = [+0.28, +0.23, +0.63, +0.70], spread 0.47, p=0.003
  count_class_selector vs runtime_ns changes with count_type_selector: rho by count_type_selector stratum = [-0.55, -0.25, -0.15, -0.17], spread 0.40, p=0.003
  count_sel_namechar vs runtime_ns changes with count_type_selector: rho by count_type_selector stratum = [-0.21, -0.04, -0.05, -0.37], spread 0.34, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
