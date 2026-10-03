# orjson_known

- corpus: 4176 rows, 696 inputs, 6 systems
- elapsed: 3519s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_ws | 2 | 392 | 190 |
| count_wschar | 0 | 181 | 105 |
| count_end_array | 0 | 11 | 8 |
| count_more_value | 0 | 90 | 26 |
| count_value_separator | 0 | 91 | 45 |
| count_value | 0 | 100 | 50 |
| count_string | 0 | 84 | 55 |
| count_char_2 | 0 | 478 | 181 |
| count_unescaped_ascii_other | 0 | 252 | 138 |
| count_char_3 | 0 | 257 | 141 |
| count_escaped | 0 | 126 | 101 |
| count_u_escape | 0 | 19 | 20 |
| count_unescaped_nonascii | 0 | 135 | 100 |
| count_unescaped_utf8_2 | 0 | 54 | 51 |
| count_unescaped_utf8_4 | 0 | 48 | 47 |
| count_unescaped_utf8_3 | 0 | 49 | 48 |
| count_unescaped_alnum | 0 | 519 | 182 |
| count_null | 0 | 21 | 19 |
| count_float_number | 0 | 10 | 8 |
| count_exp_opt | 0 | 6 | 6 |
| count_exp | 0 | 7 | 6 |
| count_minus | 0 | 7 | 8 |
| count_exp_zeros | 0 | 13 | 12 |
| count_int_sig | 0 | 4 | 5 |
| count_zero | 0 | 4 | 5 |
| count_DIGIT | 0 | 41 | 23 |
| count_digit1_9 | 0 | 6 | 6 |
| count_int_frac | 0 | 6 | 6 |
| count_minus_opt | 0 | 16 | 11 |
| count_integer_number | 0 | 6 | 7 |
| count_int_16 | 0 | 4 | 5 |
| count_int_upto15 | 0 | 5 | 4 |
| count_false | 0 | 20 | 19 |
| count_true | 0 | 22 | 20 |
| count_object | 0 | 9 | 10 |
| count_begin_array | 0 | 11 | 8 |
| count_end_object | 0 | 9 | 10 |
| count_more_member | 0 | 72 | 28 |
| count_begin_object | 0 | 9 | 10 |
| count_hex_low_surrogate_fffe | 0 | 10 | 11 |
| count_hex_low_surrogate | 0 | 9 | 10 |
| count_hex_high_surrogate | 0 | 9 | 10 |
| count_hex_high_surrogate_not3f | 0 | 10 | 11 |
| count_hex_bmp | 0 | 11 | 11 |
| count_root_scalar | 0 | 1 | 2 |
| depth | 0 | 15 | 12 |
| num_pairs | 0 | 75 | 32 |
| num_arrays | 0 | 11 | 12 |
| num_numbers | 0 | 16 | 11 |
| total_string_len | 0 | 951 | 203 |

## frontier
[orjson_known] grammar frontier (targeting stopped asking here):
  count_null: pinned at 21 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_false: pinned at 20 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_true: pinned at 22 by the SEARCH; 1 escalating request(s) returned nothing further.
  num_arrays: pinned at 11 by the SEARCH; 1 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 696 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_string bins move with count_null (1..10 across bins); count_true (1..9.5 across bins); num_arrays (2..9 across bins) -- those regions are joint, not count_string findings
[compare] count_null bins move with count_string (3..59 across bins); count_true (1..9 across bins); num_arrays (0.5..7 across bins) -- those regions are joint, not count_null findings
[compare] count_true bins move with count_string (2..58 across bins); count_null (1..9 across bins); num_arrays (2..9 across bins) -- those regions are joint, not count_true findings
[compare] num_arrays bins move with count_string (3..58 across bins); count_null (1..9 across bins); count_true (2..10 across bins) -- those regions are joint, not num_arrays findings
  orjson_3_10_1 and orjson_3_10_2 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-0.99, n=696)
  orjson_3_10_1 and orjson_3_10_3 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-0.99, n=696)
  orjson_3_10_1 and orjson_3_10_4 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=696)
      undecided on count_true (confounded) in [13.14,22] -- needs more inputs
  orjson_3_10_1 and orjson_3_10_5 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=696)
      undecided on count_null (confounded) in [12.64,21] -- needs more inputs
      undecided on count_true (confounded) in [13.14,22] -- needs more inputs
  orjson_3_10_1 and orjson_3_10_6 equivalent: ratio 0.98x within the equivalence band (95% CI 0.98-0.98, n=696)
  orjson_3_10_2 and orjson_3_10_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_2 and orjson_3_10_4 equivalent: ratio 0.98x within the equivalence band (95% CI 0.98-0.98, n=696)
  orjson_3_10_2 and orjson_3_10_5 equivalent: ratio 0.98x within the equivalence band (95% CI 0.98-0.98, n=696)
  orjson_3_10_2 and orjson_3_10_6 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-0.99, n=696)
  orjson_3_10_3 and orjson_3_10_4 equivalent: ratio 0.98x within the equivalence band (95% CI 0.98-0.98, n=696)
  orjson_3_10_3 and orjson_3_10_5 equivalent: ratio 0.98x within the equivalence band (95% CI 0.98-0.98, n=696)
  orjson_3_10_3 and orjson_3_10_6 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-0.99, n=696)
  orjson_3_10_4 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_4 and orjson_3_10_6 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=696)
  orjson_3_10_5 and orjson_3_10_6 equivalent: ratio 1.01x within the equivalence band (95% CI 1.01-1.01, n=696)
[compare] memory_peak: 696 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_string bins move with count_null (1..10 across bins); count_true (1..9.5 across bins); num_arrays (2..9 across bins) -- those regions are joint, not count_string findings
[compare] count_null bins move with count_string (3..59 across bins); count_true (1..9 across bins); num_arrays (0.5..7 across bins) -- those regions are joint, not count_null findings
[compare] count_true bins move with count_string (2..58 across bins); count_null (1..9 across bins); num_arrays (2..9 across bins) -- those regions are joint, not count_true findings
[compare] num_arrays bins move with count_string (3..58 across bins); count_null (1..9 across bins); count_true (2..10 across bins) -- those regions are joint, not num_arrays findings
  orjson_3_10_1 and orjson_3_10_2 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_1 and orjson_3_10_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_1 and orjson_3_10_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_1 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_1 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_2 and orjson_3_10_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_2 and orjson_3_10_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_2 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_2 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_3 and orjson_3_10_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_3 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_3 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_4 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_4 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
  orjson_3_10_5 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=696)
[compare] dominance across runtime_ns, memory_peak:
  orjson_3_10_1 and orjson_3_10_2 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_3 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_4 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_5 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_6 EQUIVALENT on every metric
  orjson_3_10_2 and orjson_3_10_3 EQUIVALENT on every metric
  orjson_3_10_2 and orjson_3_10_4 EQUIVALENT on every metric
  orjson_3_10_2 and orjson_3_10_5 EQUIVALENT on every metric
  orjson_3_10_2 and orjson_3_10_6 EQUIVALENT on every metric
  orjson_3_10_3 and orjson_3_10_4 EQUIVALENT on every metric
  orjson_3_10_3 and orjson_3_10_5 EQUIVALENT on every metric
  orjson_3_10_3 and orjson_3_10_6 EQUIVALENT on every metric
  orjson_3_10_4 and orjson_3_10_5 EQUIVALENT on every metric
  orjson_3_10_4 and orjson_3_10_6 EQUIVALENT on every metric
  orjson_3_10_5 and orjson_3_10_6 EQUIVALENT on every metric
      count_string =0 (n=22): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_string [1,2.093) (n=47): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_string [2.093,4.38) (n=60): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_string [4.38,9.165) (n=31): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_string [9.165,19.18) (n=65): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_string [19.18,40.14) (n=313): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_string [40.14,84] (n=158): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null =0 (n=117): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null [1,1.661) (n=62): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null [1.661,2.759) (n=35): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null [2.759,4.583) (n=118): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null [4.583,7.612) (n=204): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null [7.612,12.64) (n=97): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_null [12.64,21] (n=63): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true =0 (n=108): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true [1,1.674) (n=55): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true [1.674,2.802) (n=49): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true [2.802,4.69) (n=86): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true [4.69,7.851) (n=261): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true [7.851,13.14) (n=100): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      count_true [13.14,22] (n=37): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays =0 (n=130): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays [1,1.491) (n=62): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays [1.491,2.224) (n=87): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays [2.224,3.317) (n=80): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays [3.317,4.946) (n=81): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays [4.946,7.376) (n=142): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      num_arrays [7.376,11] (n=114): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
[interference] 12 property pair(s) tested over 4176 rows; 12 show a dependence
  count_string vs runtime_ns changes with count_true: rho by count_true stratum = [+0.86, +0.25, -0.13, +0.57], spread 0.99, p=0.003
  count_string vs runtime_ns changes with count_null: rho by count_null stratum = [+0.89, +0.49, -0.01, +0.31], spread 0.90, p=0.003
  count_true vs runtime_ns changes with count_string: rho by count_string stratum = [+0.54, +0.22, -0.24, +0.42], spread 0.78, p=0.003
  count_string vs runtime_ns changes with num_arrays: rho by num_arrays stratum = [+0.85, +0.33, +0.16, +0.14], spread 0.71, p=0.003
  num_arrays vs runtime_ns changes with count_null: rho by count_null stratum = [+0.59, +0.64, +0.11, -0.07], spread 0.70, p=0.003
  count_null vs runtime_ns changes with count_string: rho by count_string stratum = [+0.46, +0.35, -0.21, +0.01], spread 0.66, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
