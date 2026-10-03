# pyjsonpath_tailored

- corpus: 824 rows, 412 inputs, 2 systems
- elapsed: 2757s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_pre_segment | 0 | 1 | 2 |
| count_basic_expr | 1 | 374 | 61 |
| count_match_expr | 0 | 181 | 57 |
| count_value_argument | 1 | 374 | 61 |
| count_iregexp_literal | 1 | 374 | 61 |
| count_ire_alt | 0 | 198 | 54 |
| count_ire_branch | 1 | 572 | 87 |
| count_ire_piece | 1 | 1402 | 138 |
| count_ire_char_class | 0 | 369 | 70 |
| count_ire_char_class_expr | 0 | 183 | 48 |
| count_ire_cce1 | 0 | 385 | 68 |
| count_ire_quantifier | 0 | 689 | 99 |
| count_ire_range_quantifier | 0 | 174 | 55 |
| count_search_expr | 0 | 193 | 57 |
| count_and_tail | 0 | 373 | 61 |
| count_item | 1 | 351 | 83 |
| count_doc_string | 1 | 465 | 95 |
| count_letter | 1 | 14489 | 178 |
| count_wide_more_item | 0 | 350 | 83 |
| doc_depth | 1 | 2 | 2 |
| doc_bytes | 5 | 15903 | 232 |
| query_len | 17 | 9572 | 233 |
| n_doc_nodes | 2 | 692 | 119 |
| n_function_calls | 1 | 374 | 61 |

## frontier
[pyjsonpath_tailored] grammar frontier (targeting stopped asking here):
  count_pre_segment: pinned at 1 by the SEARCH; 2 escalating request(s) returned nothing further.
  count_ire_char_class: pinned at 369 by the NODE BUDGET; <and_tail>{746,895} would need 477,930 nodes against a cap of 30,000.
  count_item: pinned at 351 by the SEARCH; 1 escalating request(s) returned nothing further.
  doc_depth: pinned at 2 by the SEARCH; 2 escalating request(s) returned nothing further.
  n_doc_nodes: pinned at 692 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 412 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_ire_char_class bins move with n_doc_nodes (17..219 across bins) -- those regions are joint, not count_ire_char_class findings
[compare] doc_depth bins move with count_ire_char_class (1..11 across bins); n_doc_nodes (2..50 across bins) -- those regions are joint, not doc_depth findings
[compare] n_doc_nodes bins move with count_ire_char_class (2..17 across bins) -- those regions are joint, not n_doc_nodes findings
  pyjsonpath_2_0_0 better than pyjsonpath_1_3_2 on runtime_ns: 1.16x (95% CI 1.15-1.16, n=412, p=9.01e-18)
      DEPENDS ON SAMPLING: counting each doc_depth bin once gives 0.94x (95% CI 0.91-0.97, 2 bins, equal weight per bin), verdict 'equivalent' not 'b_faster'
      ... and 4 doc_depth bin(s) have too little data to enter that: [1.167,1.333), [1.333,1.5), [1.5,1.667), [1.667,1.833)
      DEPENDS ON SAMPLING: counting each n_doc_nodes bin once gives 0.89x (95% CI 0.87-0.91, 6 bins, equal weight per bin), verdict 'undecided' not 'b_faster'
      undecided on count_ire_char_class (confounded) in =0, [2.678,7.173) -- needs more inputs
      undecided on doc_depth (confounded) in [1,1.167) -- needs more inputs
      undecided on n_doc_nodes (confounded) in [2,5.299), [37.2,98.57), [261.2,692] -- needs more inputs
[interference] 5 property pair(s) tested over 824 rows; 4 show a dependence
  count_pre_segment vs runtime_ns changes with count_ire_char_class: rho by count_ire_char_class stratum = [+0.09, -0.18, -0.46, -0.25], spread 0.56, p=0.003
  count_pre_segment vs runtime_ns changes with n_doc_nodes: rho by n_doc_nodes stratum = [-0.17, -0.10, -0.52, -0.35], spread 0.43, p=0.003
  doc_depth vs runtime_ns changes with count_ire_char_class: rho by count_ire_char_class stratum = [+0.53, +0.45, +0.17, +0.33], spread 0.36, p=0.003
  n_doc_nodes vs runtime_ns changes with count_ire_char_class: rho by count_ire_char_class stratum = [+0.96, +0.84, +0.71, +0.70], spread 0.26, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
