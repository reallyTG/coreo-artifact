# jsonpath_ng_latest

- corpus: 3564 rows, 594 inputs, 6 systems
- elapsed: 3463s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_s_segment | 0 | 185 | 103 |
| count_child_segment | 0 | 91 | 68 |
| count_member_name_shorthand | 0 | 75 | 60 |
| count_name_first | 0 | 2865 | 212 |
| count_name_char | 0 | 2865 | 193 |
| count_bracketed_selection | 0 | 31 | 31 |
| count_selector | 0 | 210 | 67 |
| count_slice_selector | 0 | 18 | 18 |
| count_B | 0 | 2096 | 382 |
| count_int | 0 | 103 | 71 |
| count_pos_int | 0 | 77 | 52 |
| count_DIGIT | 0 | 251 | 138 |
| count_DIGIT1 | 0 | 195 | 112 |
| count_name_selector | 0 | 54 | 43 |
| count_name_dq_chars | 0 | 40 | 31 |
| count_name_dq_mixed | 0 | 40 | 19 |
| count_name_dq_special | 0 | 2617 | 32 |
| count_escapable | 0 | 1159 | 52 |
| count_hexchar | 0 | 256 | 35 |
| count_high_surrogate | 0 | 120 | 26 |
| count_D | 0 | 318 | 38 |
| count_HEXDIG | 0 | 810 | 51 |
| count_low_surrogate | 0 | 120 | 26 |
| count_non_surrogate | 0 | 136 | 25 |
| count_oct_digit | 0 | 78 | 20 |
| count_non_d_hex | 0 | 58 | 21 |
| count_name_dq_char | 0 | 5220 | 39 |
| count_name_sq_chars | 0 | 50 | 28 |
| count_name_sq_mixed | 0 | 50 | 13 |
| count_name_sq_special | 0 | 1436 | 34 |
| count_name_sq_char | 0 | 2771 | 39 |
| count_filter_selector | 0 | 32 | 21 |
| count_logical_expr | 0 | 38 | 35 |
| count_logical_and_expr | 0 | 238 | 58 |
| count_basic_expr | 0 | 268 | 93 |
| count_test_expr | 0 | 235 | 61 |
| count_logical_function_expr | 0 | 40 | 24 |
| count_search_expr | 0 | 10 | 10 |
| count_S | 0 | 194 | 99 |
| count_value_argument | 0 | 44 | 29 |
| count_singular_query | 0 | 50 | 31 |
| count_abs_singular_query | 0 | 14 | 15 |
| count_s_singular_segment | 0 | 194 | 71 |
| count_index_segment | 0 | 103 | 47 |
| count_index_selector | 0 | 103 | 56 |
| count_name_segment | 0 | 96 | 48 |
| count_rel_singular_query | 0 | 50 | 22 |
| count_value_function_expr | 0 | 22 | 22 |
| count_count_expr | 0 | 10 | 11 |
| count_filter_query | 0 | 238 | 60 |
| count_rel_query | 0 | 114 | 44 |
| count_wildcard_selector | 0 | 126 | 74 |
| count_more_selector | 0 | 195 | 47 |
| count_descendant_segment | 0 | 94 | 67 |
| count_abs_query | 0 | 124 | 43 |
| count_length_expr | 0 | 10 | 11 |
| count_value_expr | 0 | 9 | 10 |
| count_literal | 0 | 96 | 47 |
| count_number | 0 | 10 | 11 |
| count_frac | 0 | 14 | 12 |
| count_exp | 0 | 6 | 7 |
| count_string_literal | 0 | 96 | 22 |
| count_sq_chars | 0 | 96 | 12 |
| count_letter | 0 | 3693 | 91 |
| count_sq_mixed | 0 | 96 | 11 |
| count_dq_chars | 0 | 96 | 17 |
| count_dq_mixed | 0 | 96 | 14 |
| count_sign_opt | 0 | 9 | 9 |
| count_sq_special | 0 | 3214 | 20 |
| count_sq_char | 0 | 6345 | 24 |
| count_dq_special | 0 | 3357 | 25 |
| count_dq_char | 0 | 6721 | 25 |
| count_regex_argument | 0 | 40 | 24 |
| count_iregexp_literal | 0 | 40 | 22 |
| count_ire_regexp | 0 | 81 | 56 |
| count_ire_branch | 0 | 527 | 94 |
| count_ire_piece | 0 | 793 | 107 |
| count_ire_quantifier | 0 | 380 | 90 |
| count_ire_range_quantifier | 0 | 103 | 57 |
| count_ire_char_class | 0 | 206 | 64 |
| count_ire_char_class_expr | 0 | 206 | 44 |
| count_ire_cce1 | 0 | 1406 | 91 |
| count_ire_alt | 0 | 491 | 76 |
| count_match_expr | 0 | 40 | 22 |
| count_and_tail | 0 | 249 | 48 |
| count_or_tail | 0 | 221 | 30 |
| count_paren_expr | 0 | 24 | 24 |
| count_comparison_expr | 0 | 48 | 37 |
| count_logical_not_op | 0 | 55 | 39 |
| count_comparable | 0 | 96 | 37 |
| count_ire_normal_char | 0 | 489 | 60 |
| count_ws | 4 | 367 | 88 |
| count_nonempty_array | 0 | 16 | 12 |
| count_value | 1 | 131 | 45 |
| count_object | 0 | 17 | 17 |
| count_nonempty_object | 0 | 11 | 12 |
| count_member | 0 | 55 | 32 |
| count_doc_name_mixed | 0 | 50 | 18 |
| count_doc_name_special | 0 | 2421 | 37 |
| count_doc_escape | 0 | 2428 | 41 |
| count_doc_name_char | 0 | 4734 | 44 |
| count_doc_number | 0 | 18 | 16 |
| count_doc_exp | 0 | 9 | 9 |
| count_doc_string | 0 | 16 | 16 |
| count_array | 0 | 24 | 16 |
| count_more_member | 0 | 45 | 29 |
| count_doc_mixed | 0 | 11 | 8 |
| count_doc_special | 0 | 44 | 18 |
| count_doc_char | 0 | 76 | 21 |
| count_more_value | 0 | 78 | 30 |
| doc_depth | 1 | 13 | 11 |
| doc_bytes | 3 | 8004 | 171 |
| query_len | 1 | 10647 | 330 |

## frontier
[jsonpath_ng_latest] grammar frontier (targeting stopped asking here):
  count_s_segment: pinned at 185 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_descendant_segment: pinned at 94 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_nonempty_array: pinned at 16 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_value: pinned at 131 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_doc_name_mixed: pinned at 50 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_doc_escape: pinned at 2428 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_more_value: pinned at 78 by the SEARCH; 1 escalating request(s) returned nothing further.
  query_len: pinned at 10647 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 233 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_descendant_segment bins move with count_ws (4..59 across bins); query_len (32..1639 across bins) -- those regions are joint, not count_descendant_segment findings
[compare] count_ws bins move with count_descendant_segment (1..6 across bins); count_more_value (4..27 across bins); query_len (27..1771 across bins) -- those regions are joint, not count_ws findings
[compare] count_more_value bins move with count_descendant_segment (0.5..5 across bins); count_ws (4..220 across bins); query_len (29..1741 across bins) -- those regions are joint, not count_more_value findings
[compare] query_len bins move with count_descendant_segment (1..12 across bins); count_ws (4..54.5 across bins); count_more_value (1..4 across bins) -- those regions are joint, not query_len findings
  jsonpath_ng_1_5_2 and jsonpath_ng_1_5_3 equivalent: ratio 1.04x within the equivalence band (95% CI 1.04-1.05, n=208)
      undecided on count_more_value (confounded) in [1,2.067) -- needs more inputs
      undecided on query_len (confounded) in [103.2,484), [484,2270) -- needs more inputs
  jsonpath_ng_1_5_2 and jsonpath_ng_1_6_0 equivalent: ratio 1.05x within the equivalence band (95% CI 1.04-1.05, n=208)
      undecided on count_more_value (confounded) in [1,2.067) -- needs more inputs
      undecided on query_len (confounded) in [103.2,484), [484,2270) -- needs more inputs
  jsonpath_ng_1_5_2 and jsonpath_ng_1_6_1 equivalent: ratio 1.05x within the equivalence band (95% CI 1.04-1.05, n=208)
      undecided on count_more_value (confounded) in [1,2.067) -- needs more inputs
      undecided on query_len (confounded) in [103.2,484), [484,2270) -- needs more inputs
  jsonpath_ng_1_5_2 and jsonpath_ng_1_7_0 equivalent: ratio 1.04x within the equivalence band (95% CI 1.04-1.05, n=208)
      undecided on count_more_value (confounded) in [1,2.067) -- needs more inputs
      undecided on query_len (confounded) in [103.2,484), [484,2270) -- needs more inputs
  jsonpath_ng_1_5_2 and jsonpath_ng_1_8_0 equivalent: ratio 1.08x within the equivalence band (95% CI 1.07-1.09, n=208)
      DEPENDS ON SAMPLING: counting each count_more_value bin once gives 1.09x (95% CI 1.08-1.10, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      ... and 1 count_more_value bin(s) have too little data to enter that: [37.74,78]
      undecided on count_descendant_segment (confounded) in [2.132,4.547), [4.547,9.695) -- needs more inputs
      undecided on count_ws (confounded) in [38.31,81.37), [81.37,172.8), [172.8,367] -- needs more inputs
      undecided on count_more_value (confounded) in [1,2.067), [2.067,4.273), [8.832,18.26) -- needs more inputs
      undecided on query_len (confounded) in [4.69,22), [22,103.2), [103.2,484), [484,2270) -- needs more inputs
  jsonpath_ng_1_5_3 and jsonpath_ng_1_6_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.01, n=208)
  jsonpath_ng_1_5_3 and jsonpath_ng_1_6_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.01, n=208)
  jsonpath_ng_1_5_3 and jsonpath_ng_1_7_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=208)
  jsonpath_ng_1_5_3 and jsonpath_ng_1_8_0 equivalent: ratio 1.04x within the equivalence band (95% CI 1.03-1.04, n=208)
  jsonpath_ng_1_6_0 and jsonpath_ng_1_6_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=208)
  jsonpath_ng_1_6_0 and jsonpath_ng_1_7_0 equivalent: ratio 1.00x within the equivalence band (95% CI 0.99-1.00, n=208)
  jsonpath_ng_1_6_0 and jsonpath_ng_1_8_0 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.04, n=208)
  jsonpath_ng_1_6_1 and jsonpath_ng_1_7_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=219)
  jsonpath_ng_1_6_1 and jsonpath_ng_1_8_0 equivalent: ratio 1.03x within the equivalence band (95% CI 1.02-1.04, n=219)
  jsonpath_ng_1_7_0 and jsonpath_ng_1_8_0 equivalent: ratio 1.04x within the equivalence band (95% CI 1.03-1.04, n=219)
