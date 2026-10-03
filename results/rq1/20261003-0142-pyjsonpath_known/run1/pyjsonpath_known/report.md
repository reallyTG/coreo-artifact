# pyjsonpath_known

- corpus: 1144 rows, 572 inputs, 2 systems
- elapsed: 3424s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_s_segment | 0 | 166 | 95 |
| count_B | 4 | 2096 | 377 |
| count_descendant_segment | 0 | 91 | 62 |
| count_wildcard_selector | 0 | 126 | 69 |
| count_bracketed_selection | 0 | 33 | 30 |
| count_selector | 0 | 210 | 63 |
| count_index_selector | 0 | 103 | 54 |
| count_int | 0 | 103 | 71 |
| count_pos_int | 0 | 77 | 54 |
| count_DIGIT1 | 0 | 195 | 119 |
| count_DIGIT | 0 | 251 | 138 |
| count_name_selector | 0 | 54 | 43 |
| count_name_dq_chars | 0 | 40 | 31 |
| count_name_char | 0 | 2865 | 192 |
| count_name_first | 0 | 2865 | 206 |
| count_name_dq_mixed | 0 | 40 | 19 |
| count_name_dq_special | 0 | 2617 | 29 |
| count_escapable | 0 | 1159 | 52 |
| count_hexchar | 0 | 256 | 35 |
| count_high_surrogate | 0 | 120 | 26 |
| count_D | 0 | 318 | 38 |
| count_HEXDIG | 0 | 810 | 52 |
| count_non_surrogate | 0 | 136 | 25 |
| count_oct_digit | 0 | 78 | 20 |
| count_non_d_hex | 0 | 58 | 21 |
| count_low_surrogate | 0 | 120 | 26 |
| count_name_dq_char | 0 | 5220 | 40 |
| count_name_sq_chars | 0 | 50 | 28 |
| count_name_sq_mixed | 0 | 50 | 14 |
| count_name_sq_special | 0 | 1436 | 35 |
| count_name_sq_char | 0 | 2771 | 43 |
| count_slice_selector | 0 | 18 | 16 |
| count_filter_selector | 0 | 32 | 21 |
| count_logical_expr | 0 | 38 | 34 |
| count_logical_and_expr | 0 | 238 | 58 |
| count_and_tail | 0 | 249 | 49 |
| count_basic_expr | 0 | 268 | 92 |
| count_comparison_expr | 0 | 48 | 37 |
| count_comparable | 0 | 96 | 37 |
| count_singular_query | 0 | 50 | 31 |
| count_abs_singular_query | 0 | 14 | 15 |
| count_s_singular_segment | 0 | 194 | 66 |
| count_name_segment | 0 | 96 | 48 |
| count_member_name_shorthand | 0 | 73 | 59 |
| count_index_segment | 0 | 103 | 46 |
| count_rel_singular_query | 0 | 50 | 23 |
| count_literal | 0 | 96 | 48 |
| count_number | 0 | 9 | 10 |
| count_exp | 0 | 8 | 8 |
| count_sign_opt | 0 | 9 | 10 |
| count_frac | 0 | 14 | 12 |
| count_string_literal | 0 | 96 | 21 |
| count_dq_chars | 0 | 96 | 15 |
| count_letter | 0 | 3693 | 94 |
| count_dq_mixed | 0 | 96 | 13 |
| count_dq_special | 0 | 3357 | 23 |
| count_dq_char | 0 | 6721 | 24 |
| count_sq_chars | 0 | 96 | 13 |
| count_sq_mixed | 0 | 96 | 11 |
| count_sq_special | 0 | 3214 | 20 |
| count_sq_char | 0 | 6345 | 23 |
| count_value_function_expr | 0 | 23 | 23 |
| count_count_expr | 0 | 11 | 12 |
| count_S | 0 | 194 | 100 |
| count_filter_query | 0 | 238 | 63 |
| count_rel_query | 0 | 114 | 44 |
| count_or_tail | 0 | 221 | 30 |
| count_more_selector | 0 | 195 | 47 |
| count_child_segment | 0 | 83 | 67 |
| count_abs_query | 0 | 124 | 45 |
| count_value_expr | 0 | 9 | 10 |
| count_length_expr | 0 | 11 | 11 |
| count_value_argument | 0 | 44 | 29 |
| count_paren_expr | 0 | 24 | 25 |
| count_logical_not_op | 0 | 55 | 38 |
| count_test_expr | 0 | 235 | 62 |
| count_logical_function_expr | 0 | 40 | 24 |
| count_search_expr | 0 | 9 | 10 |
| count_regex_argument | 0 | 40 | 24 |
| count_iregexp_literal | 0 | 40 | 22 |
| count_ire_regexp | 0 | 81 | 56 |
| count_match_expr | 0 | 40 | 22 |
| count_ire_alt | 0 | 491 | 77 |
| count_ire_branch | 0 | 527 | 84 |
| count_ire_piece | 0 | 793 | 104 |
| count_ire_char_class | 0 | 206 | 64 |
| count_ire_char_class_expr | 0 | 206 | 42 |
| count_ire_quantifier | 0 | 380 | 88 |
| count_ire_range_quantifier | 0 | 103 | 56 |
| count_ire_cce1 | 0 | 1406 | 86 |
| count_ire_normal_char | 0 | 489 | 62 |
| count_ws | 4 | 367 | 92 |
| count_nonempty_array | 0 | 16 | 12 |
| count_value | 1 | 131 | 52 |
| count_doc_number | 0 | 18 | 15 |
| count_doc_exp | 0 | 9 | 9 |
| count_object | 0 | 17 | 16 |
| count_nonempty_object | 0 | 11 | 12 |
| count_member | 0 | 57 | 32 |
| count_doc_name_mixed | 0 | 50 | 18 |
| count_doc_name_special | 0 | 2421 | 37 |
| count_doc_escape | 0 | 2428 | 44 |
| count_doc_name_char | 0 | 4734 | 46 |
| count_doc_string | 0 | 16 | 17 |
| count_array | 0 | 24 | 17 |
| count_more_member | 0 | 46 | 32 |
| count_doc_mixed | 0 | 11 | 8 |
| count_doc_special | 0 | 44 | 18 |
| count_doc_char | 0 | 76 | 23 |
| count_more_value | 0 | 78 | 33 |
| doc_depth | 1 | 13 | 12 |
| doc_bytes | 3 | 8004 | 164 |
| query_len | 1 | 10647 | 352 |

## frontier
[pyjsonpath_known] grammar frontier (targeting stopped asking here):
  count_selector: pinned at 210 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_filter_selector: pinned at 32 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_ire_cce1: pinned at 1406 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_value: pinned at 131 by the SEARCH; 1 escalating request(s) returned nothing further.
  query_len: pinned at 10647 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 499 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_selector bins move with count_filter_selector (1..6 across bins); count_value (1..8 across bins); query_len (3..1808 across bins) -- those regions are joint, not count_selector findings
[compare] count_filter_selector bins move with count_selector (4..33 across bins); count_value (1..8 across bins); query_len (33..1904 across bins) -- those regions are joint, not count_filter_selector findings
[compare] count_value bins move with count_selector (0.5..13 across bins); query_len (33..1778 across bins) -- those regions are joint, not count_value findings
[compare] query_len bins move with count_selector (1..23 across bins); count_value (1..9 across bins) -- those regions are joint, not query_len findings
  pyjsonpath_1_3_2 and pyjsonpath_2_0_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.02, n=486)
      DEPENDS ON SAMPLING: counting each count_value bin once gives 1.27x (95% CI 1.13-1.83, 6 bins, equal weight per bin), verdict 'a_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each query_len bin once gives 1.17x (95% CI 1.08-1.43, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      undecided on count_selector (confounded) in [1,2.438) -- needs more inputs
      undecided on count_filter_selector (confounded) in =0, [1,1.782) -- needs more inputs
      undecided on count_value (confounded) in [11.45,25.79), [25.79,58.13), [58.13,131] -- needs more inputs
      undecided on query_len (confounded) in [103.2,484), [2270,1.065e+04] -- needs more inputs
[interference] 5 property pair(s) tested over 1144 rows; 3 show a dependence
  query_len vs runtime_ns changes with count_selector: rho by count_selector stratum = [+0.79, +0.23, -0.04, -0.18], spread 0.96, p=0.003
  count_selector vs runtime_ns changes with query_len: rho by query_len stratum = [+0.50, +0.17, -0.37, -0.20], spread 0.88, p=0.003
  count_value vs runtime_ns changes with query_len: rho by query_len stratum = [+0.23, +0.27, -0.02, -0.23], spread 0.50, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
