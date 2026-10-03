# jpython_tailored

- corpus: 2176 rows, 544 inputs, 4 systems
- elapsed: 3118s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_trav_segment | 1 | 5 | 5 |
| count_wildcard_selector | 0 | 4 | 5 |
| count_member_name_shorthand | 0 | 4 | 5 |
| count_name_char | 8 | 1734 | 214 |
| count_s_segment | 0 | 4 | 5 |
| count_wide_member | 1 | 171 | 58 |
| count_leaf | 1 | 9211 | 203 |
| count_doc_string | 0 | 1744 | 160 |
| count_letter | 0 | 3492 | 217 |
| count_doc_int | 0 | 9211 | 165 |
| count_pos_int | 0 | 920 | 121 |
| count_DIGIT1 | 0 | 1143 | 142 |
| count_DIGIT | 0 | 461 | 88 |
| count_inner_array | 0 | 151 | 56 |
| count_more_leaf | 0 | 9060 | 182 |
| count_inner_object | 0 | 65 | 37 |
| count_wide_more_member | 0 | 170 | 58 |
| doc_depth | 1 | 3 | 3 |
| doc_bytes | 14 | 20386 | 358 |
| query_len | 3 | 16 | 14 |
| n_object_keys | 1 | 307 | 86 |
| max_value_bytes | 1 | 1511 | 129 |

## frontier
[jpython_tailored] grammar frontier (targeting stopped asking here):
  count_trav_segment: pinned at 5 by the LANGUAGE (<s_segment>{..,2}); no input this grammar admits goes further.
  count_wildcard_selector: pinned at 4 by the LANGUAGE (<s_segment>{..,2}); no input this grammar admits goes further.
  count_s_segment: pinned at 4 by the LANGUAGE (<s_segment>{..,2}); no input this grammar admits goes further.
  count_doc_int: pinned at 9211 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_inner_object: pinned at 65 by the SEARCH; 1 escalating request(s) returned nothing further.
  doc_bytes: pinned at 20386 by the SEARCH; 2 escalating request(s) returned nothing further.
  query_len: pinned at 16 by the SEARCH; 2 escalating request(s) returned nothing further.
  max_value_bytes: pinned at 1511 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 544 inputs, 4 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_wildcard_selector bins move with doc_bytes (336..3342 across bins) -- those regions are joint, not count_wildcard_selector findings
[compare] count_s_segment bins move with count_wildcard_selector (1..3 across bins); doc_bytes (161..3357 across bins) -- those regions are joint, not count_s_segment findings
[compare] doc_bytes bins move with max_value_bytes (6..708 across bins) -- those regions are joint, not doc_bytes findings
[compare] max_value_bytes bins move with doc_bytes (18..1.273e+04 across bins) -- those regions are joint, not max_value_bytes findings
  jpython_1_1_0 vs jpython_1_1_1 undecided: jpython_1_1_1 ahead by 1.09x but the 95% CI (0.91-0.92, n=544) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_wildcard_selector bin once gives 0.93x (95% CI 0.92-0.93, 4 bins, equal weight per bin), verdict 'equivalent' not 'undecided'
      ... and 3 count_wildcard_selector bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3.5,4]
      DEPENDS ON SAMPLING: counting each doc_bytes bin once gives 0.92x (95% CI 0.91-0.93, 6 bins, equal weight per bin), verdict 'equivalent' not 'undecided'
      undecided on count_wildcard_selector (confounded) in [1,1.5), [2,2.5) -- needs more inputs
      undecided on count_s_segment (confounded) in =0, [1,1.5), [3,3.5), [3.5,4] -- needs more inputs
      undecided on doc_bytes (confounded) in [158.7,534.2), [534.2,1799) -- needs more inputs
      undecided on max_value_bytes (confounded) in [446.1,1511] -- needs more inputs
  jpython_1_1_2 better than jpython_1_1_0 on runtime_ns: 1.20x (95% CI 1.19-1.22, n=544, p=3.13e-80)
      undecided on count_s_segment (confounded) in [2,2.5) -- needs more inputs
      undecided on max_value_bytes (confounded) in [131.7,446.1) -- needs more inputs
  jpython_1_1_3 better than jpython_1_1_0 on runtime_ns: 1.31x (95% CI 1.29-1.35, n=544, p=6.29e-84)
      undecided on max_value_bytes (confounded) in [131.7,446.1) -- needs more inputs
  jpython_1_1_1 vs jpython_1_1_2 undecided: jpython_1_1_2 ahead by 1.10x but the 95% CI (0.90-0.91, n=544) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_wildcard_selector bin once gives 0.95x (95% CI 0.95-0.96, 4 bins, equal weight per bin), verdict 'equivalent' not 'undecided'
      ... and 3 count_wildcard_selector bin(s) have too little data to enter that: [1.5,2), [2.5,3), [3.5,4]
      undecided on count_wildcard_selector (confounded) in [3,3.5) -- needs more inputs
      undecided on count_s_segment (confounded) in [1,1.5), [3,3.5), [3.5,4] -- needs more inputs
      undecided on doc_bytes (confounded) in [14,47.13), [47.13,158.7), [158.7,534.2), [1799,6055), [6055,2.039e+04] -- needs more inputs
      undecided on max_value_bytes (confounded) in [1,3.387), [11.48,38.87), [38.87,131.7), [131.7,446.1), [446.1,1511] -- needs more inputs
  jpython_1_1_3 better than jpython_1_1_1 on runtime_ns: 1.20x (95% CI 1.19-1.22, n=544, p=3.37e-77)
      undecided on count_s_segment (confounded) in [2,2.5) -- needs more inputs
      undecided on doc_bytes (confounded) in [6055,2.039e+04] -- needs more inputs
      undecided on max_value_bytes (confounded) in [131.7,446.1) -- needs more inputs
  jpython_1_1_2 vs jpython_1_1_3 undecided: jpython_1_1_3 ahead by 1.10x but the 95% CI (0.90-0.92, n=544) spans the equivalence band
      DEPENDS ON SAMPLING: counting each count_s_segment bin once gives 0.88x (95% CI 0.86-0.90, 5 bins, equal weight per bin), verdict 'b_faster' not 'undecided'
      ... and 2 count_s_segment bin(s) have too little data to enter that: [1.5,2), [2.5,3)
      undecided on count_wildcard_selector (confounded) in [2,2.5) -- needs more inputs
      undecided on count_s_segment (confounded) in [1,1.5), [3,3.5), [3.5,4] -- needs more inputs
      undecided on doc_bytes (confounded) in [47.13,158.7), [158.7,534.2), [534.2,1799), [1799,6055), [6055,2.039e+04] -- needs more inputs
      undecided on max_value_bytes (confounded) in [131.7,446.1), [446.1,1511] -- needs more inputs
[interference] 6 property pair(s) tested over 2176 rows; 5 show a dependence
  count_wildcard_selector vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [+0.17, +0.14, +0.65, +0.11], spread 0.54, p=0.003
  doc_bytes vs runtime_ns changes with max_value_bytes: rho by max_value_bytes stratum = [+0.85, +0.79, +0.43, +0.35], spread 0.49, p=0.003
  count_s_segment vs runtime_ns changes with doc_bytes: rho by doc_bytes stratum = [+0.12, +0.05, +0.51, +0.13], spread 0.46, p=0.003
  count_s_segment vs runtime_ns changes with max_value_bytes: rho by max_value_bytes stratum = [-0.25, +0.07, +0.09, +0.15], spread 0.41, p=0.003
  count_wildcard_selector vs runtime_ns changes with max_value_bytes: rho by max_value_bytes stratum = [+0.03, -0.05, +0.26, +0.27], spread 0.32, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
