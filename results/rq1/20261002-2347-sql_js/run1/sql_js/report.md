# sql_js

- corpus: 1026 rows, 342 inputs, 3 systems
- elapsed: 3430s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_select_stmt | 1 | 45 | 35 |
| count_with_query | 0 | 36 | 16 |
| count_with_query_name | 0 | 39 | 29 |
| count_col_id | 1 | 119 | 89 |
| count_col_id_rare | 0 | 79 | 55 |
| count_quoted_identifier | 0 | 79 | 37 |
| count_qchar | 0 | 1834 | 121 |
| count_identifier | 0 | 90 | 75 |
| count_ident_char | 0 | 1716 | 193 |
| count_ws | 21 | 455 | 155 |
| count_ws_1 | 7 | 229 | 112 |
| count_ws_2 | 3 | 117 | 78 |
| count_ws_unit | 0 | 30 | 30 |
| count_ows | 4 | 320 | 177 |
| count_select_with_parens | 0 | 44 | 35 |
| count_ws_nc | 0 | 45 | 40 |
| count_more_recursive_with_query | 0 | 22 | 9 |
| count_more_with_query | 0 | 33 | 11 |
| count_recursive_with_query | 0 | 24 | 14 |
| count_simple_select | 1 | 84 | 48 |
| count_set_operation | 0 | 79 | 26 |
| count_order_by_clause | 0 | 14 | 9 |
| count_offset_rows_clause | 0 | 14 | 13 |
| count_offset_clause | 0 | 1 | 2 |
| count_fetch_clause | 0 | 3 | 4 |
| count_limit_clause | 0 | 12 | 13 |
| count_lock_strength | 0 | 17 | 17 |
| count_ws_nc_1 | 0 | 28 | 23 |
| count_ws_nc_unit | 0 | 12 | 13 |
| count_name_list | 0 | 24 | 15 |
| count_more_name | 0 | 94 | 43 |
| count_set_operand | 0 | 80 | 32 |
| count_select_list | 0 | 56 | 35 |
| count_select_list_opt | 0 | 47 | 37 |
| count_all_opt | 0 | 47 | 37 |
| count_distinct_clause | 0 | 37 | 24 |
| count_sortby | 0 | 60 | 12 |
| count_more_sortby | 0 | 55 | 11 |
| count_int32_const | 0 | 16 | 17 |
| count_row_or_rows | 0 | 14 | 14 |
| count_a_expr | 0 | 73 | 49 |
| count_target_el | 0 | 134 | 53 |
| count_output_name | 0 | 3 | 4 |
| count_more_target_el | 0 | 123 | 31 |
| count_grouping_element | 0 | 60 | 12 |
| count_expr_list | 0 | 18 | 15 |
| count_more_grouping_element | 0 | 55 | 13 |
| count_more_from_item | 0 | 77 | 12 |
| count_from_item | 0 | 84 | 21 |
| count_table_primary | 0 | 86 | 31 |
| count_joined_table | 0 | 66 | 18 |
| count_or_expr | 0 | 73 | 57 |
| count_more_expr | 0 | 66 | 14 |
| count_digit | 0 | 1271 | 123 |
| count_nonzero_digit | 0 | 16 | 17 |
| count_and_expr | 0 | 74 | 59 |
| count_lateral_opt | 0 | 38 | 26 |
| count_table_name | 0 | 48 | 22 |
| count_func_application | 0 | 37 | 22 |
| count_alias_clause | 0 | 18 | 13 |
| count_alias_clause_opt | 0 | 85 | 29 |
| count_with_ordinality_opt | 0 | 37 | 21 |
| count_join_qual | 0 | 4 | 5 |
| count_join_type | 0 | 4 | 5 |
| count_not_expr | 0 | 92 | 74 |
| count_agg_order_by_opt | 0 | 2 | 3 |
| count_outer_opt | 0 | 3 | 4 |
| count_is_expr | 0 | 74 | 59 |
| count_not_expr_rare | 0 | 47 | 43 |
| count_is_test | 0 | 32 | 29 |
| count_sub_operand | 0 | 17 | 13 |
| count_pred_expr | 0 | 74 | 60 |
| count_comp_op | 0 | 12 | 13 |
| count_sub_type | 0 | 17 | 13 |
| count_not_opt | 0 | 25 | 23 |
| count_op_expr | 0 | 75 | 63 |
| count_in_expr | 0 | 5 | 6 |
| count_like_op | 0 | 8 | 9 |
| count_b_op_expr | 0 | 22 | 20 |
| count_add_expr | 0 | 76 | 66 |
| count_op_tail_more | 0 | 8 | 9 |
| count_op_tail | 0 | 8 | 9 |
| count_qual_op | 0 | 12 | 10 |
| count_b_add_expr | 0 | 30 | 23 |
| count_add_tail | 0 | 13 | 13 |
| count_mul_expr | 0 | 79 | 72 |
| count_add_tail_more | 0 | 13 | 13 |
| count_any_operator | 0 | 2 | 3 |
| count_b_mul_expr | 0 | 64 | 41 |
| count_exp_expr | 0 | 85 | 79 |
| count_mul_tail | 0 | 24 | 20 |
| count_mul_tail_more | 0 | 24 | 20 |
| count_b_exp_expr | 0 | 112 | 50 |
| count_exp_expr_rare | 0 | 38 | 38 |
| count_at_expr | 0 | 92 | 83 |
| count_unary_expr | 0 | 150 | 116 |
| count_exp_tail | 0 | 26 | 19 |
| count_exp_tail_more | 0 | 26 | 19 |
| count_at_expr_rare | 0 | 45 | 43 |
| count_cast_expr | 0 | 171 | 108 |
| count_unary_expr_rare | 0 | 75 | 59 |
| count_at_tail | 0 | 24 | 23 |
| count_at_tail_more | 0 | 24 | 23 |
| count_c_expr | 0 | 171 | 108 |
| count_cast_expr_rare | 0 | 51 | 47 |
| count_aexpr_const | 0 | 171 | 89 |
| count_columnref | 0 | 32 | 31 |
| count_c_expr_compound | 0 | 40 | 38 |
| count_typecast | 0 | 35 | 29 |
| count_typecast_more | 0 | 35 | 29 |
| count_fconst | 0 | 7 | 8 |
| count_xconst | 0 | 144 | 23 |
| count_const_typename | 0 | 76 | 30 |
| count_sconst | 0 | 152 | 43 |
| count_bconst | 0 | 171 | 25 |
| count_iconst | 0 | 85 | 21 |
| count_subscripts_opt | 0 | 36 | 35 |
| count_func_expr | 0 | 4 | 5 |
| count_array_expr | 0 | 12 | 13 |
| count_case_expr | 0 | 4 | 5 |
| count_conditional_function | 0 | 3 | 4 |
| count_row_expr | 0 | 8 | 9 |
| count_cast_function | 0 | 4 | 5 |
| count_typename | 0 | 37 | 29 |
| count_exponent_opt | 0 | 6 | 7 |
| count_exponent | 0 | 4 | 5 |
| count_digits_opt | 0 | 3 | 4 |
| count_digits | 0 | 330 | 42 |
| count_hexdigit | 0 | 1489 | 47 |
| count_uchar | 0 | 1485 | 35 |
| count_schar | 0 | 1498 | 33 |
| count_echar | 0 | 1600 | 34 |
| count_e_prefix | 0 | 131 | 18 |
| count_bit | 0 | 1626 | 45 |
| count_digit_group | 0 | 305 | 34 |
| count_subscripts_rare | 0 | 23 | 21 |
| count_when_clause | 0 | 13 | 6 |
| count_array_bounds | 0 | 24 | 21 |
| count_subscript | 0 | 5 | 6 |
| count_window_definition | 0 | 2 | 3 |
| count_partition_clause | 0 | 1 | 2 |
| sql_bytes | 1515 | 3846 | 251 |
| paren_depth | 1 | 37 | 28 |

## comparison
[compare] runtime_ns: 339 inputs, 3 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_ws bins move with count_ws_2 (18..71 across bins); count_ws_unit (4..15 across bins); count_cast_expr (18..63 across bins) -- those regions are joint, not count_ws findings
[compare] count_ws_2 bins move with count_ws (73..310 across bins); count_ws_unit (3..15 across bins); count_cast_expr (17..61 across bins) -- those regions are joint, not count_ws_2 findings
[compare] count_ws_unit bins move with count_ws (82..315 across bins); count_ws_2 (17.5..75 across bins); count_cast_expr (18..75 across bins) -- those regions are joint, not count_ws_unit findings
  cst better than formatter on runtime_ns: 1.42x (95% CI 1.34-1.47, n=165, p=3.14e-14)
      undecided on count_ws (confounded) in [58.54,97.75) -- needs more inputs
      undecided on count_ws_2 (confounded) in [10.17,18.73) -- needs more inputs
      undecided on count_ws_unit (confounded) in [3.107,5.477) -- needs more inputs
      undecided on count_cast_expr in [13.08,30.81) -- needs more inputs
  cst better than pgsql on runtime_ns: 2.36x (95% CI 1.86-3.05, n=26, p=2.98e-07)
  formatter better than pgsql on runtime_ns: 2.00x (95% CI 1.64-2.33, n=32, p=2.08e-07)
[compare] rss: 339 inputs, 3 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_ws bins move with count_ws_2 (18..71 across bins); count_ws_unit (4..15 across bins); count_cast_expr (18..63 across bins) -- those regions are joint, not count_ws findings
[compare] count_ws_2 bins move with count_ws (73..310 across bins); count_ws_unit (3..15 across bins); count_cast_expr (17..61 across bins) -- those regions are joint, not count_ws_2 findings
[compare] count_ws_unit bins move with count_ws (82..315 across bins); count_ws_2 (17.5..75 across bins); count_cast_expr (18..75 across bins) -- those regions are joint, not count_ws_unit findings
  formatter better than cst on rss: 1.39x (95% CI 1.37-1.40, n=165, p=7.91e-29)
  pgsql better than cst on rss: 1.40x (95% CI 1.36-1.41, n=26, p=2.98e-08)
  formatter and pgsql equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.03, n=32)
      undecided on count_cast_expr in [13.08,30.81) -- needs more inputs
[compare] dominance across runtime_ns, rss:
  cst vs formatter TRADE-OFF: cst better on runtime_ns 1.42x; formatter better on rss 1.39x
  cst vs pgsql TRADE-OFF: cst better on runtime_ns 2.36x; pgsql better on rss 1.40x
  formatter DOMINATES pgsql: better on runtime_ns 2.00x; equivalent on rss
      count_ws [58.54,97.75) (n=13): cst, formatter, pgsql not dominated
      count_ws [97.75,163.2) (n=24): cst, formatter not dominated
      count_ws [163.2,272.5) (n=44): cst, formatter, pgsql not dominated
      count_ws [272.5,455] (n=257): cst, formatter, pgsql not dominated
      WARNING pgsql is dominated by formatter over the whole corpus but survives in [58.54,97.75), [163.2,272.5), [272.5,455] on count_ws -- the global verdict is a statement about this corpus's mix, not about the systems
      count_ws_2 [10.17,18.73) (n=10): cst, formatter, pgsql not dominated
      count_ws_2 [18.73,34.5) (n=25): cst, formatter not dominated
      count_ws_2 [34.5,63.53) (n=96): cst, formatter, pgsql not dominated
      count_ws_2 [63.53,117] (n=209): cst, formatter, pgsql not dominated
      WARNING pgsql is dominated by formatter over the whole corpus but survives in [10.17,18.73), [34.5,63.53), [63.53,117] on count_ws_2 -- the global verdict is a statement about this corpus's mix, not about the systems
      count_ws_unit [1.763,3.107) (n=8): cst, formatter, pgsql not dominated
      count_ws_unit [3.107,5.477) (n=15): cst, formatter, pgsql not dominated
      count_ws_unit [5.477,9.655) (n=44): cst, formatter not dominated
      count_ws_unit [9.655,17.02) (n=200): cst, formatter not dominated
      count_ws_unit [17.02,30] (n=70): cst, formatter, pgsql not dominated
      WARNING pgsql is dominated by formatter over the whole corpus but survives in [1.763,3.107), [3.107,5.477), [17.02,30] on count_ws_unit -- the global verdict is a statement about this corpus's mix, not about the systems
      count_cast_expr [5.55,13.08) (n=9): cst, formatter, pgsql not dominated
      count_cast_expr [13.08,30.81) (n=36): cst, formatter, pgsql not dominated
      count_cast_expr [30.81,72.58) (n=196): cst, formatter not dominated
      count_cast_expr [72.58,171] (n=95): cst, formatter, pgsql not dominated
      WARNING pgsql is dominated by formatter over the whole corpus but survives in [5.55,13.08), [13.08,30.81), [72.58,171] on count_cast_expr -- the global verdict is a statement about this corpus's mix, not about the systems
[interference] 12 property pair(s) tested over 1026 rows; 12 show a dependence
  count_ws vs runtime_ns changes with count_ws_2: rho by count_ws_2 stratum = [+0.77, +0.21, +0.21, -0.25], spread 1.03, p=0.003
  count_ws_2 vs runtime_ns changes with count_ws: rho by count_ws stratum = [+0.70, +0.09, +0.19, -0.30], spread 1.01, p=0.003
  count_ws_unit vs runtime_ns changes with count_ws: rho by count_ws stratum = [+0.60, +0.03, -0.09, -0.32], spread 0.92, p=0.003
  count_cast_expr vs runtime_ns changes with count_ws_unit: rho by count_ws_unit stratum = [+0.63, +0.08, +0.06, -0.26], spread 0.89, p=0.003
  count_ws_unit vs runtime_ns changes with count_ws_2: rho by count_ws_2 stratum = [+0.58, -0.03, -0.23, -0.19], spread 0.81, p=0.003
  count_ws_unit vs runtime_ns changes with count_cast_expr: rho by count_cast_expr stratum = [+0.68, +0.29, +0.24, -0.10], spread 0.78, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
