# domselector_known

- corpus: 1116 rows, 124 inputs, 9 systems
- elapsed: 3503s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 21 | 13 |
| count_more_complex_selector | 0 | 10 | 11 |
| count_comma | 0 | 15 | 12 |
| count_complex_selector | 1 | 68 | 24 |
| count_combinator | 0 | 47 | 23 |
| count_subclass_selectors | 0 | 161 | 32 |
| count_type_selector | 0 | 55 | 27 |
| count_wq_name | 0 | 16 | 14 |
| count_class_selector | 0 | 40 | 20 |
| count_id_selector | 0 | 50 | 20 |
| count_attribute_selector | 0 | 55 | 20 |
| count_pseudo_class_selector | 0 | 20 | 13 |
| count_name | 2 | 221 | 76 |
| count_attr_modifier | 0 | 9 | 9 |
| count_attr_value | 0 | 25 | 17 |
| count_attr_matcher_ws | 0 | 25 | 17 |
| count_pseudo_class_ident | 0 | 14 | 11 |
| count_pseudo_class_function | 0 | 12 | 11 |
| count_namechar | 8 | 2043 | 110 |
| count_attr_value_words | 0 | 69 | 52 |
| count_attr_ident | 0 | 14 | 11 |
| count_relative_selector_list | 0 | 15 | 9 |
| count_nth_function | 0 | 2 | 3 |
| count_lparen | 0 | 17 | 14 |
| count_rparen | 0 | 17 | 14 |
| count_lang_range | 0 | 3 | 4 |
| count_more_value_word | 0 | 41 | 36 |
| count_more_relative_selector | 0 | 11 | 8 |
| count_lang_tag | 0 | 67 | 52 |
| count_relative_combinator | 0 | 8 | 5 |
| count_complex_selector_in_has | 0 | 54 | 11 |
| count_an_b_sign | 0 | 1 | 2 |
| count_an_a | 0 | 1 | 2 |
| count_digits | 0 | 3 | 4 |
| count_signed_integer | 0 | 1 | 2 |
| count_sign | 0 | 1 | 2 |
| count_subclass_selectors_in_has | 0 | 82 | 13 |
| count_pseudo_class_selector_in_has | 0 | 18 | 7 |
| count_pseudo_class_function_in_has | 0 | 9 | 5 |
| count_complex_selector_list_in_has | 0 | 16 | 6 |
| count_more_complex_selector_in_has | 0 | 10 | 4 |
| count_node | 1 | 27 | 25 |
| count_p | 0 | 11 | 11 |
| count_attrs | 1 | 144 | 51 |
| count_id_attr | 0 | 55 | 33 |
| count_title_attr | 0 | 60 | 38 |
| count_data_attr | 0 | 33 | 33 |
| count_lang_attr | 0 | 32 | 32 |
| count_class_attr | 0 | 33 | 33 |
| count_class_list | 0 | 66 | 50 |
| count_phrasing_content | 0 | 16 | 15 |
| count_text_run | 0 | 86 | 48 |
| count_tchar | 0 | 2007 | 85 |
| count_phrasing_item | 0 | 104 | 31 |
| count_input | 0 | 36 | 27 |
| count_type_attr | 0 | 14 | 14 |
| count_a | 0 | 97 | 34 |
| count_href_attr | 0 | 14 | 15 |
| count_phrasing_element | 0 | 51 | 21 |
| count_em | 0 | 18 | 13 |
| count_b | 0 | 16 | 12 |
| count_span | 0 | 22 | 15 |
| count_section | 0 | 8 | 9 |
| count_flow_content | 0 | 26 | 22 |
| count_flow_item | 0 | 143 | 40 |
| count_div | 0 | 27 | 24 |
| count_more_node | 0 | 16 | 15 |
| doc_depth | 3 | 18 | 14 |
| doc_bytes | 65 | 3835 | 113 |
| selector_len | 1 | 1859 | 86 |
| selector_nesting | 0 | 11 | 8 |

## comparison
[compare] runtime_ns: 124 inputs, 9 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_attribute_selector bins move with count_node (3..11 across bins); count_tchar (23..232 across bins) -- those regions are joint, not count_attribute_selector findings
[compare] count_name bins move with count_attribute_selector (1..3 across bins); count_node (1..12.5 across bins); count_tchar (7..237.5 across bins) -- those regions are joint, not count_name findings
[compare] count_node bins move with count_attribute_selector (1..17.5 across bins); count_name (12..156 across bins); count_tchar (8..235 across bins) -- those regions are joint, not count_node findings
[compare] count_tchar bins move with count_attribute_selector (1..20 across bins); count_name (8..152 across bins); count_node (1..13 across bins) -- those regions are joint, not count_tchar findings
  domselector_8_2_4 and domselector_8_2_5 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.01, n=124)
      undecided on count_attribute_selector (confounded) in [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_8_2_4 and domselector_9_0_3 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.02, n=124)
      undecided on count_attribute_selector (confounded) in [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_8_2_4 and domselector_9_0_4 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.05, n=124)
      undecided on count_attribute_selector (confounded) in [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5) -- needs more inputs
  domselector_8_2_4 and domselector_9_1_0 equivalent: ratio 1.05x within the equivalence band (95% CI 1.03-1.07, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416), [14.46,28.2), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02), [21.02,46.05), [46.05,100.9) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [3,5.196), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5) -- needs more inputs
  domselector_8_2_4 and domselector_9_1_1 equivalent: ratio 1.04x within the equivalence band (95% CI 1.02-1.07, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [3.803,7.416), [14.46,28.2), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [46.05,100.9) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [3,5.196), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [20.02,63.36), [63.36,200.5) -- needs more inputs
  domselector_8_2_4 and domselector_9_1_2 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.06, n=124)
      undecided on count_attribute_selector (confounded) in [14.46,28.2), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [46.05,100.9) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [3,5.196), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [20.02,63.36) -- needs more inputs
  domselector_8_2_4 and domselector_9_2_1 equivalent: ratio 1.06x within the equivalence band (95% CI 1.04-1.09, n=124)
      DEPENDS ON SAMPLING: counting each count_name bin once gives 1.06x (95% CI 1.03-1.11, 5 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 1 count_name bin(s) have too little data to enter that: [2,4.381)
      DEPENDS ON SAMPLING: counting each count_node bin once gives 1.08x (95% CI 1.04-1.11, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      undecided on count_attribute_selector (confounded) in [1,1.95), [1.95,3.803), [3.803,7.416), [14.46,28.2), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [46.05,100.9) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [3,5.196), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5) -- needs more inputs
  domselector_8_2_4 vs domselector_9_2_2 undecided: domselector_8_2_4 ahead by 1.10x but the 95% CI (1.07-1.11, n=124) spans the equivalence band
      undecided on count_attribute_selector (confounded) in =0, [1,1.95), [1.95,3.803), [3.803,7.416), [14.46,28.2), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [46.05,100.9), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1,1.732), [1.732,3), [3,5.196), [5.196,9), [9,15.59), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in =0, [6.328,20.02), [20.02,63.36), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_8_2_5 and domselector_9_0_3 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.03, n=124)
      undecided on count_node (confounded) in [5.196,9) -- needs more inputs
  domselector_8_2_5 and domselector_9_0_4 equivalent: ratio 1.04x within the equivalence band (95% CI 1.02-1.06, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [63.36,200.5) -- needs more inputs
  domselector_8_2_5 and domselector_9_1_0 equivalent: ratio 1.06x within the equivalence band (95% CI 1.04-1.08, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5) -- needs more inputs
  domselector_8_2_5 and domselector_9_1_1 equivalent: ratio 1.07x within the equivalence band (95% CI 1.05-1.08, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_8_2_5 and domselector_9_1_2 equivalent: ratio 1.06x within the equivalence band (95% CI 1.04-1.08, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02), [21.02,46.05), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [3,5.196), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [20.02,63.36), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_8_2_5 and domselector_9_2_1 equivalent: ratio 1.07x within the equivalence band (95% CI 1.05-1.09, n=124)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 1.08x (95% CI 1.06-1.10, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 1 count_attribute_selector bin(s) have too little data to enter that: [7.416,14.46)
      DEPENDS ON SAMPLING: counting each count_node bin once gives 1.08x (95% CI 1.06-1.11, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      undecided on count_attribute_selector (confounded) in [1,1.95), [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [3,5.196), [5.196,9), [9,15.59), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in =0, [6.328,20.02), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_8_2_5 vs domselector_9_2_2 undecided: domselector_8_2_5 ahead by 1.11x but the 95% CI (1.07-1.13, n=124) spans the equivalence band
      undecided on count_attribute_selector (confounded) in =0, [1,1.95), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [46.05,100.9), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1,1.732), [1.732,3), [3,5.196), [9,15.59), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in =0, [6.328,20.02), [20.02,63.36), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_9_0_3 and domselector_9_0_4 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.04, n=124)
      undecided on count_node (confounded) in [15.59,27] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_0 equivalent: ratio 1.05x within the equivalence band (95% CI 1.03-1.07, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [3.803,7.416) -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_3 and domselector_9_1_1 equivalent: ratio 1.05x within the equivalence band (95% CI 1.04-1.06, n=124)
      undecided on count_attribute_selector (confounded) in [1,1.95), [3.803,7.416), [14.46,28.2) -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_3 and domselector_9_1_2 equivalent: ratio 1.05x within the equivalence band (95% CI 1.03-1.07, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416) -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_3 and domselector_9_2_1 equivalent: ratio 1.06x within the equivalence band (95% CI 1.05-1.08, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_node (confounded) in [1,1.732), [1.732,3), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_3 vs domselector_9_2_2 undecided: domselector_9_0_3 ahead by 1.09x but the 95% CI (1.06-1.10, n=124) spans the equivalence band
      undecided on count_attribute_selector (confounded) in =0, [1,1.95), [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [46.05,100.9), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1,1.732), [1.732,3), [5.196,9), [9,15.59), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_9_0_4 and domselector_9_1_0 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.03, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_4 and domselector_9_1_1 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.04, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416) -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_4 and domselector_9_1_2 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.03, n=124)
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_0_4 and domselector_9_2_1 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.05, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416) -- needs more inputs
      undecided on count_name (confounded) in [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
  domselector_9_0_4 and domselector_9_2_2 equivalent: ratio 1.05x within the equivalence band (95% CI 1.03-1.08, n=124)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 1.06x (95% CI 1.04-1.11, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 1 count_attribute_selector bin(s) have too little data to enter that: [7.416,14.46)
      DEPENDS ON SAMPLING: counting each count_name bin once gives 1.07x (95% CI 1.03-1.11, 5 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 1 count_name bin(s) have too little data to enter that: [2,4.381)
      DEPENDS ON SAMPLING: counting each count_node bin once gives 1.07x (95% CI 1.04-1.11, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      undecided on count_attribute_selector (confounded) in =0, [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05), [100.9,221] -- needs more inputs
      undecided on count_node (confounded) in [1,1.732), [1.732,3), [5.196,9), [15.59,27] -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02), [63.36,200.5), [200.5,634.3) -- needs more inputs
  domselector_9_1_0 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=124)
  domselector_9_1_0 and domselector_9_1_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.01, n=124)
  domselector_9_1_0 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.02, n=124)
      undecided on count_node (confounded) in [5.196,9) -- needs more inputs
  domselector_9_1_0 and domselector_9_2_2 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.04, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_1_1 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.00, n=124)
  domselector_9_1_1 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.03, n=124)
      undecided on count_node (confounded) in [5.196,9) -- needs more inputs
  domselector_9_1_1 and domselector_9_2_2 equivalent: ratio 1.03x within the equivalence band (95% CI 1.01-1.05, n=124)
      undecided on count_attribute_selector (confounded) in [1.95,3.803), [3.803,7.416), [28.2,55] -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02) -- needs more inputs
      undecided on count_node (confounded) in [1,1.732), [1.732,3), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in =0 -- needs more inputs
  domselector_9_1_2 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=124)
      undecided on count_node (confounded) in [5.196,9) -- needs more inputs
  domselector_9_1_2 and domselector_9_2_2 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.04, n=124)
      undecided on count_attribute_selector (confounded) in =0, [1.95,3.803), [3.803,7.416) -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
      undecided on count_tchar (confounded) in [6.328,20.02) -- needs more inputs
  domselector_9_2_1 and domselector_9_2_2 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.05, n=124)
      undecided on count_attribute_selector (confounded) in [3.803,7.416) -- needs more inputs
      undecided on count_name (confounded) in [4.381,9.597), [9.597,21.02), [21.02,46.05) -- needs more inputs
      undecided on count_node (confounded) in [1.732,3), [5.196,9) -- needs more inputs
[compare] rss: 124 inputs, 9 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_attribute_selector bins move with count_node (3..11 across bins); count_tchar (23..232 across bins) -- those regions are joint, not count_attribute_selector findings
[compare] count_name bins move with count_attribute_selector (1..3 across bins); count_node (1..12.5 across bins); count_tchar (7..237.5 across bins) -- those regions are joint, not count_name findings
[compare] count_node bins move with count_attribute_selector (1..17.5 across bins); count_name (12..156 across bins); count_tchar (8..235 across bins) -- those regions are joint, not count_node findings
[compare] count_tchar bins move with count_attribute_selector (1..20 across bins); count_name (8..152 across bins); count_node (1..13 across bins) -- those regions are joint, not count_tchar findings
  domselector_8_2_4 and domselector_8_2_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_0_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_0_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_1_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_4 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_8_2_5 and domselector_9_0_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_5 and domselector_9_0_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_5 and domselector_9_1_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_5 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_5 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_5 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_8_2_5 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_9_0_3 and domselector_9_0_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_3 and domselector_9_1_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_3 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_3 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_3 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_3 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_9_0_4 and domselector_9_1_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_4 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_4 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_4 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_0_4 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_9_1_0 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_1_0 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_1_0 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_1_0 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_9_1_1 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_1_1 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_1_1 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_9_1_2 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=124)
  domselector_9_1_2 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=124)
  domselector_9_2_1 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.01, n=124)
[compare] dominance across runtime_ns, rss:
  domselector_8_2_4 and domselector_8_2_5 EQUIVALENT on every metric
  domselector_8_2_4 and domselector_9_0_3 EQUIVALENT on every metric
  domselector_8_2_4 and domselector_9_0_4 EQUIVALENT on every metric
  domselector_8_2_4 and domselector_9_1_0 EQUIVALENT on every metric
  domselector_8_2_4 and domselector_9_1_1 EQUIVALENT on every metric
  domselector_8_2_4 and domselector_9_1_2 EQUIVALENT on every metric
  domselector_8_2_4 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_8_2_4 vs domselector_9_2_2 undecided on every metric
  domselector_8_2_5 and domselector_9_0_3 EQUIVALENT on every metric
  domselector_8_2_5 and domselector_9_0_4 EQUIVALENT on every metric
  domselector_8_2_5 and domselector_9_1_0 EQUIVALENT on every metric
  domselector_8_2_5 and domselector_9_1_1 EQUIVALENT on every metric
  domselector_8_2_5 and domselector_9_1_2 EQUIVALENT on every metric
  domselector_8_2_5 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_8_2_5 vs domselector_9_2_2 undecided on every metric
  domselector_9_0_3 and domselector_9_0_4 EQUIVALENT on every metric
  domselector_9_0_3 and domselector_9_1_0 EQUIVALENT on every metric
  domselector_9_0_3 and domselector_9_1_1 EQUIVALENT on every metric
  domselector_9_0_3 and domselector_9_1_2 EQUIVALENT on every metric
  domselector_9_0_3 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_9_0_3 vs domselector_9_2_2 undecided on every metric
  domselector_9_0_4 and domselector_9_1_0 EQUIVALENT on every metric
  domselector_9_0_4 and domselector_9_1_1 EQUIVALENT on every metric
  domselector_9_0_4 and domselector_9_1_2 EQUIVALENT on every metric
  domselector_9_0_4 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_9_0_4 and domselector_9_2_2 EQUIVALENT on every metric
  domselector_9_1_0 and domselector_9_1_1 EQUIVALENT on every metric
  domselector_9_1_0 and domselector_9_1_2 EQUIVALENT on every metric
  domselector_9_1_0 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_9_1_0 and domselector_9_2_2 EQUIVALENT on every metric
  domselector_9_1_1 and domselector_9_1_2 EQUIVALENT on every metric
  domselector_9_1_1 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_9_1_1 and domselector_9_2_2 EQUIVALENT on every metric
  domselector_9_1_2 and domselector_9_2_1 EQUIVALENT on every metric
  domselector_9_1_2 and domselector_9_2_2 EQUIVALENT on every metric
  domselector_9_2_1 and domselector_9_2_2 EQUIVALENT on every metric
      count_attribute_selector =0 (n=35): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attribute_selector [1,1.95) (n=23): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attribute_selector [1.95,3.803) (n=29): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1 not dominated
      count_attribute_selector [3.803,7.416) (n=10): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attribute_selector [14.46,28.2) (n=13): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attribute_selector [28.2,55] (n=11): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_name [4.381,9.597) (n=11): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_name [9.597,21.02) (n=10): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_name [21.02,46.05) (n=11): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_name [46.05,100.9) (n=32): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_name [100.9,221] (n=58): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_node [1,1.732) (n=26): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_node [1.732,3) (n=9): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_node [3,5.196) (n=22): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_node [5.196,9) (n=9): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1 not dominated
      count_node [9,15.59) (n=37): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_node [15.59,27] (n=21): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_tchar =0 (n=11): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_tchar [6.328,20.02) (n=12): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_tchar [20.02,63.36) (n=28): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_tchar [63.36,200.5) (n=23): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_tchar [200.5,634.3) (n=40): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
[interference] 9 property pair(s) tested over 1116 rows; 8 show a dependence
  count_name vs runtime_ns changes with count_tchar: rho by count_tchar stratum = [+0.47, +0.55, +0.24, -0.10], spread 0.65, p=0.003
  count_node vs runtime_ns changes with count_tchar: rho by count_tchar stratum = [+0.08, +0.60, +0.06, +0.06], spread 0.54, p=0.003
  count_node vs runtime_ns changes with count_name: rho by count_name stratum = [+0.06, +0.13, -0.32, +0.15], spread 0.47, p=0.003
  count_attribute_selector vs runtime_ns changes with count_name: rho by count_name stratum = [+0.27, +0.11, +0.57, +0.30], spread 0.46, p=0.003
  count_tchar vs runtime_ns changes with count_node: rho by count_node stratum = [+0.11, +0.23, -0.12, +0.06], spread 0.35, p=0.003
  count_attribute_selector vs runtime_ns changes with count_node: rho by count_node stratum = [+0.33, +0.35, +0.61, +0.40], spread 0.28, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
