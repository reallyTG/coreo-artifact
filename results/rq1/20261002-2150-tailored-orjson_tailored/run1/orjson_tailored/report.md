# orjson_tailored

- corpus: 2424 rows, 404 inputs, 6 systems
- elapsed: 3461s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_key_ascii | 0 | 1010 | 109 |
| count_key_latin1 | 0 | 973 | 105 |
| count_literal | 0 | 711 | 91 |
| count_null | 0 | 244 | 60 |
| count_true | 0 | 239 | 63 |
| count_false | 0 | 228 | 63 |
| count_number | 0 | 657 | 96 |
| count_string | 0 | 658 | 93 |
| count_str_one_wide | 0 | 213 | 66 |
| count_ascii_run | 0 | 426 | 66 |
| count_str_ascii | 0 | 238 | 66 |
| count_str_latin1 | 0 | 217 | 64 |
| num_pairs | 2 | 1987 | 112 |
| doc_bytes | 19 | 31348 | 296 |
| key_density | 0.0553191 | 0.105263 | 297 |
| latin1_char_share | 0 | 1 | 205 |

## frontier
[orjson_tailored] grammar frontier (targeting stopped asking here):
  doc_bytes: pinned at 31348 by the SEARCH; 2 escalating request(s) returned nothing further.
  latin1_char_share: pinned at 1 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 404 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] latin1_char_share bins move with doc_bytes (48..1009 across bins) -- those regions are joint, not latin1_char_share findings
  orjson_3_10_1 and orjson_3_10_2 equivalent: ratio 0.94x within the equivalence band (95% CI 0.94-0.95, n=404)
      undecided on doc_bytes in [2653,9119), [9119,3.135e+04] -- needs more inputs
  orjson_3_10_1 and orjson_3_10_3 equivalent: ratio 0.94x within the equivalence band (95% CI 0.93-0.95, n=404)
      undecided on doc_bytes in [2653,9119), [9119,3.135e+04] -- needs more inputs
  orjson_3_10_1 and orjson_3_10_4 equivalent: ratio 0.94x within the equivalence band (95% CI 0.93-0.94, n=404)
      undecided on doc_bytes in [2653,9119), [9119,3.135e+04] -- needs more inputs
  orjson_3_10_1 and orjson_3_10_5 equivalent: ratio 0.94x within the equivalence band (95% CI 0.93-0.94, n=404)
      undecided on doc_bytes in [2653,9119) -- needs more inputs
  orjson_3_10_1 vs orjson_3_10_6 undecided: orjson_3_10_6 ahead by 1.10x but the 95% CI (0.90-0.91, n=404) spans the equivalence band
      DEPENDS ON SAMPLING: counting each latin1_char_share bin once gives 0.92x (95% CI 0.91-0.93, 3 bins, equal weight per bin), verdict 'equivalent' not 'undecided'
      ... and 4 latin1_char_share bin(s) have too little data to enter that: =0, [0.5833,0.6667), [0.6667,0.75), [0.75,0.8333)
      undecided on doc_bytes in [224.5,771.8) -- needs more inputs
      undecided on key_density in [0.05532,0.1053] -- needs more inputs
      undecided on latin1_char_share (confounded) in [0.8333,0.9167), [0.9167,1] -- needs more inputs
  orjson_3_10_2 and orjson_3_10_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_4 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_5 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_6 equivalent: ratio 0.96x within the equivalence band (95% CI 0.96-0.97, n=404)
  orjson_3_10_3 and orjson_3_10_4 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=404)
  orjson_3_10_3 and orjson_3_10_5 equivalent: ratio 0.99x within the equivalence band (95% CI 0.99-1.00, n=404)
  orjson_3_10_3 and orjson_3_10_6 equivalent: ratio 0.97x within the equivalence band (95% CI 0.96-0.97, n=404)
  orjson_3_10_4 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_4 and orjson_3_10_6 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.97, n=404)
  orjson_3_10_5 and orjson_3_10_6 equivalent: ratio 0.97x within the equivalence band (95% CI 0.96-0.97, n=404)
[compare] memory_peak: 404 inputs, 6 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] latin1_char_share bins move with doc_bytes (48..1009 across bins) -- those regions are joint, not latin1_char_share findings
  orjson_3_10_1 and orjson_3_10_2 equivalent: ratio 0.98x within the equivalence band (95% CI 0.97-1.00, n=404)
      undecided on doc_bytes in [2653,9119) -- needs more inputs
  orjson_3_10_1 and orjson_3_10_3 equivalent: ratio 0.99x within the equivalence band (95% CI 0.98-1.00, n=404)
  orjson_3_10_1 and orjson_3_10_4 equivalent: ratio 0.98x within the equivalence band (95% CI 0.97-1.00, n=404)
      undecided on doc_bytes in [2653,9119) -- needs more inputs
  orjson_3_10_1 and orjson_3_10_5 equivalent: ratio 0.98x within the equivalence band (95% CI 0.97-1.00, n=404)
  orjson_3_10_1 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 0.98-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_3 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_2 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_3 and orjson_3_10_4 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_3 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_3 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_4 and orjson_3_10_5 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_4 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
  orjson_3_10_5 and orjson_3_10_6 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=404)
[compare] dominance across runtime_ns, memory_peak:
  orjson_3_10_1 and orjson_3_10_2 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_3 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_4 EQUIVALENT on every metric
  orjson_3_10_1 and orjson_3_10_5 EQUIVALENT on every metric
  orjson_3_10_1 vs orjson_3_10_6 undecided on every metric
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
      doc_bytes [19,65.31) (n=57): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      doc_bytes [65.31,224.5) (n=24): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      doc_bytes [224.5,771.8) (n=126): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      doc_bytes [771.8,2653) (n=121): orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      doc_bytes [2653,9119) (n=46): orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      doc_bytes [9119,3.135e+04] (n=30): orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      key_density [0.05532,0.1053] (n=404): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      latin1_char_share [0.5,0.5833) (n=15): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      latin1_char_share [0.8333,0.9167) (n=48): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
      latin1_char_share [0.9167,1] (n=336): orjson_3_10_1, orjson_3_10_2, orjson_3_10_3, orjson_3_10_4, orjson_3_10_5, orjson_3_10_6 not dominated
[interference] 6 property pair(s) tested over 2424 rows; 4 show a dependence
  key_density vs runtime_ns changes with latin1_char_share: rho by latin1_char_share stratum = [-0.26, -0.04, -0.19, -0.76], spread 0.72, p=0.003
  key_density vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [-0.67, -0.48, -0.13, +0.02], spread 0.69, p=0.003
  latin1_char_share vs runtime_ns changes with key_density: rho by key_density stratum = [+0.13, -0.07, -0.12, -0.55], spread 0.68, p=0.003
  latin1_char_share vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [-0.04, -0.01, +0.24, -0.24], spread 0.48, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
