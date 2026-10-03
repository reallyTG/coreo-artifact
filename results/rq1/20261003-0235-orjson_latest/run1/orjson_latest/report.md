# orjson_latest

- corpus: 2304 rows, 384 inputs, 6 systems
- elapsed: 3474s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_ws | 2 | 347 | 145 |
| count_wschar | 0 | 142 | 93 |
| count_root_scalar | 0 | 1 | 2 |
| count_float_number | 0 | 10 | 7 |
| count_int_sig | 0 | 4 | 5 |
| count_DIGIT | 0 | 35 | 22 |
| count_digit1_9 | 0 | 6 | 6 |
| count_zero | 0 | 3 | 4 |
| count_int_frac | 0 | 6 | 5 |
| count_exp_opt | 0 | 6 | 5 |
| count_exp | 0 | 7 | 5 |
| count_minus | 0 | 8 | 9 |
| count_exp_zeros | 0 | 11 | 9 |
| count_minus_opt | 0 | 16 | 11 |
| count_integer_number | 0 | 7 | 8 |
| count_int_upto15 | 0 | 5 | 5 |
| count_int_16 | 0 | 4 | 5 |
| count_false | 0 | 20 | 19 |
| count_null | 0 | 21 | 17 |
| count_true | 0 | 22 | 17 |
| count_string | 0 | 64 | 46 |
| count_char_2 | 0 | 478 | 121 |
| count_char_3 | 0 | 257 | 100 |
| count_unescaped_nonascii | 0 | 135 | 81 |
| count_unescaped_utf8_3 | 0 | 45 | 42 |
| count_unescaped_utf8_2 | 0 | 54 | 45 |
| count_unescaped_utf8_4 | 0 | 47 | 42 |
| count_escaped | 0 | 125 | 74 |
| count_u_escape | 0 | 20 | 21 |
| count_hex_low_surrogate_fffe | 0 | 9 | 10 |
| count_hex_bmp | 0 | 8 | 9 |
| count_hex_high_surrogate | 0 | 9 | 10 |
| count_hex_high_surrogate_not3f | 0 | 9 | 10 |
| count_hex_low_surrogate | 0 | 9 | 10 |
| count_unescaped_ascii_other | 0 | 246 | 101 |
| count_unescaped_alnum | 0 | 519 | 124 |
| count_object | 0 | 9 | 9 |
| count_end_object | 0 | 6 | 7 |
| count_more_member | 0 | 48 | 27 |
| count_value_separator | 0 | 91 | 37 |
| count_value | 0 | 100 | 41 |
| count_begin_object | 0 | 6 | 7 |
| count_end_array | 0 | 11 | 9 |
| count_more_value | 0 | 90 | 18 |
| count_begin_array | 0 | 11 | 9 |
| depth | 0 | 15 | 11 |
| num_pairs | 0 | 50 | 32 |
| num_arrays | 0 | 12 | 13 |
| num_numbers | 0 | 16 | 11 |
| total_string_len | 0 | 948 | 133 |

## frontier
[orjson_latest] grammar frontier (targeting stopped asking here):
  count_unescaped_nonascii: pinned at 135 by the SEARCH; 1 escalating request(s) returned nothing further.
  depth: pinned at 15 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 384 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_string bins move with count_unescaped_nonascii (1..101 across bins); count_hex_high_surrogate (1..5 across bins); depth (1..4 across bins) -- those regions are joint, not count_string findings
[compare] count_unescaped_nonascii bins move with count_string (1..29 across bins); count_hex_high_surrogate (1..3 across bins); depth (1..3 across bins) -- those regions are joint, not count_unescaped_nonascii findings
[compare] count_hex_high_surrogate bins move with count_string (2..59 across bins); count_unescaped_nonascii (3..101 across bins); depth (1..3 across bins) -- those regions are joint, not count_hex_high_surrogate findings
[compare] depth bins move with count_string (1..56 across bins); count_unescaped_nonascii (19..105.5 across bins) -- those regions are joint, not depth findings
  orjson_3_11_5 and orjson_3_11_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_11_7 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_11_8 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_11_9 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=384)
  orjson_3_11_5 and orjson_3_12_0 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=384)
  orjson_3_11_6 and orjson_3_11_7 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_6 and orjson_3_11_8 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.01, n=384)
  orjson_3_11_6 and orjson_3_11_9 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=384)
  orjson_3_11_6 and orjson_3_12_0 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=384)
  orjson_3_11_7 and orjson_3_11_8 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_7 and orjson_3_11_9 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=384)
  orjson_3_11_7 and orjson_3_12_0 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=384)
  orjson_3_11_8 and orjson_3_11_9 equivalent: ratio 0.97x within the equivalence band (95% CI 0.96-0.97, n=384)
  orjson_3_11_8 and orjson_3_12_0 equivalent: ratio 0.97x within the equivalence band (95% CI 0.96-0.97, n=384)
  orjson_3_11_9 and orjson_3_12_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
[compare] memory_peak: 384 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_string bins move with count_unescaped_nonascii (1..101 across bins); count_hex_high_surrogate (1..5 across bins); depth (1..4 across bins) -- those regions are joint, not count_string findings
[compare] count_unescaped_nonascii bins move with count_string (1..29 across bins); count_hex_high_surrogate (1..3 across bins); depth (1..3 across bins) -- those regions are joint, not count_unescaped_nonascii findings
[compare] count_hex_high_surrogate bins move with count_string (2..59 across bins); count_unescaped_nonascii (3..101 across bins); depth (1..3 across bins) -- those regions are joint, not count_hex_high_surrogate findings
[compare] depth bins move with count_string (1..56 across bins); count_unescaped_nonascii (19..105.5 across bins) -- those regions are joint, not depth findings
  orjson_3_11_5 and orjson_3_11_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_11_7 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_11_8 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_11_9 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_5 and orjson_3_12_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_6 and orjson_3_11_7 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_6 and orjson_3_11_8 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_6 and orjson_3_11_9 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_6 and orjson_3_12_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_7 and orjson_3_11_8 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_7 and orjson_3_11_9 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_7 and orjson_3_12_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_8 and orjson_3_11_9 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_8 and orjson_3_12_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
  orjson_3_11_9 and orjson_3_12_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=384)
[compare] dominance across runtime_ns, memory_peak:
  orjson_3_11_5 and orjson_3_11_6 EQUIVALENT on every metric
  orjson_3_11_5 and orjson_3_11_7 EQUIVALENT on every metric
  orjson_3_11_5 and orjson_3_11_8 EQUIVALENT on every metric
  orjson_3_11_5 and orjson_3_11_9 EQUIVALENT on every metric
  orjson_3_11_5 and orjson_3_12_0 EQUIVALENT on every metric
  orjson_3_11_6 and orjson_3_11_7 EQUIVALENT on every metric
  orjson_3_11_6 and orjson_3_11_8 EQUIVALENT on every metric
  orjson_3_11_6 and orjson_3_11_9 EQUIVALENT on every metric
  orjson_3_11_6 and orjson_3_12_0 EQUIVALENT on every metric
  orjson_3_11_7 and orjson_3_11_8 EQUIVALENT on every metric
  orjson_3_11_7 and orjson_3_11_9 EQUIVALENT on every metric
  orjson_3_11_7 and orjson_3_12_0 EQUIVALENT on every metric
  orjson_3_11_8 and orjson_3_11_9 EQUIVALENT on every metric
  orjson_3_11_8 and orjson_3_12_0 EQUIVALENT on every metric
  orjson_3_11_9 and orjson_3_12_0 EQUIVALENT on every metric
      count_string =0 (n=24): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_string [1,2) (n=28): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_string [2,4) (n=29): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_string [4,8) (n=31): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_string [8,16) (n=25): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_string [16,32) (n=124): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_string [32,64] (n=123): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_unescaped_nonascii =0 (n=31): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_unescaped_nonascii [1,2.265) (n=16): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_unescaped_nonascii [2.265,5.13) (n=12): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_unescaped_nonascii [11.62,26.32) (n=28): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_unescaped_nonascii [26.32,59.6) (n=37): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_unescaped_nonascii [59.6,135] (n=256): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_hex_high_surrogate =0 (n=94): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_hex_high_surrogate [1,2.333) (n=92): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_hex_high_surrogate [2.333,3.667) (n=72): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_hex_high_surrogate [3.667,5) (n=50): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_hex_high_surrogate [5,6.333) (n=55): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      count_hex_high_surrogate [6.333,7.667) (n=16): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      depth =0 (n=36): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      depth [1,1.57) (n=53): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      depth [1.57,2.466) (n=119): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      depth [2.466,3.873) (n=111): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      depth [3.873,6.082) (n=45): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
      depth [6.082,9.552) (n=16): orjson_3_11_5, orjson_3_11_6, orjson_3_11_7, orjson_3_11_8, orjson_3_11_9, orjson_3_12_0 not dominated
[interference] 9 property pair(s) tested over 2304 rows; 9 show a dependence
  count_unescaped_nonascii vs runtime_ns changes with count_hex_high_surrogate: rho by count_hex_high_surrogate stratum = [+0.96, +0.79, -0.18, -0.33], spread 1.28, p=0.003
  count_hex_high_surrogate vs runtime_ns changes with count_unescaped_nonascii: rho by count_unescaped_nonascii stratum = [+0.51, +0.73, -0.51, +0.04], spread 1.24, p=0.003
  count_unescaped_nonascii vs runtime_ns changes with count_string: rho by count_string stratum = [+0.94, +0.52, +0.14, +0.46], spread 0.81, p=0.003
  count_string vs runtime_ns changes with count_unescaped_nonascii: rho by count_unescaped_nonascii stratum = [+0.85, +0.75, +0.53, +0.07], spread 0.78, p=0.003
  depth vs runtime_ns changes with count_string: rho by count_string stratum = [+0.69, +0.52, +0.58, -0.02], spread 0.71, p=0.003
  count_hex_high_surrogate vs runtime_ns changes with count_string: rho by count_string stratum = [+0.53, +0.38, -0.10, +0.10], spread 0.64, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
