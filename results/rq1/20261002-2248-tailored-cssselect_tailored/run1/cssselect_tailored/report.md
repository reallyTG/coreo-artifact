# cssselect_tailored

- corpus: 558 rows, 279 inputs, 2 systems
- elapsed: 2956s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_complex_selector_list | 1 | 22 | 18 |
| count_more_complex_selector | 0 | 14 | 14 |
| count_comma | 0 | 69 | 40 |
| count_complex_selector | 1 | 48 | 30 |
| count_combinator | 0 | 159 | 61 |
| count_has_compound | 1 | 22 | 18 |
| count_compound | 0 | 26 | 21 |
| count_type_selector | 0 | 192 | 74 |
| count_subclass_selectors | 0 | 68 | 31 |
| count_wq_name | 0 | 95 | 52 |
| count_lparen | 1 | 69 | 42 |
| count_relative_selector_list | 1 | 51 | 28 |
| count_rparen | 1 | 69 | 42 |
| count_pseudo_class_selector | 0 | 21 | 16 |
| count_class_selector | 0 | 77 | 47 |
| count_attribute_selector | 0 | 88 | 44 |
| count_id_selector | 0 | 96 | 49 |
| count_more_relative_selector | 0 | 26 | 18 |
| count_pseudo_class_ident | 0 | 43 | 33 |
| count_pseudo_class_function | 0 | 15 | 11 |
| count_name | 1 | 662 | 131 |
| count_attr_matcher_ws | 0 | 65 | 35 |
| count_attr_modifier | 0 | 31 | 24 |
| count_attr_value | 0 | 65 | 35 |
| count_relative_combinator | 0 | 28 | 17 |
| count_complex_selector_in_has | 1 | 259 | 82 |
| count_nth_function | 0 | 13 | 13 |
| count_namechar | 8 | 13153 | 227 |
| count_attr_ident | 0 | 48 | 29 |
| count_attr_value_words | 0 | 188 | 70 |
| count_more_value_word | 0 | 95 | 43 |
| count_subclass_selectors_in_has | 0 | 324 | 90 |
| count_signed_integer | 0 | 4 | 5 |
| count_digits | 0 | 22 | 14 |
| count_an_b_sign | 0 | 4 | 5 |
| count_an_a | 0 | 8 | 9 |
| count_sign | 0 | 6 | 7 |
| count_pseudo_class_selector_in_has | 0 | 95 | 48 |
| count_pseudo_class_function_in_has | 0 | 56 | 35 |
| count_complex_selector_list_in_has | 0 | 97 | 40 |
| count_more_complex_selector_in_has | 0 | 54 | 25 |
| count_node | 1 | 21 | 19 |
| count_section | 0 | 21 | 20 |
| count_flow_content | 0 | 21 | 17 |
| count_text_run | 0 | 123 | 58 |
| count_tchar | 0 | 4194 | 135 |
| count_flow_item | 0 | 143 | 29 |
| count_input | 0 | 45 | 28 |
| count_type_attr | 0 | 21 | 18 |
| count_a | 0 | 112 | 34 |
| count_href_attr | 0 | 29 | 16 |
| count_attrs | 1 | 162 | 73 |
| count_class_attr | 0 | 70 | 35 |
| count_class_list | 0 | 153 | 65 |
| count_title_attr | 0 | 77 | 45 |
| count_lang_attr | 0 | 70 | 34 |
| count_id_attr | 0 | 95 | 39 |
| count_phrasing_element | 0 | 38 | 26 |
| count_b | 0 | 14 | 13 |
| count_em | 0 | 13 | 14 |
| count_span | 0 | 15 | 12 |
| count_p | 0 | 16 | 16 |
| count_phrasing_content | 0 | 22 | 17 |
| count_div | 0 | 24 | 17 |
| count_phrasing_item | 0 | 100 | 50 |
| count_leaf_items | 0 | 25 | 15 |
| count_leaf_item | 0 | 65 | 36 |
| count_lang_tag | 0 | 140 | 62 |
| count_data_attr | 0 | 85 | 34 |
| count_more_node | 0 | 12 | 11 |
| doc_depth | 3 | 23 | 20 |
| doc_bytes | 69 | 15091 | 193 |
| selector_len | 9 | 15402 | 206 |
| selector_nesting | 1 | 11 | 9 |

## frontier
[cssselect_tailored] grammar frontier (targeting stopped asking here):
  count_an_a: pinned at 8 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 279 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_comma bins move with count_pseudo_class_selector (1..7 across bins); count_an_a (1..5 across bins); doc_bytes (90..3090 across bins) -- those regions are joint, not count_comma findings
[compare] count_pseudo_class_selector bins move with count_comma (2..50 across bins); count_an_a (1..5 across bins); doc_bytes (76..2962 across bins) -- those regions are joint, not count_pseudo_class_selector findings
[compare] count_an_a bins move with count_comma (2..67 across bins); doc_bytes (76..2929 across bins) -- those regions are joint, not count_an_a findings
[compare] doc_bytes bins move with count_comma (2..31 across bins); count_pseudo_class_selector (0.5..7 across bins); count_an_a (1..4.5 across bins) -- those regions are joint, not doc_bytes findings
  css_select_5_1_0 better than css_select_5_2_0 on runtime_ns: 1.18x (95% CI 1.15-1.21, n=279, p=5.6e-33)
      undecided on count_comma (confounded) in =0, [1,2.025), [2.025,4.102), [4.102,8.307), [8.307,16.82) -- needs more inputs
      undecided on count_pseudo_class_selector (confounded) in =0, [1,1.661), [1.661,2.759) -- needs more inputs
      undecided on count_an_a (confounded) in =0 -- needs more inputs
      undecided on doc_bytes (confounded) in [415.7,1020), [1020,2505), [2505,6148), [6148,1.509e+04] -- needs more inputs
[compare] rss: 279 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_comma bins move with count_pseudo_class_selector (1..7 across bins); count_an_a (1..5 across bins); doc_bytes (90..3090 across bins) -- those regions are joint, not count_comma findings
[compare] count_pseudo_class_selector bins move with count_comma (2..50 across bins); count_an_a (1..5 across bins); doc_bytes (76..2962 across bins) -- those regions are joint, not count_pseudo_class_selector findings
[compare] count_an_a bins move with count_comma (2..67 across bins); doc_bytes (76..2929 across bins) -- those regions are joint, not count_an_a findings
[compare] doc_bytes bins move with count_comma (2..31 across bins); count_pseudo_class_selector (0.5..7 across bins); count_an_a (1..4.5 across bins) -- those regions are joint, not doc_bytes findings
  css_select_5_1_0 and css_select_5_2_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=279)
[compare] dominance across runtime_ns, rss:
  css_select_5_1_0 DOMINATES css_select_5_2_0: better on runtime_ns 1.18x; equivalent on rss
      count_comma =0 (n=48): css_select_5_1_0, css_select_5_2_0 not dominated
      count_comma [1,2.025) (n=42): css_select_5_1_0, css_select_5_2_0 not dominated
      count_comma [2.025,4.102) (n=29): css_select_5_1_0, css_select_5_2_0 not dominated
      count_comma [4.102,8.307) (n=24): css_select_5_1_0, css_select_5_2_0 not dominated
      count_comma [8.307,16.82) (n=31): css_select_5_1_0, css_select_5_2_0 not dominated
      count_comma [16.82,34.07) (n=72): css_select_5_1_0 not dominated
      count_comma [34.07,69] (n=33): css_select_5_1_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in =0, [1,2.025), [2.025,4.102), [4.102,8.307), [8.307,16.82) on count_comma -- the global verdict is a statement about this corpus's mix, not about the systems
      count_pseudo_class_selector =0 (n=108): css_select_5_1_0, css_select_5_2_0 not dominated
      count_pseudo_class_selector [1,1.661) (n=26): css_select_5_1_0, css_select_5_2_0 not dominated
      count_pseudo_class_selector [1.661,2.759) (n=19): css_select_5_1_0, css_select_5_2_0 not dominated
      count_pseudo_class_selector [2.759,4.583) (n=31): css_select_5_1_0 not dominated
      count_pseudo_class_selector [4.583,7.612) (n=66): css_select_5_1_0 not dominated
      count_pseudo_class_selector [7.612,12.64) (n=18): css_select_5_1_0 not dominated
      count_pseudo_class_selector [12.64,21] (n=11): css_select_5_1_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in =0, [1,1.661), [1.661,2.759) on count_pseudo_class_selector -- the global verdict is a statement about this corpus's mix, not about the systems
      count_an_a =0 (n=140): css_select_5_1_0, css_select_5_2_0 not dominated
      count_an_a [1,2.167) (n=62): css_select_5_1_0 not dominated
      count_an_a [2.167,3.333) (n=20): css_select_5_1_0 not dominated
      count_an_a [3.333,4.5) (n=10): css_select_5_1_0 not dominated
      count_an_a [4.5,5.667) (n=25): css_select_5_1_0 not dominated
      count_an_a [5.667,6.833) (n=12): css_select_5_1_0 not dominated
      count_an_a [6.833,8] (n=10): css_select_5_1_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in =0 on count_an_a -- the global verdict is a statement about this corpus's mix, not about the systems
      doc_bytes [69,169.4) (n=86): css_select_5_1_0 not dominated
      doc_bytes [169.4,415.7) (n=8): css_select_5_1_0 not dominated
      doc_bytes [415.7,1020) (n=22): css_select_5_1_0, css_select_5_2_0 not dominated
      doc_bytes [1020,2505) (n=40): css_select_5_1_0, css_select_5_2_0 not dominated
      doc_bytes [2505,6148) (n=110): css_select_5_1_0, css_select_5_2_0 not dominated
      doc_bytes [6148,1.509e+04] (n=13): css_select_5_1_0, css_select_5_2_0 not dominated
      WARNING css_select_5_2_0 is dominated by css_select_5_1_0 over the whole corpus but survives in [415.7,1020), [1020,2505), [2505,6148), [6148,1.509e+04] on doc_bytes -- the global verdict is a statement about this corpus's mix, not about the systems
[interference] 6 property pair(s) tested over 558 rows; 5 show a dependence
  doc_bytes vs runtime_ns changes with count_comma: rho by count_comma stratum = [+0.63, +0.34, -0.41, -0.15], spread 1.04, p=0.003
  count_an_a vs runtime_ns changes with count_comma: rho by count_comma stratum = [+0.08, -0.17, +0.33, +0.18], spread 0.50, p=0.003
  count_an_a vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [+0.37, +0.82, +0.55, +0.42], spread 0.45, p=0.003
  count_pseudo_class_selector vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [+0.58, +0.79, +0.38, +0.44], spread 0.41, p=0.003
  count_comma vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [+0.78, +0.95, +0.75, +0.69], spread 0.26, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
