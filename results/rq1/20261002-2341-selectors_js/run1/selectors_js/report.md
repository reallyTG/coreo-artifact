# selectors_js

- corpus: 780 rows, 195 inputs, 4 systems
- elapsed: 3438s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 41 | 19 |
| count_more_complex_selector | 0 | 30 | 14 |
| count_comma | 0 | 30 | 19 |
| count_complex_selector | 1 | 114 | 29 |
| count_combinator | 0 | 73 | 29 |
| count_type_selector | 0 | 77 | 33 |
| count_subclass_selectors | 0 | 214 | 39 |
| count_wq_name | 0 | 66 | 22 |
| count_id_selector | 0 | 74 | 28 |
| count_pseudo_class_selector | 0 | 35 | 20 |
| count_class_selector | 0 | 62 | 25 |
| count_attribute_selector | 0 | 43 | 27 |
| count_name | 2 | 221 | 100 |
| count_pseudo_class_ident | 0 | 18 | 18 |
| count_pseudo_class_function | 0 | 18 | 16 |
| count_attr_modifier | 0 | 13 | 13 |
| count_attr_value | 0 | 34 | 22 |
| count_attr_matcher_ws | 0 | 34 | 22 |
| count_namechar | 9 | 2043 | 162 |
| count_lparen | 0 | 18 | 15 |
| count_relative_selector_list | 0 | 15 | 12 |
| count_lang_range | 0 | 4 | 5 |
| count_rparen | 0 | 18 | 15 |
| count_nth_function | 0 | 7 | 6 |
| count_attr_value_words | 0 | 69 | 64 |
| count_attr_ident | 0 | 14 | 13 |
| count_more_relative_selector | 0 | 11 | 8 |
| count_lang_tag | 0 | 67 | 64 |
| count_more_value_word | 0 | 41 | 39 |
| count_relative_combinator | 0 | 9 | 8 |
| count_complex_selector_in_has | 0 | 54 | 19 |
| count_digits | 0 | 3 | 4 |
| count_an_b_sign | 0 | 1 | 2 |
| count_signed_integer | 0 | 1 | 2 |
| count_an_a | 0 | 1 | 2 |
| count_sign | 0 | 2 | 3 |
| count_subclass_selectors_in_has | 0 | 82 | 20 |
| count_pseudo_class_selector_in_has | 0 | 18 | 12 |
| count_pseudo_class_function_in_has | 0 | 9 | 7 |
| count_complex_selector_list_in_has | 0 | 16 | 8 |
| count_more_complex_selector_in_has | 0 | 10 | 5 |
| count_node | 1 | 32 | 29 |
| count_section | 0 | 13 | 12 |
| count_flow_content | 0 | 26 | 22 |
| count_text_run | 0 | 86 | 55 |
| count_tchar | 0 | 2007 | 114 |
| count_flow_item | 0 | 143 | 44 |
| count_input | 0 | 36 | 27 |
| count_type_attr | 0 | 14 | 14 |
| count_a | 0 | 97 | 35 |
| count_attrs | 1 | 144 | 60 |
| count_class_attr | 0 | 33 | 34 |
| count_class_list | 0 | 71 | 59 |
| count_lang_attr | 0 | 32 | 33 |
| count_title_attr | 0 | 60 | 40 |
| count_id_attr | 0 | 55 | 34 |
| count_href_attr | 0 | 14 | 15 |
| count_phrasing_element | 0 | 51 | 26 |
| count_span | 0 | 22 | 15 |
| count_em | 0 | 18 | 14 |
| count_b | 0 | 16 | 12 |
| count_div | 0 | 27 | 24 |
| count_p | 0 | 11 | 12 |
| count_phrasing_content | 0 | 16 | 16 |
| count_phrasing_item | 0 | 104 | 42 |
| count_data_attr | 0 | 33 | 33 |
| count_more_node | 0 | 24 | 17 |
| doc_depth | 3 | 18 | 14 |
| doc_bytes | 64 | 3835 | 166 |
| selector_len | 1 | 2155 | 131 |
| selector_nesting | 0 | 6 | 7 |

## frontier
[selectors_js] grammar frontier (targeting stopped asking here):
  count_tchar: pinned at 2007 by the SEARCH; 1 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 195 inputs, 5 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_wq_name bins move with count_class_selector (1..49 across bins); count_attr_modifier (1..12 across bins); count_complex_selector_in_has (1..33.5 across bins) -- those regions are joint, not count_wq_name findings
[compare] count_class_selector bins move with count_wq_name (1..33.5 across bins); count_attr_modifier (1..9 across bins); count_complex_selector_in_has (2..10 across bins) -- those regions are joint, not count_class_selector findings
[compare] count_attr_modifier bins move with count_wq_name (1..52 across bins); count_class_selector (1..49 across bins); count_complex_selector_in_has (1.5..36.5 across bins) -- those regions are joint, not count_attr_modifier findings
[compare] count_complex_selector_in_has bins move with count_wq_name (1..29 across bins); count_class_selector (1..34 across bins); count_attr_modifier (2..7 across bins) -- those regions are joint, not count_complex_selector_in_has findings
  cssselect vs domselector undecided: cssselect ahead by 1.47x but the 95% CI (1.09-1.90, n=195) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_wq_name bin once gives 0.77x (95% CI 0.69-0.88, 7 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_attr_modifier bin once gives 0.72x (95% CI 0.69-0.86, 7 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      DEPENDS ON SAMPLING: counting each count_complex_selector_in_has bin once gives 0.61x (95% CI 0.53-0.73, 5 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_complex_selector_in_has bin(s) have too little data to enter that: [1,1.944), [3.78,7.348)
      crossover on count_wq_name (confounded): cssselect better below 2.01, domselector better above 8.124
      undecided on count_wq_name (confounded) in [2.01,4.041), [4.041,8.124) -- needs more inputs
      crossover on count_class_selector (confounded): cssselect better below 1.989, domselector better above 7.874
      undecided on count_class_selector (confounded) in [1.989,3.958), [3.958,7.874) -- needs more inputs
      crossover on count_attr_modifier (confounded): cssselect better below 1.533, domselector better above 2.351
      undecided on count_attr_modifier (confounded) in [1.533,2.351) -- needs more inputs
      crossover on count_complex_selector_in_has (confounded): cssselect better at 0, domselector better above 7.348
      undecided on count_complex_selector_in_has (confounded) in [1.944,3.78) -- needs more inputs
  cssselect vs nwsapi undecided: cssselect ahead by 1.16x but the 95% CI (0.94-1.33, n=126) spans the equivalence band
      undecided on count_wq_name (confounded) in [1,2.01), [2.01,4.041) -- needs more inputs
      undecided on count_class_selector (confounded) in =0, [1.989,3.958), [3.958,7.874) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.533), [1.533,2.351) -- needs more inputs
      undecided on count_complex_selector_in_has (confounded) in =0 -- needs more inputs
  cssselect vs nwsapi_prev undecided: cssselect ahead by 1.10x but the 95% CI (0.90-1.33, n=126) spans the equivalence band
      undecided on count_wq_name (confounded) in [1,2.01), [2.01,4.041) -- needs more inputs
      undecided on count_class_selector (confounded) in =0, [1.989,3.958), [3.958,7.874) -- needs more inputs
      undecided on count_attr_modifier (confounded) in =0, [1,1.533), [1.533,2.351) -- needs more inputs
      undecided on count_complex_selector_in_has (confounded) in =0 -- needs more inputs
  nwsapi better than domselector on runtime_ns: 2.05x (95% CI 1.89-2.25, n=126, p=4.6e-20)
  nwsapi_prev better than domselector on runtime_ns: 2.08x (95% CI 1.90-2.23, n=126, p=3.06e-20)
  nwsapi and nwsapi_prev equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.00, n=126)
[compare] rss: 195 inputs, 5 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_wq_name bins move with count_class_selector (1..49 across bins); count_attr_modifier (1..12 across bins); count_complex_selector_in_has (1..33.5 across bins) -- those regions are joint, not count_wq_name findings
[compare] count_class_selector bins move with count_wq_name (1..33.5 across bins); count_attr_modifier (1..9 across bins); count_complex_selector_in_has (2..10 across bins) -- those regions are joint, not count_class_selector findings
[compare] count_attr_modifier bins move with count_wq_name (1..52 across bins); count_class_selector (1..49 across bins); count_complex_selector_in_has (1.5..36.5 across bins) -- those regions are joint, not count_attr_modifier findings
[compare] count_complex_selector_in_has bins move with count_wq_name (1..29 across bins); count_class_selector (1..34 across bins); count_attr_modifier (2..7 across bins) -- those regions are joint, not count_complex_selector_in_has findings
  cssselect better than domselector on rss: 2.80x (95% CI 2.79-2.81, n=195, p=9.48e-34)
  cssselect better than nwsapi on rss: 2.81x (95% CI 2.81-2.81, n=126, p=2.03e-22)
  cssselect better than nwsapi_prev on rss: 2.81x (95% CI 2.81-2.81, n=126, p=2.03e-22)
  domselector and nwsapi equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=126)
  domselector and nwsapi_prev equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=126)
  nwsapi and nwsapi_prev equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=126)
[compare] dominance across runtime_ns, rss:
  cssselect ahead on rss 2.80x but runtime_ns undecided -- not a dominance claim until those are settled
  cssselect ahead on rss 2.81x but runtime_ns undecided -- not a dominance claim until those are settled
  cssselect ahead on rss 2.81x but runtime_ns undecided -- not a dominance claim until those are settled
  cssselect ahead on rss 2.81x but runtime_ns undecided -- not a dominance claim until those are settled
  nwsapi DOMINATES domselector: better on runtime_ns 2.05x; equivalent on rss
  nwsapi_prev DOMINATES domselector: better on runtime_ns 2.08x; equivalent on rss
  nwsapi and nwsapi_prev EQUIVALENT on every metric
[interference] 2 property pair(s) tested over 975 rows; 0 show a dependence
