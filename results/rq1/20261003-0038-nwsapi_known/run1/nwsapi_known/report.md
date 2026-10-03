# nwsapi_known

- corpus: 1127 rows, 161 inputs, 7 systems
- elapsed: 3443s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 44 | 21 |
| count_more_complex_selector | 0 | 30 | 15 |
| count_comma | 0 | 30 | 19 |
| count_complex_selector | 1 | 84 | 31 |
| count_combinator | 0 | 41 | 27 |
| count_type_selector | 0 | 60 | 32 |
| count_subclass_selectors | 0 | 94 | 37 |
| count_wq_name | 0 | 21 | 18 |
| count_class_selector | 0 | 28 | 25 |
| count_attribute_selector | 0 | 29 | 21 |
| count_id_selector | 0 | 18 | 19 |
| count_pseudo_class_selector | 0 | 35 | 23 |
| count_name | 1 | 221 | 99 |
| count_attr_value | 0 | 17 | 15 |
| count_attr_matcher_ws | 0 | 17 | 15 |
| count_attr_modifier | 0 | 9 | 9 |
| count_pseudo_class_function | 0 | 15 | 14 |
| count_pseudo_class_ident | 0 | 23 | 17 |
| count_namechar | 2 | 2043 | 150 |
| count_attr_ident | 0 | 14 | 11 |
| count_attr_value_words | 0 | 69 | 58 |
| count_relative_selector_list | 0 | 15 | 9 |
| count_rparen | 0 | 17 | 16 |
| count_nth_function | 0 | 2 | 3 |
| count_lparen | 0 | 17 | 16 |
| count_lang_range | 0 | 3 | 4 |
| count_more_value_word | 0 | 41 | 37 |
| count_more_relative_selector | 0 | 11 | 8 |
| count_lang_tag | 0 | 67 | 59 |
| count_relative_combinator | 0 | 8 | 5 |
| count_complex_selector_in_has | 0 | 54 | 12 |
| count_signed_integer | 0 | 1 | 2 |
| count_an_b_sign | 0 | 1 | 2 |
| count_an_a | 0 | 1 | 2 |
| count_digits | 0 | 4 | 5 |
| count_sign | 0 | 1 | 2 |
| count_subclass_selectors_in_has | 0 | 82 | 16 |
| count_pseudo_class_selector_in_has | 0 | 18 | 9 |
| count_pseudo_class_function_in_has | 0 | 10 | 8 |
| count_complex_selector_list_in_has | 0 | 17 | 8 |
| count_more_complex_selector_in_has | 0 | 10 | 6 |
| count_node | 1 | 36 | 29 |
| count_p | 0 | 11 | 12 |
| count_phrasing_content | 0 | 16 | 16 |
| count_phrasing_item | 0 | 104 | 36 |
| count_input | 0 | 36 | 27 |
| count_type_attr | 0 | 14 | 14 |
| count_a | 0 | 97 | 35 |
| count_href_attr | 0 | 14 | 15 |
| count_attrs | 1 | 144 | 64 |
| count_id_attr | 0 | 55 | 35 |
| count_title_attr | 0 | 60 | 40 |
| count_lang_attr | 0 | 32 | 32 |
| count_class_attr | 0 | 33 | 34 |
| count_class_list | 0 | 66 | 58 |
| count_text_run | 0 | 86 | 54 |
| count_tchar | 0 | 2007 | 107 |
| count_phrasing_element | 0 | 51 | 25 |
| count_span | 0 | 22 | 15 |
| count_b | 0 | 16 | 12 |
| count_em | 0 | 18 | 13 |
| count_data_attr | 0 | 33 | 33 |
| count_div | 0 | 27 | 25 |
| count_flow_content | 0 | 26 | 22 |
| count_flow_item | 0 | 143 | 47 |
| count_section | 0 | 14 | 11 |
| count_more_node | 0 | 24 | 16 |
| doc_depth | 3 | 18 | 14 |
| doc_bytes | 60 | 3835 | 153 |
| selector_len | 1 | 1859 | 108 |
| selector_nesting | 0 | 7 | 8 |

## frontier
[nwsapi_known] grammar frontier (targeting stopped asking here):
  count_a: pinned at 97 by the SEARCH; 1 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 115 inputs, 7 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_more_complex_selector bins move with count_attribute_selector (1..3 across bins) -- those regions are joint, not count_more_complex_selector findings
[compare] count_attribute_selector bins move with count_a (4..14 across bins) -- those regions are joint, not count_attribute_selector findings
[compare] count_a bins move with count_more_complex_selector (0.5..4 across bins); count_attribute_selector (1..15 across bins) -- those regions are joint, not count_a findings
  nwsapi_2_2_21 and nwsapi_2_2_22 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.01, n=113)
  nwsapi_2_2_21 and nwsapi_2_2_23 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.01, n=113)
  nwsapi_2_2_21 and nwsapi_2_2_24 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.01, n=110)
      undecided on count_a (confounded) in [4.595,9.849) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_25 equivalent: ratio 1.02x within the equivalence band (95% CI 1.00-1.03, n=113)
      undecided on count_a (confounded) in =0, [1,2.144), [4.595,9.849) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_26 equivalent: ratio 1.04x within the equivalence band (95% CI 1.02-1.06, n=113)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_attribute_selector (confounded) in =0 -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [2.144,4.595), [4.595,9.849) -- needs more inputs
  nwsapi_2_2_21 and nwsapi_2_2_27 equivalent: ratio 1.05x within the equivalence band (95% CI 1.03-1.08, n=113)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_attribute_selector (confounded) in [1,1.753) -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [2.144,4.595), [4.595,9.849) -- needs more inputs
  nwsapi_2_2_22 and nwsapi_2_2_23 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=113)
  nwsapi_2_2_22 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_25 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.04, n=113)
      undecided on count_a (confounded) in =0, [1,2.144) -- needs more inputs
  nwsapi_2_2_22 and nwsapi_2_2_26 equivalent: ratio 1.04x within the equivalence band (95% CI 1.03-1.06, n=113)
      undecided on count_a (confounded) in =0, [1,2.144), [21.11,45.25) -- needs more inputs
  nwsapi_2_2_22 and nwsapi_2_2_27 equivalent: ratio 1.06x within the equivalence band (95% CI 1.04-1.08, n=113)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_attribute_selector (confounded) in =0 -- needs more inputs
      undecided on count_attr_modifier in =0 -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [2.144,4.595), [4.595,9.849), [21.11,45.25) -- needs more inputs
  nwsapi_2_2_23 and nwsapi_2_2_24 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.02, n=110)
  nwsapi_2_2_23 and nwsapi_2_2_25 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.05, n=113)
  nwsapi_2_2_23 and nwsapi_2_2_26 equivalent: ratio 1.05x within the equivalence band (95% CI 1.03-1.07, n=113)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [2.144,4.595), [4.595,9.849), [21.11,45.25) -- needs more inputs
  nwsapi_2_2_23 and nwsapi_2_2_27 equivalent: ratio 1.07x within the equivalence band (95% CI 1.04-1.09, n=113)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_attribute_selector (confounded) in =0 -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [2.144,4.595), [4.595,9.849), [21.11,45.25) -- needs more inputs
  nwsapi_2_2_24 and nwsapi_2_2_25 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.04, n=110)
      undecided on count_a (confounded) in =0 -- needs more inputs
  nwsapi_2_2_24 and nwsapi_2_2_26 equivalent: ratio 1.04x within the equivalence band (95% CI 1.03-1.05, n=110)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_attribute_selector (confounded) in =0 -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [2.144,4.595) -- needs more inputs
  nwsapi_2_2_24 and nwsapi_2_2_27 equivalent: ratio 1.04x within the equivalence band (95% CI 1.04-1.07, n=110)
      undecided on count_more_complex_selector (confounded) in =0 -- needs more inputs
      undecided on count_attribute_selector (confounded) in =0 -- needs more inputs
      undecided on count_a (confounded) in =0, [1,2.144), [4.595,9.849), [21.11,45.25) -- needs more inputs
  nwsapi_2_2_25 and nwsapi_2_2_26 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.04, n=113)
  nwsapi_2_2_25 and nwsapi_2_2_27 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.04, n=113)
      undecided on count_a (confounded) in [4.595,9.849) -- needs more inputs
  nwsapi_2_2_26 and nwsapi_2_2_27 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.02, n=113)
[compare] rss: 115 inputs, 7 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_more_complex_selector bins move with count_attribute_selector (1..3 across bins) -- those regions are joint, not count_more_complex_selector findings
[compare] count_attribute_selector bins move with count_a (4..14 across bins) -- those regions are joint, not count_attribute_selector findings
[compare] count_a bins move with count_more_complex_selector (0.5..4 across bins); count_attribute_selector (1..15 across bins) -- those regions are joint, not count_a findings
  nwsapi_2_2_21 and nwsapi_2_2_22 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_21 and nwsapi_2_2_23 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_21 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_21 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_21 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_21 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_22 and nwsapi_2_2_23 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_22 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_22 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_22 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_22 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_23 and nwsapi_2_2_24 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_23 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_23 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_23 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_24 and nwsapi_2_2_25 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_24 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_24 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=110)
  nwsapi_2_2_25 and nwsapi_2_2_26 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_25 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
  nwsapi_2_2_26 and nwsapi_2_2_27 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=113)
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
      count_more_complex_selector =0 (n=67): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [1,1.763) (n=22): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [1.763,3.107) (n=31): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [3.107,5.477) (n=10): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [5.477,9.655) (n=12): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_more_complex_selector [9.655,17.02) (n=12): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attribute_selector =0 (n=58): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attribute_selector [1,1.753) (n=21): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attribute_selector [1.753,3.072) (n=31): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attribute_selector [3.072,5.385) (n=15): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attribute_selector [9.439,16.54) (n=16): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attribute_selector [16.54,29] (n=13): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attr_modifier =0 (n=93): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attr_modifier [1,2.333) (n=50): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_attr_modifier [2.333,3.667) (n=12): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_a =0 (n=32): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_a [1,2.144) (n=21): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_a [2.144,4.595) (n=18): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_a [4.595,9.849) (n=23): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_a [9.849,21.11) (n=50): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
      count_a [21.11,45.25) (n=11): nwsapi_2_2_21, nwsapi_2_2_22, nwsapi_2_2_23, nwsapi_2_2_24, nwsapi_2_2_25, nwsapi_2_2_26, nwsapi_2_2_27 not dominated
[interference] 3 property pair(s) tested over 1127 rows; 1 show a dependence
  count_attr_modifier vs runtime_ns changes with count_a: rho by count_a stratum = [+0.32, +0.24, +0.02, +0.31], spread 0.30, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
