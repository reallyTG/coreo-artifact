# domselector_tailored

- corpus: 864 rows, 96 inputs, 9 systems
- elapsed: 3522s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector | 0 | 15 | 14 |
| count_type_selector | 0 | 7 | 8 |
| count_nth_function | 0 | 15 | 11 |
| count_digits | 0 | 18 | 15 |
| count_an_a | 0 | 9 | 7 |
| count_sign | 0 | 4 | 5 |
| count_signed_integer | 0 | 3 | 4 |
| count_an_b_sign | 0 | 4 | 5 |
| count_attribute_selector | 0 | 11 | 11 |
| count_attr_name | 0 | 5 | 6 |
| count_short_name | 87 | 2374 | 92 |
| count_namechar | 161 | 4659 | 93 |
| count_attr_modifier | 0 | 4 | 5 |
| count_attr_value | 0 | 9 | 10 |
| count_eq_attr_name | 0 | 9 | 10 |
| count_attr_matcher_ws | 0 | 9 | 10 |
| count_trailing_subclasses | 0 | 21 | 15 |
| count_id_selector | 0 | 4 | 5 |
| count_class_selector | 0 | 5 | 5 |
| count_pseudo_class_ident | 0 | 5 | 6 |
| count_combinator | 0 | 9 | 9 |
| count_bare_attribute | 0 | 1 | 2 |
| count_more_complex_selector | 0 | 7 | 7 |
| count_node | 20 | 1000 | 73 |
| count_section | 4 | 269 | 73 |
| count_phrasing_content | 9 | 399 | 67 |
| count_phrasing_item | 6 | 159 | 57 |
| count_text_run | 12 | 528 | 82 |
| count_tchar | 23 | 1067 | 92 |
| count_leaf_span | 0 | 64 | 40 |
| count_attrs | 28 | 1024 | 79 |
| count_class_attr | 9 | 412 | 80 |
| count_lang_attr | 11 | 364 | 78 |
| count_lang_subtag | 18 | 555 | 84 |
| count_data_attr | 9 | 375 | 78 |
| count_id_attr | 12 | 373 | 80 |
| count_a | 0 | 65 | 43 |
| count_input | 0 | 61 | 38 |
| count_type_attr | 0 | 36 | 27 |
| count_p | 1 | 286 | 67 |
| count_phrasing_element | 3 | 270 | 68 |
| count_em | 0 | 105 | 53 |
| count_span | 0 | 98 | 50 |
| count_b | 0 | 97 | 52 |
| count_div | 4 | 266 | 72 |
| count_more_node | 19 | 999 | 73 |
| doc_depth | 4 | 4 | 1 |
| doc_bytes | 1273 | 33685 | 96 |
| selector_len | 4 | 521 | 65 |
| selector_nesting | 0 | 1 | 2 |

## comparison
[compare] runtime_ns: 96 inputs, 9 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_attr_modifier bins move with count_attribute_selector (1.5..7 across bins) -- those regions are joint, not count_attr_modifier findings
  domselector_8_2_4 and domselector_8_2_5 equivalent: ratio 0.98x within the equivalence band (95% CI 0.94-1.01, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.91x (95% CI 0.86-1.00, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.92x (95% CI 0.84-1.01, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 and domselector_9_0_3 equivalent: ratio 1.03x within the equivalence band (95% CI 0.96-1.05, n=96)
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.96x (95% CI 0.89-1.08, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      undecided on count_attribute_selector in =0, [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0, =1 -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_0_4 undecided: domselector_9_0_4 ahead by 1.01x but the 95% CI (0.88-1.03, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.66-0.82, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.53x (95% CI 0.51-0.55, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_1_0 undecided: domselector_9_1_0 ahead by 1.01x but the 95% CI (0.88-1.02, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.67x (95% CI 0.65-0.81, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.53x (95% CI 0.51-0.55, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_1_1 undecided: domselector_8_2_4 ahead by 1.00x but the 95% CI (0.90-1.03, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.66-0.83, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.54x (95% CI 0.51-0.55, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_1_2 undecided: domselector_9_1_2 ahead by 1.04x but the 95% CI (0.73-1.00, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.67x (95% CI 0.61-0.81, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.53x (95% CI 0.50-0.55, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_2_1 undecided: domselector_9_2_1 ahead by 1.02x but the 95% CI (0.71-1.02, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.69x (95% CI 0.61-0.80, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.53x (95% CI 0.51-0.56, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_2_2 undecided: domselector_9_2_2 ahead by 1.03x but the 95% CI (0.74-1.06, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.69x (95% CI 0.61-0.80, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.54x (95% CI 0.52-0.57, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_0_3 equivalent: ratio 1.06x within the equivalence band (95% CI 1.04-1.07, n=96)
  domselector_8_2_5 vs domselector_9_0_4 undecided: domselector_8_2_5 ahead by 1.03x but the 95% CI (1.00-1.13, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.74x (95% CI 0.68-0.80, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.55x (95% CI 0.53-0.58, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 vs domselector_9_1_0 undecided: domselector_8_2_5 ahead by 1.05x but the 95% CI (1.01-1.13, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.72x (95% CI 0.68-0.81, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.55x (95% CI 0.53-0.58, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 vs domselector_9_1_1 undecided: domselector_8_2_5 ahead by 1.05x but the 95% CI (1.01-1.13, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.73x (95% CI 0.70-0.80, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.56x (95% CI 0.54-0.58, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      crossover on count_attribute_selector: domselector_9_1_1 better at 0, domselector_8_2_5 better above 4.946
      undecided on count_attribute_selector in [1,1.491) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0 -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_1_2 equivalent: ratio 1.03x within the equivalence band (95% CI 0.99-1.08, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.71x (95% CI 0.67-0.79, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.11x (95% CI 0.75-1.16, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.55x (95% CI 0.53-0.56, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.02x (95% CI 0.73-1.08, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_2_1 equivalent: ratio 1.06x within the equivalence band (95% CI 1.03-1.09, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.71x (95% CI 0.68-0.78, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.11x (95% CI 0.77-1.17, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.55x (95% CI 0.53-0.57, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.05x (95% CI 0.74-1.09, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 vs domselector_9_2_2 undecided: domselector_8_2_5 ahead by 1.09x but the 95% CI (1.02-1.14, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.72x (95% CI 0.67-0.79, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.56x (95% CI 0.54-0.58, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [2,2.5) -- needs more inputs
      crossover on count_bare_attribute: domselector_8_2_5 better at 0, domselector_9_2_2 better at 1
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_0_4 equivalent: ratio 1.02x within the equivalence band (95% CI 0.99-1.08, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.65-0.75, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.10x (95% CI 0.72-1.13, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.52x (95% CI 0.51-0.53, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.03x (95% CI 0.72-1.08, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_0 equivalent: ratio 1.04x within the equivalence band (95% CI 1.02-1.08, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.65-0.76, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.11x (95% CI 0.72-1.13, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.52x (95% CI 0.50-0.54, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.04x (95% CI 0.72-1.08, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_1 equivalent: ratio 1.05x within the equivalence band (95% CI 1.01-1.09, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.69x (95% CI 0.66-0.75, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.10x (95% CI 0.72-1.12, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.53x (95% CI 0.51-0.54, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.04x (95% CI 0.73-1.09, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_2 equivalent: ratio 1.02x within the equivalence band (95% CI 1.00-1.05, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.66x (95% CI 0.63-0.74, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.06x (95% CI 0.69-1.10, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.52x (95% CI 0.50-0.53, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.02x (95% CI 0.71-1.05, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_2_1 equivalent: ratio 1.04x within the equivalence band (95% CI 1.01-1.07, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.67x (95% CI 0.65-0.74, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.07x (95% CI 0.71-1.11, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.52x (95% CI 0.51-0.53, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.03x (95% CI 0.72-1.06, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [111.4,286] -- needs more inputs
  domselector_9_0_3 vs domselector_9_2_2 undecided: domselector_9_0_3 ahead by 1.04x but the 95% CI (1.01-1.11, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.64-0.74, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.53x (95% CI 0.51-0.54, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [111.4,286] -- needs more inputs
  domselector_9_0_4 and domselector_9_1_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.01, n=96)
  domselector_9_0_4 and domselector_9_1_1 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
  domselector_9_0_4 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=96)
  domselector_9_0_4 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
      undecided on count_attr_modifier (confounded) in [2,2.5) -- needs more inputs
  domselector_9_0_4 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
      undecided on count_attr_modifier (confounded) in [2,2.5) -- needs more inputs
  domselector_9_1_0 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=96)
  domselector_9_1_0 and domselector_9_1_2 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.00, n=96)
  domselector_9_1_0 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 0.98-1.02, n=96)
  domselector_9_1_0 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91) -- needs more inputs
  domselector_9_1_1 and domselector_9_1_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.00, n=96)
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
  domselector_9_1_1 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=96)
  domselector_9_1_1 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.02, n=96)
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [2,2.5) -- needs more inputs
  domselector_9_1_2 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
  domselector_9_1_2 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
      undecided on count_p in [6.589,16.91) -- needs more inputs
  domselector_9_2_1 and domselector_9_2_2 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=96)
[compare] fresh_ns: 96 inputs, 9 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_attr_modifier bins move with count_attribute_selector (1.5..7 across bins) -- those regions are joint, not count_attr_modifier findings
  domselector_8_2_4 vs domselector_8_2_5 undecided: domselector_8_2_5 ahead by 1.03x but the 95% CI (0.87-1.00, n=96) spans the equivalence band
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_0_3 undecided: domselector_9_0_3 ahead by 1.03x but the 95% CI (0.90-1.05, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.96x (95% CI 0.92-1.00, 3 bins, equal weight per bin), verdict 'equivalent' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 1.00x (95% CI 0.97-1.03, 2 bins, equal weight per bin), verdict 'equivalent' not 'undecided'
      undecided on count_attribute_selector in =0, [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0, =1 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_4 vs domselector_9_0_4 undecided: domselector_9_0_4 ahead by 1.40x but the 95% CI (0.34-0.99, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.64x (95% CI 0.60-0.66, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.65x (95% CI 0.53-0.85, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.46-0.51, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 0.69x (95% CI 0.40-0.74, 4 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4) -- needs more inputs
  domselector_8_2_4 vs domselector_9_1_0 undecided: domselector_9_1_0 ahead by 1.42x but the 95% CI (0.36-1.00, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.64x (95% CI 0.60-0.66, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.66x (95% CI 0.53-0.85, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.49x (95% CI 0.46-0.52, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 0.69x (95% CI 0.40-0.74, 4 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4) -- needs more inputs
  domselector_8_2_4 vs domselector_9_1_1 undecided: domselector_9_1_1 ahead by 1.45x but the 95% CI (0.36-0.99, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.64x (95% CI 0.60-0.67, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.66x (95% CI 0.53-0.85, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.50x (95% CI 0.46-0.51, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 0.69x (95% CI 0.40-0.74, 4 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4) -- needs more inputs
  domselector_8_2_4 vs domselector_9_1_2 undecided: domselector_9_1_2 ahead by 1.62x but the 95% CI (0.36-0.95, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.61x (95% CI 0.55-0.65, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.65x (95% CI 0.50-0.81, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.45-0.49, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 0.64x (95% CI 0.40-0.72, 4 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4) -- needs more inputs
  domselector_8_2_4 vs domselector_9_2_1 undecided: domselector_9_2_1 ahead by 1.62x but the 95% CI (0.36-0.97, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.63x (95% CI 0.55-0.66, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.66x (95% CI 0.50-0.82, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.45-0.51, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 0.64x (95% CI 0.40-0.73, 4 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4) -- needs more inputs
  domselector_8_2_4 vs domselector_9_2_2 undecided: domselector_9_2_2 ahead by 1.56x but the 95% CI (0.38-0.94, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.61x (95% CI 0.54-0.66, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.66x (95% CI 0.50-0.82, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.47x (95% CI 0.45-0.50, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 0.64x (95% CI 0.40-0.73, 4 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4) -- needs more inputs
  domselector_8_2_5 and domselector_9_0_3 equivalent: ratio 1.05x within the equivalence band (95% CI 1.04-1.07, n=96)
  domselector_8_2_5 vs domselector_9_0_4 undecided: domselector_8_2_5 ahead by 1.04x but the 95% CI (0.98-1.10, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.67x (95% CI 0.63-0.73, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.51x (95% CI 0.48-0.53, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 vs domselector_9_1_0 undecided: domselector_8_2_5 ahead by 1.04x but the 95% CI (1.00-1.12, n=96) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.64-0.76, 3 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.51x (95% CI 0.49-0.54, 2 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_1_1 equivalent: ratio 1.04x within the equivalence band (95% CI 1.00-1.10, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.68x (95% CI 0.65-0.75, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.11x (95% CI 0.72-1.14, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.51x (95% CI 0.48-0.54, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.03x (95% CI 0.71-1.11, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_1_2 equivalent: ratio 1.02x within the equivalence band (95% CI 0.98-1.06, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.65x (95% CI 0.62-0.71, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.08x (95% CI 0.71-1.11, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.50x (95% CI 0.47-0.52, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.00x (95% CI 0.70-1.06, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_2_1 equivalent: ratio 1.02x within the equivalence band (95% CI 1.00-1.07, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.66x (95% CI 0.62-0.71, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.08x (95% CI 0.71-1.12, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.50x (95% CI 0.48-0.52, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.02x (95% CI 0.70-1.07, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_8_2_5 and domselector_9_2_2 equivalent: ratio 1.03x within the equivalence band (95% CI 0.98-1.07, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.65x (95% CI 0.62-0.72, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.05x (95% CI 0.71-1.10, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.50x (95% CI 0.48-0.52, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.01x (95% CI 0.69-1.07, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_0_4 equivalent: ratio 1.02x within the equivalence band (95% CI 0.99-1.07, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.64x (95% CI 0.61-0.67, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.07x (95% CI 0.66-1.11, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.49x (95% CI 0.46-0.50, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.02x (95% CI 0.69-1.07, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_0 equivalent: ratio 1.04x within the equivalence band (95% CI 1.01-1.07, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.64x (95% CI 0.62-0.69, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.09x (95% CI 0.68-1.12, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.46-0.50, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.03x (95% CI 0.71-1.07, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_1 equivalent: ratio 1.04x within the equivalence band (95% CI 1.00-1.07, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.65x (95% CI 0.63-0.68, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.06x (95% CI 0.66-1.10, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.49x (95% CI 0.46-0.51, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.03x (95% CI 0.70-1.07, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491), [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_bare_attribute in =0 -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [43.41,111.4), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_1_2 equivalent: ratio 1.02x within the equivalence band (95% CI 0.98-1.05, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.63x (95% CI 0.61-0.67, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.04x (95% CI 0.65-1.08, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.45-0.49, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.01x (95% CI 0.68-1.04, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_2_1 equivalent: ratio 1.03x within the equivalence band (95% CI 0.99-1.05, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.63x (95% CI 0.61-0.67, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.04x (95% CI 0.65-1.07, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.46-0.49, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.03x (95% CI 0.69-1.05, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [16.91,43.41), [111.4,286] -- needs more inputs
  domselector_9_0_3 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 0.97-1.03, n=96)
      DEPENDS ON SAMPLING: counting each count_attribute_selector bin once gives 0.62x (95% CI 0.60-0.66, 3 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      ... and 4 count_attribute_selector bin(s) have too little data to enter that: [1.491,2.224), [2.224,3.317), [3.317,4.946), [7.376,11]
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 1.02x (95% CI 0.65-1.06, 3 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 4 count_attr_modifier bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3,3.5), [3.5,4]
      DEPENDS ON SAMPLING: counting each count_bare_attribute bin once gives 0.48x (95% CI 0.46-0.49, 2 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_p bin once gives 1.01x (95% CI 0.68-1.03, 4 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 2 count_p bin(s) have too little data to enter that: [1,2.567), [2.567,6.589)
      undecided on count_attribute_selector in [1,1.491) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_p in [6.589,16.91), [16.91,43.41), [111.4,286] -- needs more inputs
  domselector_9_0_4 and domselector_9_1_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
  domselector_9_0_4 and domselector_9_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=96)
  domselector_9_0_4 and domselector_9_1_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.01, n=96)
  domselector_9_0_4 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.01, n=96)
  domselector_9_0_4 and domselector_9_2_2 equivalent: ratio 1.01x within the equivalence band (95% CI 0.99-1.01, n=96)
      undecided on count_attr_modifier (confounded) in [2,2.5) -- needs more inputs
  domselector_9_1_0 and domselector_9_1_1 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=96)
  domselector_9_1_0 and domselector_9_1_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.97-0.99, n=96)
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
  domselector_9_1_0 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.00, n=96)
  domselector_9_1_0 and domselector_9_2_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.97-1.01, n=96)
      undecided on count_attribute_selector in [4.946,7.376) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [2,2.5) -- needs more inputs
      undecided on count_p in [43.41,111.4) -- needs more inputs
  domselector_9_1_1 and domselector_9_1_2 equivalent: ratio 0.98x within the equivalence band (95% CI 0.97-1.00, n=96)
  domselector_9_1_1 and domselector_9_2_1 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.01, n=96)
  domselector_9_1_1 and domselector_9_2_2 equivalent: ratio 0.98x within the equivalence band (95% CI 0.97-1.02, n=96)
  domselector_9_1_2 and domselector_9_2_1 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=96)
  domselector_9_1_2 and domselector_9_2_2 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=96)
  domselector_9_2_1 and domselector_9_2_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.01, n=96)
[compare] dominance across runtime_ns, fresh_ns:
  domselector_8_2_4 vs domselector_8_2_5 undecided on every metric
  domselector_8_2_4 vs domselector_9_0_3 undecided on every metric
  domselector_8_2_4 vs domselector_9_0_4 undecided on every metric
  domselector_8_2_4 vs domselector_9_1_0 undecided on every metric
  domselector_8_2_4 vs domselector_9_1_1 undecided on every metric
  domselector_8_2_4 vs domselector_9_1_2 undecided on every metric
  domselector_8_2_4 vs domselector_9_2_1 undecided on every metric
  domselector_8_2_4 vs domselector_9_2_2 undecided on every metric
  domselector_8_2_5 and domselector_9_0_3 EQUIVALENT on every metric
  domselector_8_2_5 vs domselector_9_0_4 undecided on every metric
  domselector_8_2_5 vs domselector_9_1_0 undecided on every metric
  domselector_8_2_5 vs domselector_9_1_1 undecided on every metric
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
      count_attribute_selector =0 (n=39): domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attribute_selector [1,1.491) (n=26): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attribute_selector [4.946,7.376) (n=11): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attr_modifier =0 (n=61): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attr_modifier [1,1.5) (n=18): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_attr_modifier [2,2.5) (n=10): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_bare_attribute =0 (n=68): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_bare_attribute =1 (n=28): domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_p [6.589,16.91) (n=19): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_p [16.91,43.41) (n=17): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_p [43.41,111.4) (n=21): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
      count_p [111.4,286] (n=34): domselector_8_2_4, domselector_8_2_5, domselector_9_0_3, domselector_9_0_4, domselector_9_1_0, domselector_9_1_1, domselector_9_1_2, domselector_9_2_1, domselector_9_2_2 not dominated
[interference] 3 property pair(s) tested over 864 rows; 3 show a dependence
  count_attribute_selector vs runtime_ns changes with count_p: rho by count_p stratum = [+0.51, +0.19, +0.70, +0.32], spread 0.51, p=0.003
  count_bare_attribute vs runtime_ns changes with count_p: rho by count_p stratum = [-0.04, +0.02, -0.16, -0.30], spread 0.32, p=0.003
  count_attr_modifier vs runtime_ns changes with count_p: rho by count_p stratum = [+0.47, +0.25, +0.50, +0.40], spread 0.26, p=0.030
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
