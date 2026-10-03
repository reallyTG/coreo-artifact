# jpython_known

- corpus: 2624 rows, 656 inputs, 4 systems
- elapsed: 3470s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_s_segment | 0 | 193 | 121 |
| count_B | 0 | 2096 | 419 |
| count_child_segment | 0 | 99 | 82 |
| count_wildcard_selector | 0 | 126 | 90 |
| count_member_name_shorthand | 0 | 77 | 68 |
| count_name_first | 0 | 2865 | 225 |
| count_name_char | 0 | 2865 | 208 |
| count_bracketed_selection | 0 | 32 | 33 |
| count_selector | 0 | 210 | 67 |
| count_index_selector | 0 | 103 | 57 |
| count_int | 0 | 103 | 72 |
| count_pos_int | 0 | 77 | 52 |
| count_DIGIT1 | 0 | 195 | 114 |
| count_DIGIT | 0 | 251 | 140 |
| count_name_selector | 0 | 54 | 43 |
| count_name_sq_chars | 0 | 50 | 28 |
| count_name_sq_mixed | 0 | 50 | 13 |
| count_name_sq_special | 0 | 1436 | 34 |
| count_escapable | 0 | 1159 | 52 |
| count_hexchar | 0 | 256 | 37 |
| count_high_surrogate | 0 | 120 | 26 |
| count_D | 0 | 318 | 39 |
| count_HEXDIG | 0 | 810 | 54 |
| count_non_surrogate | 0 | 136 | 26 |
| count_oct_digit | 0 | 78 | 21 |
| count_non_d_hex | 0 | 58 | 21 |
| count_low_surrogate | 0 | 120 | 26 |
| count_name_sq_char | 0 | 2771 | 41 |
| count_name_dq_chars | 0 | 40 | 31 |
| count_name_dq_mixed | 0 | 40 | 19 |
| count_name_dq_special | 0 | 2617 | 32 |
| count_name_dq_char | 0 | 5220 | 41 |
| count_filter_selector | 0 | 32 | 21 |
| count_logical_expr | 0 | 38 | 35 |
| count_or_tail | 0 | 221 | 31 |
| count_logical_and_expr | 0 | 238 | 59 |
| count_and_tail | 0 | 249 | 46 |
| count_basic_expr | 0 | 268 | 91 |
| count_test_expr | 0 | 235 | 61 |
| count_filter_query | 0 | 238 | 61 |
| count_abs_query | 0 | 124 | 44 |
| count_slice_selector | 0 | 18 | 17 |
| count_more_selector | 0 | 195 | 49 |
| count_descendant_segment | 0 | 94 | 78 |
| count_rel_query | 0 | 114 | 44 |
| count_S | 0 | 194 | 103 |
| count_logical_function_expr | 0 | 40 | 23 |
| count_search_expr | 0 | 8 | 9 |
| count_value_argument | 0 | 44 | 28 |
| count_literal | 0 | 96 | 46 |
| count_number | 0 | 9 | 10 |
| count_exp | 0 | 6 | 7 |
| count_sign_opt | 0 | 12 | 10 |
| count_frac | 0 | 14 | 12 |
| count_string_literal | 0 | 96 | 20 |
| count_dq_chars | 0 | 96 | 15 |
| count_letter | 0 | 3693 | 96 |
| count_dq_mixed | 0 | 96 | 13 |
| count_dq_special | 0 | 3357 | 23 |
| count_dq_char | 0 | 6721 | 24 |
| count_sq_chars | 0 | 96 | 12 |
| count_sq_mixed | 0 | 96 | 11 |
| count_sq_special | 0 | 3214 | 20 |
| count_sq_char | 0 | 6345 | 24 |
| count_singular_query | 0 | 50 | 31 |
| count_abs_singular_query | 0 | 14 | 15 |
| count_s_singular_segment | 0 | 194 | 73 |
| count_index_segment | 0 | 103 | 48 |
| count_name_segment | 0 | 96 | 48 |
| count_rel_singular_query | 0 | 50 | 23 |
| count_value_function_expr | 0 | 22 | 22 |
| count_length_expr | 0 | 11 | 12 |
| count_count_expr | 0 | 10 | 11 |
| count_value_expr | 0 | 9 | 10 |
| count_regex_argument | 0 | 40 | 23 |
| count_iregexp_literal | 0 | 40 | 22 |
| count_ire_regexp | 0 | 83 | 59 |
| count_ire_branch | 0 | 527 | 93 |
| count_ire_piece | 0 | 793 | 108 |
| count_ire_alt | 0 | 491 | 80 |
| count_ire_char_class | 0 | 206 | 65 |
| count_ire_quantifier | 0 | 380 | 94 |
| count_ire_range_quantifier | 0 | 103 | 56 |
| count_match_expr | 0 | 40 | 22 |
| count_logical_not_op | 0 | 55 | 38 |
| count_comparison_expr | 0 | 48 | 37 |
| count_comparable | 0 | 96 | 37 |
| count_paren_expr | 0 | 26 | 27 |
| count_ire_char_class_expr | 0 | 206 | 43 |
| count_ire_cce1 | 0 | 1406 | 94 |
| count_ire_normal_char | 0 | 489 | 64 |
| count_ws | 4 | 367 | 79 |
| count_nonempty_array | 0 | 16 | 12 |
| count_value | 1 | 131 | 41 |
| count_array | 0 | 24 | 16 |
| count_doc_string | 0 | 16 | 17 |
| count_object | 0 | 18 | 15 |
| count_nonempty_object | 0 | 11 | 12 |
| count_doc_number | 0 | 19 | 17 |
| count_doc_exp | 0 | 12 | 10 |
| count_more_value | 0 | 78 | 30 |
| count_doc_mixed | 0 | 11 | 9 |
| count_doc_special | 0 | 44 | 19 |
| count_doc_char | 0 | 76 | 21 |
| count_member | 0 | 55 | 31 |
| count_more_member | 0 | 45 | 29 |
| count_doc_escape | 0 | 2428 | 45 |
| count_doc_name_mixed | 0 | 50 | 19 |
| count_doc_name_special | 0 | 2421 | 42 |
| count_doc_name_char | 0 | 4734 | 47 |
| doc_depth | 1 | 13 | 11 |
| doc_bytes | 3 | 8004 | 161 |
| query_len | 1 | 10647 | 365 |

## frontier
[jpython_known] grammar frontier (targeting stopped asking here):
  count_member_name_shorthand: pinned at 77 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_selector: pinned at 210 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_logical_expr: pinned at 38 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_descendant_segment: pinned at 94 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_nonempty_object: pinned at 11 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_member: pinned at 55 by the SEARCH; 1 escalating request(s) returned nothing further.
  query_len: pinned at 10647 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 656 inputs, 4 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_s_segment bins move with count_more_selector (2..20.5 across bins); query_len (1..1762 across bins) -- those regions are joint, not count_s_segment findings
[compare] count_more_selector bins move with count_s_segment (2..81.5 across bins); query_len (29..1777 across bins) -- those regions are joint, not count_more_selector findings
[compare] count_member bins move with count_s_segment (1..28 across bins); count_more_selector (1..10 across bins); query_len (43..1746 across bins) -- those regions are joint, not count_member findings
[compare] query_len bins move with count_s_segment (1..40 across bins); count_more_selector (1..13 across bins) -- those regions are joint, not query_len findings
  jpython_1_1_0 and jpython_1_1_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=656)
      undecided on count_member (confounded) in [7.416,14.46) -- needs more inputs
  jpython_1_1_2 better than jpython_1_1_0 on runtime_ns: 1.27x (95% CI 1.27-1.27, n=656, p=5.16e-109)
  jpython_1_1_3 better than jpython_1_1_0 on runtime_ns: 1.27x (95% CI 1.27-1.27, n=656, p=5.63e-109)
  jpython_1_1_2 better than jpython_1_1_1 on runtime_ns: 1.27x (95% CI 1.26-1.27, n=656, p=9.86e-109)
  jpython_1_1_3 better than jpython_1_1_1 on runtime_ns: 1.27x (95% CI 1.27-1.27, n=656, p=5.59e-109)
  jpython_1_1_2 and jpython_1_1_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=656)
[interference] 6 property pair(s) tested over 2624 rows; 4 show a dependence
  count_s_segment vs runtime_ns changes with query_len: rho by query_len stratum = [+0.27, -0.04, -0.03, +0.17], spread 0.31, p=0.003
  count_more_selector vs runtime_ns changes with query_len: rho by query_len stratum = [+0.12, -0.02, -0.09, +0.19], spread 0.29, p=0.003
  count_member vs runtime_ns changes with count_s_segment: rho by count_s_segment stratum = [+0.12, +0.06, +0.19, -0.09], spread 0.27, p=0.003
  count_member vs runtime_ns changes with query_len: rho by query_len stratum = [+0.12, +0.12, +0.39, +0.30], spread 0.27, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
