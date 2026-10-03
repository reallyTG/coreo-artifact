# simplejson_known

- corpus: 764 rows, 382 inputs, 2 systems
- elapsed: 3429s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_ws | 2 | 347 | 158 |
| count_wschar | 0 | 135 | 89 |
| count_object | 0 | 9 | 9 |
| count_end_object | 0 | 6 | 7 |
| count_begin_object | 0 | 6 | 7 |
| count_more_member | 0 | 48 | 30 |
| count_value_separator | 0 | 91 | 38 |
| count_string | 0 | 63 | 44 |
| count_char_2 | 0 | 487 | 143 |
| count_unescaped_ascii_other | 0 | 254 | 121 |
| count_char_3 | 0 | 259 | 114 |
| count_escaped | 0 | 140 | 80 |
| count_unescaped_nonascii | 0 | 139 | 87 |
| count_unescaped_alnum | 0 | 519 | 137 |
| count_value | 0 | 100 | 39 |
| count_false | 0 | 20 | 16 |
| count_null | 0 | 21 | 18 |
| count_true | 0 | 22 | 18 |
| count_float_number | 0 | 10 | 5 |
| count_exp | 0 | 7 | 5 |
| count_exp_opt | 0 | 6 | 5 |
| count_minus_opt | 0 | 16 | 9 |
| count_minus | 0 | 7 | 8 |
| count_int_frac | 0 | 6 | 5 |
| count_int_sig | 0 | 4 | 5 |
| count_integer_number | 0 | 6 | 7 |
| count_more_value | 0 | 90 | 18 |
| count_begin_array | 0 | 11 | 8 |
| count_end_array | 0 | 11 | 8 |
| count_exp_zeros | 0 | 11 | 11 |
| count_DIGIT | 0 | 38 | 22 |
| count_digit1_9 | 0 | 6 | 6 |
| count_zero | 0 | 3 | 4 |
| count_int_upto15 | 0 | 5 | 4 |
| count_int_16 | 0 | 4 | 5 |
| count_u_escape | 0 | 20 | 21 |
| count_unescaped_utf8_3 | 0 | 51 | 45 |
| count_unescaped_utf8_2 | 0 | 54 | 50 |
| count_unescaped_utf8_4 | 0 | 53 | 49 |
| count_hex_high_surrogate_not3f | 0 | 9 | 10 |
| count_hex_high_surrogate | 0 | 9 | 10 |
| count_hex_low_surrogate_fffe | 0 | 9 | 10 |
| count_hex_low_surrogate | 0 | 9 | 10 |
| count_hex_bmp | 0 | 9 | 10 |
| count_root_scalar | 0 | 1 | 2 |
| depth | 0 | 15 | 10 |
| num_pairs | 0 | 50 | 31 |
| num_arrays | 0 | 11 | 12 |
| num_numbers | 0 | 16 | 9 |
| total_string_len | 0 | 948 | 153 |

## frontier
[simplejson_known] grammar frontier (targeting stopped asking here):
  count_end_object: pinned at 6 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_u_escape: pinned at 20 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_root_scalar: pinned at 1 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 382 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_wschar bins move with count_null (1..7 across bins); count_u_escape (3..10 across bins); num_pairs (1..40 across bins) -- those regions are joint, not count_wschar findings
[compare] count_null bins move with count_wschar (9..80.5 across bins); count_u_escape (1..13 across bins); num_pairs (1..40 across bins) -- those regions are joint, not count_null findings
[compare] count_u_escape bins move with count_wschar (4..61.5 across bins); count_null (1..5.5 across bins); num_pairs (3..25 across bins) -- those regions are joint, not count_u_escape findings
[compare] num_pairs bins move with count_wschar (3..74 across bins); count_null (1..8 across bins); count_u_escape (3..11 across bins) -- those regions are joint, not num_pairs findings
  simplejson_3_20_2 and simplejson_4_0_0 equivalent: ratio 0.98x within the equivalence band (95% CI 0.98-0.98, n=382)
[compare] memory_peak: 382 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_wschar bins move with count_null (1..7 across bins); count_u_escape (3..10 across bins); num_pairs (1..40 across bins) -- those regions are joint, not count_wschar findings
[compare] count_null bins move with count_wschar (9..80.5 across bins); count_u_escape (1..13 across bins); num_pairs (1..40 across bins) -- those regions are joint, not count_null findings
[compare] count_u_escape bins move with count_wschar (4..61.5 across bins); count_null (1..5.5 across bins); num_pairs (3..25 across bins) -- those regions are joint, not count_u_escape findings
[compare] num_pairs bins move with count_wschar (3..74 across bins); count_null (1..8 across bins); count_u_escape (3..11 across bins) -- those regions are joint, not num_pairs findings
  simplejson_3_20_2 and simplejson_4_0_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=382)
[compare] dominance across runtime_ns, memory_peak:
  simplejson_3_20_2 and simplejson_4_0_0 EQUIVALENT on every metric
      count_wschar [1,2.265) (n=18): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_wschar [2.265,5.13) (n=18): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_wschar [5.13,11.62) (n=16): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_wschar [11.62,26.32) (n=48): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_wschar [26.32,59.6) (n=145): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_wschar [59.6,135] (n=132): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null =0 (n=93): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null [1,1.661) (n=38): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null [1.661,2.759) (n=23): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null [2.759,4.583) (n=47): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null [4.583,7.612) (n=119): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null [7.612,12.64) (n=52): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_null [12.64,21] (n=10): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_u_escape =0 (n=54): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_u_escape [1,1.648) (n=17): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_u_escape [2.714,4.472) (n=26): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_u_escape [4.472,7.368) (n=52): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_u_escape [7.368,12.14) (n=152): simplejson_3_20_2, simplejson_4_0_0 not dominated
      count_u_escape [12.14,20] (n=74): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs =0 (n=46): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [1.919,3.684) (n=31): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [3.684,7.071) (n=27): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [7.071,13.57) (n=33): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [13.57,26.05) (n=153): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [26.05,50] (n=88): simplejson_3_20_2, simplejson_4_0_0 not dominated
[interference] 12 property pair(s) tested over 764 rows; 9 show a dependence
  count_u_escape vs runtime_ns changes with count_wschar: rho by count_wschar stratum = [+0.82, +0.53, +0.21, -0.15], spread 0.97, p=0.003
  count_u_escape vs runtime_ns changes with count_null: rho by count_null stratum = [+0.89, +0.78, +0.12, +0.18], spread 0.77, p=0.003
  count_u_escape vs runtime_ns changes with num_pairs: rho by num_pairs stratum = [+0.85, +0.56, +0.67, +0.24], spread 0.61, p=0.003
  count_null vs runtime_ns changes with count_wschar: rho by count_wschar stratum = [+0.47, +0.29, +0.68, +0.11], spread 0.57, p=0.003
  count_wschar vs runtime_ns changes with count_null: rho by count_null stratum = [+0.83, +0.71, +0.46, +0.28], spread 0.55, p=0.003
  count_wschar vs runtime_ns changes with num_pairs: rho by num_pairs stratum = [+0.75, +0.43, +0.46, +0.33], spread 0.41, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
