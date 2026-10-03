# simplejson_tailored

- corpus: 154 rows, 77 inputs, 2 systems
- elapsed: 3456s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_number | 7 | 958 | 61 |
| count_literal | 7 | 945 | 60 |
| count_false | 2 | 309 | 52 |
| count_true | 2 | 318 | 51 |
| count_null | 2 | 318 | 51 |
| count_string | 6 | 963 | 60 |
| num_pairs | 32 | 2866 | 62 |
| doc_bytes | 430 | 38384 | 75 |
| key_density | 0.0685446 | 0.0782998 | 75 |

## comparison
[compare] runtime_ns: 77 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
  simplejson_3_20_2 and simplejson_4_0_0 equivalent: ratio 0.95x within the equivalence band (95% CI 0.94-0.95, n=77)
[compare] memory_peak: 77 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
  simplejson_3_20_2 and simplejson_4_0_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=77)
[compare] dominance across runtime_ns, memory_peak:
  simplejson_3_20_2 and simplejson_4_0_0 EQUIVALENT on every metric
      num_pairs [32,67.69) (n=11): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [67.69,143.2) (n=10): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [143.2,302.8) (n=12): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [302.8,640.6) (n=9): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [640.6,1355) (n=11): simplejson_3_20_2, simplejson_4_0_0 not dominated
      num_pairs [1355,2866] (n=24): simplejson_3_20_2, simplejson_4_0_0 not dominated
      key_density [0.06854,0.0783] (n=77): simplejson_3_20_2, simplejson_4_0_0 not dominated
[interference] 2 property pair(s) tested over 154 rows; 0 show a dependence
