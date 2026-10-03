# json

- corpus: 1872 rows, 468 inputs, 4 systems
- elapsed: 3457s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_ws | 2 | 384 | 157 |
| count_wschar | 0 | 191 | 105 |
| count_object | 0 | 13 | 13 |
| count_end_object | 0 | 8 | 9 |
| count_begin_object | 0 | 8 | 9 |
| count_string | 0 | 63 | 44 |
| count_unescaped_alnum | 0 | 519 | 143 |
| count_char_2 | 0 | 480 | 128 |
| count_char_3 | 0 | 256 | 116 |
| count_escaped | 0 | 132 | 83 |
| count_u_escape | 0 | 20 | 20 |
| count_unescaped_nonascii | 0 | 137 | 85 |
| count_unescaped_utf8_4 | 0 | 55 | 48 |
| count_unescaped_utf8_2 | 0 | 48 | 47 |
| count_unescaped_utf8_3 | 0 | 54 | 48 |
| count_unescaped_ascii_other | 0 | 247 | 116 |
| count_value | 0 | 100 | 48 |
| count_false | 0 | 20 | 19 |
| count_null | 0 | 21 | 19 |
| count_true | 0 | 22 | 19 |
| count_more_member | 0 | 48 | 22 |
| count_value_separator | 0 | 91 | 42 |
| count_float_number | 0 | 10 | 11 |
| count_int_sig | 0 | 5 | 6 |
| count_exp | 0 | 7 | 8 |
| count_int_frac | 0 | 6 | 7 |
| count_minus_opt | 0 | 16 | 14 |
| count_minus | 0 | 17 | 12 |
| count_exp_opt | 0 | 6 | 7 |
| count_integer_number | 0 | 9 | 9 |
| count_end_array | 0 | 11 | 12 |
| count_more_value | 0 | 90 | 25 |
| count_begin_array | 0 | 11 | 12 |
| count_DIGIT | 0 | 50 | 26 |
| count_zero | 0 | 5 | 6 |
| count_digit1_9 | 0 | 7 | 8 |
| count_exp_zeros | 0 | 12 | 12 |
| count_int_16 | 0 | 3 | 4 |
| count_int_upto15 | 0 | 5 | 6 |
| count_hex_low_surrogate | 0 | 10 | 10 |
| count_hex_high_surrogate | 0 | 10 | 10 |
| count_hex_high_surrogate_not3f | 0 | 9 | 10 |
| count_hex_bmp | 0 | 8 | 9 |
| count_hex_low_surrogate_fffe | 0 | 9 | 10 |
| count_root_scalar | 0 | 1 | 2 |
| depth | 0 | 15 | 14 |
| num_pairs | 0 | 50 | 29 |
| num_arrays | 0 | 15 | 12 |
| num_numbers | 0 | 16 | 14 |
| total_string_len | 0 | 950 | 144 |

## frontier
[json] grammar frontier (targeting stopped asking here):
  count_string: pinned at 63 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_null: pinned at 21 by the SEARCH; 1 escalating request(s) returned nothing further.
  depth: pinned at 15 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 468 inputs, 4 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_string bins move with count_escaped (2..104.5 across bins); count_null (3..9 across bins); depth (1..5.5 across bins) -- those regions are joint, not count_string findings
[compare] count_escaped bins move with count_string (1..30 across bins); count_null (1..5 across bins); depth (1..3 across bins) -- those regions are joint, not count_escaped findings
[compare] count_null bins move with count_string (1..58 across bins); count_escaped (1..101 across bins); depth (1..4 across bins) -- those regions are joint, not count_null findings
[compare] depth bins move with count_string (1..49 across bins); count_escaped (2..99 across bins); count_null (4..13 across bins) -- those regions are joint, not depth findings
  json_orjson better than json_simplejson on runtime_ns: 3.54x (95% CI 3.50-3.59, n=468, p=2.13e-78)
  json_orjson better than json_stdlib on runtime_ns: 2.65x (95% CI 2.61-2.72, n=468, p=2.13e-78)
  json_orjson better than json_ujson on runtime_ns: 1.28x (95% CI 1.26-1.30, n=468, p=6.74e-78)
      undecided on count_string (confounded) in [7.937,15.83) -- needs more inputs
      undecided on depth (confounded) in [6.082,9.552) -- needs more inputs
  json_stdlib better than json_simplejson on runtime_ns: 1.33x (95% CI 1.31-1.34, n=468, p=2.13e-78)
      undecided on count_string (confounded) in =0 -- needs more inputs
      undecided on depth (confounded) in =0 -- needs more inputs
  json_ujson better than json_simplejson on runtime_ns: 2.76x (95% CI 2.73-2.78, n=468, p=2.13e-78)
  json_ujson better than json_stdlib on runtime_ns: 2.09x (95% CI 2.08-2.10, n=468, p=2.13e-78)
[compare] memory_peak: 468 inputs, 4 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_string bins move with count_escaped (2..104.5 across bins); count_null (3..9 across bins); depth (1..5.5 across bins) -- those regions are joint, not count_string findings
[compare] count_escaped bins move with count_string (1..30 across bins); count_null (1..5 across bins); depth (1..3 across bins) -- those regions are joint, not count_escaped findings
[compare] count_null bins move with count_string (1..58 across bins); count_escaped (1..101 across bins); depth (1..4 across bins) -- those regions are joint, not count_null findings
[compare] depth bins move with count_string (1..49 across bins); count_escaped (2..99 across bins); count_null (4..13 across bins) -- those regions are joint, not depth findings
  json_simplejson better than json_orjson on memory_peak: 3.59x (95% CI 3.56-3.77, n=468, p=4.18e-77)
  json_stdlib better than json_orjson on memory_peak: 3.75x (95% CI 3.58-3.80, n=468, p=4.18e-77)
  json_ujson better than json_orjson on memory_peak: 1.96x (95% CI 1.95-1.98, n=468, p=1.96e-77)
  json_simplejson and json_stdlib equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=468)
      undecided on count_string (confounded) in [3.979,7.937) -- needs more inputs
      undecided on count_escaped (confounded) in [11.49,25.92), [25.92,58.5) -- needs more inputs
  json_simplejson better than json_ujson on memory_peak: 1.86x (95% CI 1.80-1.92, n=468, p=0.000552)
      DEPENDS ON SAMPLING: counting each count_string bin once gives 0.77x (95% CI 0.73-0.88, 7 bins, equal weight per bin), verdict 'b_faster' not 'a_faster'
      DEPENDS ON SAMPLING: counting each count_escaped bin once gives 0.59x (95% CI 0.52-0.61, 6 bins, equal weight per bin), verdict 'b_faster' not 'a_faster'
      ... and 1 count_escaped bin(s) have too little data to enter that: [2.256,5.092)
      DEPENDS ON SAMPLING: counting each depth bin once gives 0.98x (95% CI 0.95-1.02, 6 bins, equal weight per bin), verdict 'equivalent' not 'a_faster'
      ... and 1 depth bin(s) have too little data to enter that: [9.552,15]
      crossover on count_string (confounded): json_ujson better below 3.979, json_simplejson better above 7.937
      undecided on count_string (confounded) in [3.979,7.937) -- needs more inputs
      crossover on count_escaped (confounded): json_ujson better below 25.92, json_simplejson better above 25.92
      crossover on count_null (confounded): json_ujson better at 0, json_simplejson better above 1.661
      undecided on count_null (confounded) in [1,1.661) -- needs more inputs
      crossover on depth (confounded): json_ujson better below 1.57, json_simplejson better above 1.57
  json_stdlib better than json_ujson on memory_peak: 1.88x (95% CI 1.86-1.96, n=468, p=3.61e-05)
      DEPENDS ON SAMPLING: counting each count_string bin once gives 0.79x (95% CI 0.75-0.94, 7 bins, equal weight per bin), verdict 'undecided' not 'a_faster'
      DEPENDS ON SAMPLING: counting each count_escaped bin once gives 0.61x (95% CI 0.54-0.65, 6 bins, equal weight per bin), verdict 'b_faster' not 'a_faster'
      ... and 1 count_escaped bin(s) have too little data to enter that: [2.256,5.092)
      DEPENDS ON SAMPLING: counting each depth bin once gives 0.99x (95% CI 0.95-1.03, 6 bins, equal weight per bin), verdict 'equivalent' not 'a_faster'
      ... and 1 depth bin(s) have too little data to enter that: [9.552,15]
      crossover on count_string (confounded): json_ujson better below 3.979, json_stdlib better above 3.979
      crossover on count_escaped (confounded): json_ujson better below 11.49, json_stdlib better above 25.92
      undecided on count_escaped (confounded) in [11.49,25.92) -- needs more inputs
      crossover on count_null (confounded): json_ujson better at 0, json_stdlib better above 1.661
      undecided on count_null (confounded) in [1,1.661) -- needs more inputs
      crossover on depth (confounded): json_ujson better below 1.57, json_stdlib better above 1.57
[compare] dominance across runtime_ns, memory_peak:
  json_orjson vs json_simplejson TRADE-OFF: json_orjson better on runtime_ns 3.54x; json_simplejson better on memory_peak 3.59x
  json_orjson vs json_stdlib TRADE-OFF: json_orjson better on runtime_ns 2.65x; json_stdlib better on memory_peak 3.75x
  json_orjson vs json_ujson TRADE-OFF: json_orjson better on runtime_ns 1.28x; json_ujson better on memory_peak 1.96x
  json_stdlib DOMINATES json_simplejson: better on runtime_ns 1.33x; equivalent on memory_peak
  json_simplejson vs json_ujson TRADE-OFF: json_simplejson better on memory_peak 1.86x; json_ujson better on runtime_ns 2.76x
  json_stdlib vs json_ujson TRADE-OFF: json_stdlib better on memory_peak 1.88x; json_ujson better on runtime_ns 2.09x
      count_string =0 (n=32): json_orjson, json_ujson not dominated
      count_string [1,1.995) (n=56): json_orjson, json_ujson not dominated
      count_string [1.995,3.979) (n=32): json_orjson, json_ujson not dominated
      count_string [3.979,7.937) (n=25): json_orjson, json_simplejson, json_stdlib, json_ujson not dominated
      count_string [7.937,15.83) (n=32): json_orjson, json_stdlib, json_ujson not dominated
      count_string [15.83,31.58) (n=185): json_orjson, json_stdlib, json_ujson not dominated
      count_string [31.58,63] (n=106): json_orjson, json_stdlib, json_ujson not dominated
      WARNING json_simplejson is dominated by json_stdlib over the whole corpus but survives in [3.979,7.937) on count_string -- the global verdict is a statement about this corpus's mix, not about the systems
      count_escaped =0 (n=50): json_orjson, json_ujson not dominated
      count_escaped [1,2.256) (n=29): json_orjson, json_ujson not dominated
      count_escaped [5.092,11.49) (n=13): json_orjson, json_ujson not dominated
      count_escaped [11.49,25.92) (n=33): json_orjson, json_stdlib, json_ujson not dominated
      count_escaped [25.92,58.5) (n=19): json_orjson, json_simplejson, json_stdlib, json_ujson not dominated
      count_escaped [58.5,132] (n=323): json_orjson, json_stdlib, json_ujson not dominated
      WARNING json_simplejson is dominated by json_stdlib over the whole corpus but survives in [25.92,58.5) on count_escaped -- the global verdict is a statement about this corpus's mix, not about the systems
      count_null =0 (n=117): json_orjson, json_ujson not dominated
      count_null [1,1.661) (n=42): json_orjson, json_stdlib, json_ujson not dominated
      count_null [1.661,2.759) (n=25): json_orjson, json_stdlib, json_ujson not dominated
      count_null [2.759,4.583) (n=68): json_orjson, json_stdlib, json_ujson not dominated
      count_null [4.583,7.612) (n=134): json_orjson, json_stdlib, json_ujson not dominated
      count_null [7.612,12.64) (n=47): json_orjson, json_stdlib, json_ujson not dominated
      count_null [12.64,21] (n=35): json_orjson, json_stdlib, json_ujson not dominated
      depth =0 (n=51): json_orjson, json_ujson not dominated
      depth [1,1.57) (n=69): json_orjson, json_ujson not dominated
      depth [1.57,2.466) (n=162): json_orjson, json_stdlib, json_ujson not dominated
      depth [2.466,3.873) (n=83): json_orjson, json_stdlib, json_ujson not dominated
      depth [3.873,6.082) (n=77): json_orjson, json_stdlib, json_ujson not dominated
      depth [6.082,9.552) (n=19): json_orjson, json_stdlib, json_ujson not dominated
[interference] 9 property pair(s) tested over 1872 rows; 7 show a dependence
  count_escaped vs runtime_ns changes with count_string: rho by count_string stratum = [+0.44, +0.49, +0.06, -0.09], spread 0.57, p=0.003
  count_escaped vs runtime_ns changes with depth: rho by depth stratum = [+0.52, +0.41, +0.05, +0.00], spread 0.52, p=0.003
  count_string vs runtime_ns changes with count_escaped: rho by count_escaped stratum = [+0.34, +0.59, +0.11, +0.07], spread 0.52, p=0.003
  depth vs runtime_ns changes with count_escaped: rho by count_escaped stratum = [+0.27, +0.47, +0.07, -0.03], spread 0.50, p=0.003
  count_null vs runtime_ns changes with count_string: rho by count_string stratum = [+0.18, +0.46, -0.02, +0.16], spread 0.48, p=0.003
  depth vs runtime_ns changes with count_string: rho by count_string stratum = [+0.27, +0.46, -0.02, +0.12], spread 0.47, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
