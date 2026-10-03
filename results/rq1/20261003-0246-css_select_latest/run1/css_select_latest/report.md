# css_select_latest

- corpus: 1300 rows, 260 inputs, 5 systems
- elapsed: 3053s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 40 | 19 |
| count_more_complex_selector | 0 | 25 | 14 |
| count_comma | 0 | 44 | 18 |
| count_complex_selector | 1 | 77 | 30 |
| count_combinator | 0 | 75 | 34 |
| count_type_selector | 0 | 91 | 37 |
| count_subclass_selectors | 0 | 120 | 40 |
| count_wq_name | 0 | 46 | 25 |
| count_class_selector | 0 | 57 | 26 |
| count_pseudo_class_selector | 0 | 34 | 21 |
| count_attribute_selector | 0 | 53 | 25 |
| count_id_selector | 0 | 52 | 27 |
| count_name | 2 | 221 | 108 |
| count_pseudo_class_ident | 0 | 27 | 21 |
| count_pseudo_class_function | 0 | 16 | 14 |
| count_attr_modifier | 0 | 15 | 11 |
| count_attr_matcher_ws | 0 | 33 | 20 |
| count_attr_value | 0 | 33 | 20 |
| count_namechar | 12 | 13223 | 202 |
| count_relative_selector_list | 0 | 15 | 11 |
| count_nth_function | 0 | 7 | 5 |
| count_lparen | 0 | 36 | 19 |
| count_lang_range | 0 | 9 | 7 |
| count_rparen | 0 | 36 | 19 |
| count_attr_value_words | 0 | 72 | 62 |
| count_attr_ident | 0 | 20 | 16 |
| count_more_relative_selector | 0 | 11 | 7 |
| count_lang_tag | 0 | 71 | 60 |
| count_more_value_word | 0 | 45 | 37 |
| count_relative_combinator | 0 | 8 | 8 |
| count_complex_selector_in_has | 0 | 125 | 21 |
| count_signed_integer | 0 | 2 | 3 |
| count_digits | 0 | 13 | 6 |
| count_an_a | 0 | 3 | 4 |
| count_an_b_sign | 0 | 3 | 3 |
| count_sign | 0 | 4 | 4 |
| count_subclass_selectors_in_has | 0 | 195 | 23 |
| count_pseudo_class_selector_in_has | 0 | 58 | 13 |
| count_pseudo_class_function_in_has | 0 | 34 | 9 |
| count_complex_selector_list_in_has | 0 | 58 | 10 |
| count_more_complex_selector_in_has | 0 | 37 | 6 |
| count_node | 1 | 27 | 24 |
| count_div | 0 | 27 | 25 |
| count_attrs | 1 | 144 | 63 |
| count_data_attr | 0 | 33 | 34 |
| count_lang_attr | 0 | 35 | 33 |
| count_title_attr | 0 | 60 | 41 |
| count_id_attr | 0 | 55 | 35 |
| count_class_attr | 0 | 33 | 34 |
| count_class_list | 0 | 66 | 57 |
| count_flow_content | 0 | 26 | 21 |
| count_text_run | 0 | 86 | 58 |
| count_tchar | 0 | 5656 | 128 |
| count_flow_item | 0 | 143 | 44 |
| count_a | 0 | 97 | 34 |
| count_href_attr | 0 | 14 | 15 |
| count_phrasing_element | 0 | 51 | 24 |
| count_b | 0 | 16 | 11 |
| count_em | 0 | 18 | 13 |
| count_span | 0 | 22 | 15 |
| count_p | 0 | 11 | 10 |
| count_phrasing_content | 0 | 16 | 15 |
| count_section | 0 | 8 | 9 |
| count_input | 0 | 36 | 27 |
| count_phrasing_item | 0 | 104 | 42 |
| count_type_attr | 0 | 14 | 14 |
| count_more_node | 0 | 16 | 14 |
| doc_depth | 3 | 18 | 15 |
| doc_bytes | 68 | 16086 | 203 |
| selector_len | 1 | 13473 | 152 |
| selector_nesting | 0 | 10 | 10 |

## frontier
[css_select_latest] grammar frontier (targeting stopped asking here):
  count_type_selector: pinned at 91 by the SEARCH; 2 escalating request(s) returned nothing further.
  count_attr_ident: pinned at 20 by the SEARCH; 2 escalating request(s) returned nothing further.
  count_complex_selector_in_has: pinned at 125 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 260 inputs, 5 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_type_selector bins move with count_attr_modifier (1..8 across bins); count_attr_ident (1..10 across bins); count_complex_selector_in_has (3..55 across bins) -- those regions are joint, not count_type_selector findings
[compare] count_attr_modifier bins move with count_type_selector (2..91 across bins); count_attr_ident (2..18 across bins); count_complex_selector_in_has (2..125 across bins) -- those regions are joint, not count_attr_modifier findings
[compare] count_attr_ident bins move with count_type_selector (2..91 across bins); count_attr_modifier (1..15 across bins); count_complex_selector_in_has (1..125 across bins) -- those regions are joint, not count_attr_ident findings
[compare] count_complex_selector_in_has bins move with count_type_selector (2..91 across bins); count_attr_modifier (2..15 across bins); count_attr_ident (1..18 across bins) -- those regions are joint, not count_complex_selector_in_has findings
  css_select_5_1_0 better than css_select_5_2_0 on runtime_ns: 1.13x (95% CI 1.12-1.14, n=154, p=2.22e-24)
      undecided on count_type_selector (confounded) in =0, [1,2.121), [2.121,4.498) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.57) -- needs more inputs
      undecided on count_attr_ident (confounded) in [1.648,2.714), [2.714,4.472) -- needs more inputs
  css_select_5_1_0 and css_select_5_2_2 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.01, n=154)
  css_select_5_1_0 better than css_select_6_0_0 on runtime_ns: 1.25x (95% CI 1.23-1.27, n=154, p=1.09e-25)
  css_select_5_1_0 and css_select_7_0_0 equivalent: ratio 0.95x within the equivalence band (95% CI 0.93-0.97, n=154)
      undecided on count_type_selector (confounded) in [1,2.121), [9.539,20.23) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [1,1.57), [6.082,9.552) -- needs more inputs
      undecided on count_attr_ident (confounded) in [1.648,2.714), [2.714,4.472) -- needs more inputs
  css_select_5_2_2 better than css_select_5_2_0 on runtime_ns: 1.13x (95% CI 1.12-1.15, n=154, p=6.01e-25)
      undecided on count_type_selector (confounded) in =0, [1,2.121), [2.121,4.498) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.57) -- needs more inputs
      undecided on count_attr_ident (confounded) in [1.648,2.714), [2.714,4.472) -- needs more inputs
  css_select_5_2_0 vs css_select_6_0_0 undecided: css_select_5_2_0 ahead by 1.10x but the 95% CI (1.10-1.11, n=197) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_complex_selector_in_has bin once gives 1.11x (95% CI 1.10-1.12, 3 bins, equal weight per bin), verdict 'a_faster' not 'undecided'
      ... and 4 count_complex_selector_in_has bin(s) have too little data to enter that: [5,11.18), [11.18,25), [25,55.9), [55.9,125]
      undecided on count_type_selector (confounded) in =0, [1,2.121), [2.121,4.498), [4.498,9.539), [9.539,20.23) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.57), [3.873,6.082) -- needs more inputs
      undecided on count_attr_ident (confounded) in =0, [1,1.648), [1.648,2.714), [2.714,4.472) -- needs more inputs
      undecided on count_complex_selector_in_has (confounded) in =0, [1,2.236) -- needs more inputs
  css_select_7_0_0 better than css_select_5_2_0 on runtime_ns: 1.20x (95% CI 1.18-1.21, n=197, p=3.21e-33)
      undecided on count_type_selector (confounded) in =0 -- needs more inputs
      undecided on count_attr_ident (confounded) in [1.648,2.714), [2.714,4.472) -- needs more inputs
  css_select_5_2_2 better than css_select_6_0_0 on runtime_ns: 1.25x (95% CI 1.23-1.27, n=154, p=1.16e-25)
  css_select_5_2_2 and css_select_7_0_0 equivalent: ratio 0.96x within the equivalence band (95% CI 0.94-0.97, n=154)
      undecided on count_type_selector (confounded) in [1,2.121) -- needs more inputs
      undecided on count_attr_modifier (confounded) in [6.082,9.552) -- needs more inputs
      undecided on count_attr_ident (confounded) in [2.714,4.472) -- needs more inputs
  css_select_7_0_0 better than css_select_6_0_0 on runtime_ns: 1.32x (95% CI 1.30-1.34, n=197, p=4.46e-34)
[compare] rss: 260 inputs, 5 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_type_selector bins move with count_attr_modifier (1..8 across bins); count_attr_ident (1..10 across bins); count_complex_selector_in_has (3..55 across bins) -- those regions are joint, not count_type_selector findings
[compare] count_attr_modifier bins move with count_type_selector (2..91 across bins); count_attr_ident (2..18 across bins); count_complex_selector_in_has (2..125 across bins) -- those regions are joint, not count_attr_modifier findings
[compare] count_attr_ident bins move with count_type_selector (2..91 across bins); count_attr_modifier (1..15 across bins); count_complex_selector_in_has (1..125 across bins) -- those regions are joint, not count_attr_ident findings
[compare] count_complex_selector_in_has bins move with count_type_selector (2..91 across bins); count_attr_modifier (2..15 across bins); count_attr_ident (1..18 across bins) -- those regions are joint, not count_complex_selector_in_has findings
  css_select_5_1_0 and css_select_5_2_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=154)
  css_select_5_1_0 and css_select_5_2_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=154)
  css_select_5_1_0 and css_select_6_0_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=154)
  css_select_5_1_0 and css_select_7_0_0 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.02, n=154)
  css_select_5_2_0 and css_select_5_2_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=154)
  css_select_5_2_0 and css_select_6_0_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=197)
  css_select_5_2_0 and css_select_7_0_0 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.02, n=197)
  css_select_5_2_2 and css_select_6_0_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=154)
  css_select_5_2_2 and css_select_7_0_0 equivalent: ratio 1.02x within the equivalence band (95% CI 1.01-1.02, n=154)
  css_select_6_0_0 and css_select_7_0_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=197)
[compare] dominance across runtime_ns, rss:
  css_select_5_1_0 DOMINATES css_select_5_2_0: better on runtime_ns 1.13x; equivalent on rss
  css_select_5_1_0 and css_select_5_2_2 EQUIVALENT on every metric
  css_select_5_1_0 DOMINATES css_select_6_0_0: better on runtime_ns 1.25x; equivalent on rss
  css_select_5_1_0 and css_select_7_0_0 EQUIVALENT on every metric
  css_select_5_2_2 DOMINATES css_select_5_2_0: better on runtime_ns 1.13x; equivalent on rss
  css_select_5_2_0 vs css_select_6_0_0 undecided on every metric
  css_select_7_0_0 DOMINATES css_select_5_2_0: better on runtime_ns 1.20x; equivalent on rss
  css_select_5_2_2 DOMINATES css_select_6_0_0: better on runtime_ns 1.25x; equivalent on rss
  css_select_5_2_2 and css_select_7_0_0 EQUIVALENT on every metric
  css_select_7_0_0 DOMINATES css_select_6_0_0: better on runtime_ns 1.32x; equivalent on rss
      count_type_selector =0 (n=20): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_type_selector [1,2.121) (n=68): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_type_selector [2.121,4.498) (n=41): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_type_selector [4.498,9.539) (n=38): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_type_selector [9.539,20.23) (n=27): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_type_selector [20.23,42.91) (n=39): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_type_selector [42.91,91] (n=27): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_7_0_0 over the whole corpus but survives in =0, [42.91,91] on count_type_selector -- the global verdict is a statement about this corpus's mix, not about the systems
      WARNING css_select_6_0_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [42.91,91] on count_type_selector -- the global verdict is a statement about this corpus's mix, not about the systems
      count_attr_modifier =0 (n=120): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_modifier [1,1.57) (n=31): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_modifier [1.57,2.466) (n=52): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_modifier [3.873,6.082) (n=22): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_modifier [6.082,9.552) (n=18): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_modifier [9.552,15] (n=10): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [9.552,15] on count_attr_modifier -- the global verdict is a statement about this corpus's mix, not about the systems
      WARNING css_select_6_0_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [9.552,15] on count_attr_modifier -- the global verdict is a statement about this corpus's mix, not about the systems
      count_attr_ident =0 (n=134): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_ident [1,1.648) (n=22): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_ident [1.648,2.714) (n=21): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_ident [2.714,4.472) (n=15): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_ident [4.472,7.368) (n=37): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_attr_ident [7.368,12.14) (n=19): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      count_attr_ident [12.14,20] (n=12): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [1.648,2.714), [2.714,4.472), [7.368,12.14), [12.14,20] on count_attr_ident -- the global verdict is a statement about this corpus's mix, not about the systems
      WARNING css_select_6_0_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [7.368,12.14), [12.14,20] on count_attr_ident -- the global verdict is a statement about this corpus's mix, not about the systems
      count_complex_selector_in_has =0 (n=165): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_complex_selector_in_has [1,2.236) (n=37): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_complex_selector_in_has [2.236,5) (n=19): css_select_5_1_0, css_select_5_2_2, css_select_7_0_0 not dominated
      count_complex_selector_in_has [11.18,25) (n=11): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      count_complex_selector_in_has [25,55.9) (n=12): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      count_complex_selector_in_has [55.9,125] (n=10): css_select_5_1_0, css_select_5_2_0, css_select_5_2_2, css_select_6_0_0, css_select_7_0_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [11.18,25), [25,55.9), [55.9,125] on count_complex_selector_in_has -- the global verdict is a statement about this corpus's mix, not about the systems
      WARNING css_select_6_0_0 is dominated by css_select_7_0_0 over the whole corpus but survives in [11.18,25), [25,55.9), [55.9,125] on count_complex_selector_in_has -- the global verdict is a statement about this corpus's mix, not about the systems
[interference] 3 property pair(s) tested over 1300 rows; 3 show a dependence
  count_attr_ident vs runtime_ns changes with count_type_selector: rho by count_type_selector stratum = [-0.23, +0.24, -0.10, +0.71], spread 0.94, p=0.003
  count_attr_modifier vs runtime_ns changes with count_type_selector: rho by count_type_selector stratum = [-0.08, +0.23, +0.35, +0.05], spread 0.43, p=0.003
  count_complex_selector_in_has vs runtime_ns changes with count_type_selector: rho by count_type_selector stratum = [+0.06, +0.44, +0.26, +0.14], spread 0.38, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
