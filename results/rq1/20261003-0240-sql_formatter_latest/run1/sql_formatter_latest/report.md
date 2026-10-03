# sql_formatter_latest

- corpus: 2544 rows, 424 inputs, 6 systems
- elapsed: 3482s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_select_stmt | 1 | 51 | 42 |
| count_more_recursive_with_query | 0 | 22 | 9 |
| count_ows | 4 | 320 | 198 |
| count_ws | 21 | 455 | 168 |
| count_ws_1 | 7 | 229 | 119 |
| count_ws_2 | 3 | 117 | 82 |
| count_ws_unit | 0 | 30 | 30 |
| count_recursive_with_query | 0 | 24 | 13 |
| count_with_query_name | 0 | 50 | 38 |
| count_col_id | 1 | 119 | 94 |
| count_identifier | 0 | 90 | 74 |
| count_ident_char | 0 | 1716 | 218 |
| count_col_id_rare | 0 | 79 | 57 |
| count_quoted_identifier | 0 | 79 | 37 |
| count_qchar | 0 | 1834 | 124 |
| count_name_list | 0 | 24 | 15 |
| count_more_name | 0 | 94 | 44 |
| count_set_operand | 0 | 80 | 34 |
| count_simple_select | 1 | 84 | 51 |
| count_from_item | 0 | 84 | 21 |
| count_table_primary | 0 | 86 | 31 |
| count_joined_table | 0 | 66 | 18 |
| count_join_qual | 0 | 4 | 5 |
| count_a_expr | 0 | 73 | 49 |
| count_or_expr | 0 | 73 | 57 |
| count_and_expr | 0 | 74 | 59 |
| count_not_expr | 0 | 92 | 74 |
| count_not_expr_rare | 0 | 47 | 43 |
| count_is_expr | 0 | 74 | 59 |
| count_ws_nc | 0 | 45 | 40 |
| count_is_test | 0 | 32 | 29 |
| count_ws_nc_1 | 0 | 28 | 24 |
| count_sub_type | 0 | 17 | 14 |
| count_comp_op | 0 | 12 | 13 |
| count_pred_expr | 0 | 74 | 60 |
| count_sub_operand | 0 | 17 | 14 |
| count_not_opt | 0 | 25 | 23 |
| count_ws_nc_unit | 0 | 13 | 14 |
| count_in_expr | 0 | 6 | 7 |
| count_op_expr | 0 | 75 | 64 |
| count_like_op | 0 | 8 | 9 |
| count_select_with_parens | 0 | 50 | 42 |
| count_b_op_expr | 0 | 22 | 20 |
| count_expr_list | 0 | 18 | 15 |
| count_op_tail | 0 | 8 | 9 |
| count_op_tail_more | 0 | 8 | 9 |
| count_add_expr | 0 | 76 | 68 |
| count_with_query | 0 | 50 | 25 |
| count_more_with_query | 0 | 48 | 22 |
| count_set_operation | 0 | 79 | 26 |
| count_order_by_clause | 0 | 14 | 9 |
| count_offset_clause | 0 | 1 | 2 |
| count_limit_clause | 0 | 12 | 13 |
| count_offset_rows_clause | 0 | 14 | 13 |
| count_fetch_clause | 0 | 3 | 4 |
| count_lock_strength | 0 | 27 | 22 |
| count_b_add_expr | 0 | 30 | 23 |
| count_qual_op | 0 | 12 | 11 |
| count_more_expr | 0 | 66 | 14 |
| count_add_tail_more | 0 | 14 | 14 |
| count_add_tail | 0 | 14 | 14 |
| count_mul_expr | 0 | 79 | 73 |
| count_all_opt | 0 | 47 | 39 |
| count_select_list_opt | 0 | 47 | 39 |
| count_distinct_clause | 0 | 37 | 25 |
| count_select_list | 0 | 56 | 39 |
| count_sortby | 0 | 60 | 12 |
| count_more_sortby | 0 | 55 | 11 |
| count_int32_const | 0 | 16 | 17 |
| count_row_or_rows | 0 | 14 | 14 |
| count_b_mul_expr | 0 | 64 | 42 |
| count_any_operator | 0 | 2 | 3 |
| count_exp_expr | 0 | 85 | 82 |
| count_mul_tail | 0 | 24 | 21 |
| count_mul_tail_more | 0 | 24 | 21 |
| count_more_from_item | 0 | 77 | 12 |
| count_target_el | 0 | 134 | 55 |
| count_more_target_el | 0 | 123 | 32 |
| count_more_grouping_element | 0 | 55 | 13 |
| count_grouping_element | 0 | 60 | 12 |
| count_digit | 0 | 1271 | 128 |
| count_nonzero_digit | 0 | 16 | 17 |
| count_b_exp_expr | 0 | 112 | 49 |
| count_exp_expr_rare | 0 | 38 | 38 |
| count_at_expr | 0 | 92 | 84 |
| count_output_name | 0 | 3 | 4 |
| count_unary_expr | 0 | 150 | 118 |
| count_exp_tail | 0 | 26 | 18 |
| count_exp_tail_more | 0 | 26 | 18 |
| count_at_expr_rare | 0 | 45 | 43 |
| count_join_type | 0 | 4 | 5 |
| count_lateral_opt | 0 | 38 | 26 |
| count_with_ordinality_opt | 0 | 37 | 21 |
| count_alias_clause_opt | 0 | 85 | 29 |
| count_func_application | 0 | 37 | 22 |
| count_table_name | 0 | 48 | 22 |
| count_alias_clause | 0 | 18 | 13 |
| count_unary_expr_rare | 0 | 75 | 60 |
| count_cast_expr | 0 | 171 | 110 |
| count_at_tail | 0 | 24 | 23 |
| count_at_tail_more | 0 | 24 | 23 |
| count_outer_opt | 0 | 3 | 4 |
| count_agg_order_by_opt | 0 | 2 | 3 |
| count_cast_expr_rare | 0 | 51 | 47 |
| count_c_expr | 0 | 171 | 110 |
| count_typecast_more | 0 | 34 | 31 |
| count_typecast | 0 | 34 | 31 |
| count_aexpr_const | 0 | 171 | 92 |
| count_c_expr_compound | 0 | 40 | 38 |
| count_columnref | 0 | 32 | 31 |
| count_typename | 0 | 35 | 31 |
| count_sconst | 0 | 152 | 43 |
| count_xconst | 0 | 144 | 24 |
| count_iconst | 0 | 85 | 22 |
| count_const_typename | 0 | 76 | 30 |
| count_fconst | 0 | 7 | 8 |
| count_bconst | 0 | 171 | 25 |
| count_conditional_function | 0 | 4 | 5 |
| count_row_expr | 0 | 8 | 9 |
| count_case_expr | 0 | 4 | 5 |
| count_func_expr | 0 | 4 | 5 |
| count_array_expr | 0 | 12 | 13 |
| count_subscripts_opt | 0 | 36 | 36 |
| count_cast_function | 0 | 3 | 4 |
| count_array_bounds | 0 | 24 | 22 |
| count_schar | 0 | 1498 | 36 |
| count_uchar | 0 | 1485 | 36 |
| count_e_prefix | 0 | 131 | 18 |
| count_echar | 0 | 1600 | 34 |
| count_hexdigit | 0 | 1489 | 46 |
| count_digits | 0 | 330 | 42 |
| count_digit_group | 0 | 305 | 35 |
| count_digits_opt | 0 | 3 | 4 |
| count_exponent | 0 | 4 | 5 |
| count_exponent_opt | 0 | 6 | 7 |
| count_bit | 0 | 1626 | 47 |
| count_when_clause | 0 | 13 | 6 |
| count_subscripts_rare | 0 | 23 | 22 |
| count_window_definition | 0 | 2 | 3 |
| count_subscript | 0 | 6 | 7 |
| count_partition_clause | 0 | 1 | 2 |
| sql_bytes | 530 | 3846 | 290 |
| paren_depth | 1 | 34 | 28 |

## frontier
[sql_formatter_latest] grammar frontier (targeting stopped asking here):
  count_ows: pinned at 320 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_col_id: pinned at 119 by the SEARCH; 1 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 421 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_ows bins move with count_with_query_name (0.5..12 across bins); count_col_id (5..65 across bins); count_all_opt (0.5..14 across bins) -- those regions are joint, not count_ows findings
[compare] count_with_query_name bins move with count_all_opt (1..25 across bins) -- those regions are joint, not count_with_query_name findings
[compare] count_col_id bins move with count_ows (22.5..170.5 across bins); count_with_query_name (1..8 across bins); count_all_opt (2..11 across bins) -- those regions are joint, not count_col_id findings
[compare] count_all_opt bins move with count_ows (43.5..216 across bins); count_with_query_name (1..24 across bins); count_col_id (13..65 across bins) -- those regions are joint, not count_all_opt findings
  sql_formatter_15_7_3 and sql_formatter_15_7_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_8_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_8_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.01, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_9_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.02, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_8_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_8_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.01, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_9_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.02, n=421)
  sql_formatter_15_8_0 and sql_formatter_15_8_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_8_0 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_8_0 and sql_formatter_15_9_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=421)
  sql_formatter_15_8_1 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_8_1 and sql_formatter_15_9_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.01, n=421)
  sql_formatter_15_8_2 and sql_formatter_15_9_0 equivalent: ratio 1.01x within the equivalence band (95% CI 1.00-1.01, n=421)
[compare] rss: 421 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_ows bins move with count_with_query_name (0.5..12 across bins); count_col_id (5..65 across bins); count_all_opt (0.5..14 across bins) -- those regions are joint, not count_ows findings
[compare] count_with_query_name bins move with count_all_opt (1..25 across bins) -- those regions are joint, not count_with_query_name findings
[compare] count_col_id bins move with count_ows (22.5..170.5 across bins); count_with_query_name (1..8 across bins); count_all_opt (2..11 across bins) -- those regions are joint, not count_col_id findings
[compare] count_all_opt bins move with count_ows (43.5..216 across bins); count_with_query_name (1..24 across bins); count_col_id (13..65 across bins) -- those regions are joint, not count_all_opt findings
  sql_formatter_15_7_3 and sql_formatter_15_7_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_8_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_8_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_3 and sql_formatter_15_9_0 equivalent: ratio 1.08x within the equivalence band (95% CI 1.06-1.10, n=421)
      undecided on count_ows (confounded) in [74.27,154.2) -- needs more inputs
      undecided on count_with_query_name (confounded) in [3.684,7.071), [7.071,13.57) -- needs more inputs
      undecided on count_all_opt (confounded) in [6.856,13.02) -- needs more inputs
  sql_formatter_15_7_4 and sql_formatter_15_8_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_8_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_7_4 and sql_formatter_15_9_0 equivalent: ratio 1.07x within the equivalence band (95% CI 1.05-1.09, n=421)
      undecided on count_ows (confounded) in [74.27,154.2) -- needs more inputs
      undecided on count_with_query_name (confounded) in [3.684,7.071), [7.071,13.57) -- needs more inputs
      undecided on count_all_opt (confounded) in [6.856,13.02) -- needs more inputs
  sql_formatter_15_8_0 and sql_formatter_15_8_1 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_8_0 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_8_0 and sql_formatter_15_9_0 equivalent: ratio 1.08x within the equivalence band (95% CI 1.05-1.10, n=421)
      undecided on count_ows (confounded) in [74.27,154.2) -- needs more inputs
      undecided on count_with_query_name (confounded) in [3.684,7.071), [7.071,13.57) -- needs more inputs
      undecided on count_all_opt (confounded) in [6.856,13.02) -- needs more inputs
  sql_formatter_15_8_1 and sql_formatter_15_8_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=421)
  sql_formatter_15_8_1 and sql_formatter_15_9_0 equivalent: ratio 1.07x within the equivalence band (95% CI 1.05-1.09, n=421)
      undecided on count_ows (confounded) in [74.27,154.2) -- needs more inputs
      undecided on count_with_query_name (confounded) in [3.684,7.071), [7.071,13.57) -- needs more inputs
      undecided on count_all_opt (confounded) in [6.856,13.02) -- needs more inputs
  sql_formatter_15_8_2 and sql_formatter_15_9_0 equivalent: ratio 1.06x within the equivalence band (95% CI 1.05-1.09, n=421)
      undecided on count_with_query_name (confounded) in [7.071,13.57) -- needs more inputs
      undecided on count_all_opt (confounded) in [6.856,13.02) -- needs more inputs
[compare] dominance across runtime_ns, rss:
  sql_formatter_15_7_3 and sql_formatter_15_7_4 EQUIVALENT on every metric
  sql_formatter_15_7_3 and sql_formatter_15_8_0 EQUIVALENT on every metric
  sql_formatter_15_7_3 and sql_formatter_15_8_1 EQUIVALENT on every metric
  sql_formatter_15_7_3 and sql_formatter_15_8_2 EQUIVALENT on every metric
  sql_formatter_15_7_3 and sql_formatter_15_9_0 EQUIVALENT on every metric
  sql_formatter_15_7_4 and sql_formatter_15_8_0 EQUIVALENT on every metric
  sql_formatter_15_7_4 and sql_formatter_15_8_1 EQUIVALENT on every metric
  sql_formatter_15_7_4 and sql_formatter_15_8_2 EQUIVALENT on every metric
  sql_formatter_15_7_4 and sql_formatter_15_9_0 EQUIVALENT on every metric
  sql_formatter_15_8_0 and sql_formatter_15_8_1 EQUIVALENT on every metric
  sql_formatter_15_8_0 and sql_formatter_15_8_2 EQUIVALENT on every metric
  sql_formatter_15_8_0 and sql_formatter_15_9_0 EQUIVALENT on every metric
  sql_formatter_15_8_1 and sql_formatter_15_8_2 EQUIVALENT on every metric
  sql_formatter_15_8_1 and sql_formatter_15_9_0 EQUIVALENT on every metric
  sql_formatter_15_8_2 and sql_formatter_15_9_0 EQUIVALENT on every metric
      count_ows [8.303,17.24) (n=8): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [17.24,35.78) (n=22): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [35.78,74.27) (n=48): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [74.27,154.2) (n=191): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [154.2,320] (n=150): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2 not dominated
      count_with_query_name =0 (n=29): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_with_query_name [1,1.919) (n=44): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_with_query_name [1.919,3.684) (n=103): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_with_query_name [3.684,7.071) (n=121): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_with_query_name [7.071,13.57) (n=55): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_with_query_name [13.57,26.05) (n=45): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2 not dominated
      count_with_query_name [26.05,50] (n=27): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2 not dominated
      count_col_id [4.919,10.91) (n=18): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [10.91,24.19) (n=50): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [24.19,53.66) (n=145): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [53.66,119] (n=202): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2 not dominated
      count_all_opt =0 (n=33): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_all_opt [1,1.9) (n=16): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_all_opt [1.9,3.609) (n=62): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_all_opt [3.609,6.856) (n=85): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_all_opt [6.856,13.02) (n=126): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_all_opt [13.02,24.74) (n=73): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2 not dominated
      count_all_opt [24.74,47] (n=29): sql_formatter_15_7_3, sql_formatter_15_7_4, sql_formatter_15_8_0, sql_formatter_15_8_1, sql_formatter_15_8_2 not dominated
[interference] 12 property pair(s) tested over 2544 rows; 8 show a dependence
  count_ows vs runtime_ns changes with count_with_query_name: rho by count_with_query_name stratum = [+0.73, +0.68, +0.43, +0.10], spread 0.64, p=0.003
  count_col_id vs runtime_ns changes with count_with_query_name: rho by count_with_query_name stratum = [+0.70, +0.78, +0.34, +0.19], spread 0.59, p=0.003
  count_all_opt vs runtime_ns changes with count_with_query_name: rho by count_with_query_name stratum = [+0.18, +0.39, +0.29, -0.12], spread 0.52, p=0.003
  count_ows vs runtime_ns changes with count_all_opt: rho by count_all_opt stratum = [+0.73, +0.59, +0.47, +0.25], spread 0.48, p=0.003
  count_col_id vs runtime_ns changes with count_all_opt: rho by count_all_opt stratum = [+0.73, +0.65, +0.38, +0.29], spread 0.44, p=0.003
  count_col_id vs runtime_ns changes with count_ows: rho by count_ows stratum = [+0.40, -0.02, +0.23, +0.17], spread 0.42, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
