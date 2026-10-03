# sqlformatter_tailored

- corpus: 1074 rows, 537 inputs, 2 systems
- elapsed: 3138s of 3420s budget

## property coverage

| property | min | max | distinct |
|---|---|---|---|
| count_ws | 3 | 2503 | 140 |
| count_columnref | 0 | 655 | 117 |
| count_col_id | 1 | 793 | 126 |
| count_ident_char | 0 | 9690 | 244 |
| count_elem | 1 | 2401 | 96 |
| count_iconst | 0 | 2401 | 110 |
| count_digit | 0 | 7197 | 203 |
| count_more_el | 0 | 2400 | 96 |
| count_ows | 1 | 2505 | 156 |
| count_more_el_bool | 0 | 1250 | 123 |
| sql_bytes | 22 | 15404 | 286 |
| list_items | 1 | 2401 | 96 |

## frontier
[sqlformatter_tailored] grammar frontier (targeting stopped asking here):
  count_col_id: pinned at 793 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_elem: pinned at 2401 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_iconst: pinned at 2401 by the SEARCH; 1 escalating request(s) returned nothing further.
  count_more_el_bool: pinned at 1250 by the SEARCH; 1 escalating request(s) returned nothing further.
  sql_bytes: pinned at 15404 by the SEARCH; 2 escalating request(s) returned nothing further.
## comparison
[compare] runtime_ns: 537 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_col_id bins move with count_ows (6..998 across bins); sql_bytes (64..1.231e+04 across bins) -- those regions are joint, not count_col_id findings
[compare] count_ows bins move with count_col_id (2..561.5 across bins); sql_bytes (29..1.229e+04 across bins) -- those regions are joint, not count_ows findings
[compare] sql_bytes bins move with count_col_id (1..341 across bins); count_ows (8..1012 across bins) -- those regions are joint, not sql_bytes findings
  sql_formatter_15_8_2 and sql_formatter_15_9_0 equivalent: ratio 0.97x within the equivalence band (95% CI 0.97-0.98, n=537)
      DEPENDS ON SAMPLING: counting each count_col_id bin once gives 0.93x (95% CI 0.91-0.94, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      DEPENDS ON SAMPLING: counting each count_ows bin once gives 0.87x (95% CI 0.86-0.90, 6 bins, equal weight per bin), verdict 'b_faster' not 'equivalent'
      DEPENDS ON SAMPLING: counting each sql_bytes bin once gives 0.92x (95% CI 0.90-0.94, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      undecided on count_ows (confounded) in [184.4,679.7) -- needs more inputs
[compare] rss: 537 inputs, 2 systems (paired; ratios, 1.10x equivalence band)
[compare] overall verdicts are weighted by what the corpus contains, which the loop itself shapes; the per-region lines are the portable claim.
[compare] count_col_id bins move with count_ows (6..998 across bins); sql_bytes (64..1.231e+04 across bins) -- those regions are joint, not count_col_id findings
[compare] count_ows bins move with count_col_id (2..561.5 across bins); sql_bytes (29..1.229e+04 across bins) -- those regions are joint, not count_ows findings
[compare] sql_bytes bins move with count_col_id (1..341 across bins); count_ows (8..1012 across bins) -- those regions are joint, not sql_bytes findings
  sql_formatter_15_8_2 and sql_formatter_15_9_0 equivalent: ratio 1.00x within the equivalence band (95% CI 1.00-1.00, n=537)
      DEPENDS ON SAMPLING: counting each count_ows bin once gives 0.90x (95% CI 0.89-0.93, 6 bins, equal weight per bin), verdict 'undecided' not 'equivalent'
      undecided on count_col_id (confounded) in [85.67,260.7) -- needs more inputs
      undecided on count_ows (confounded) in [184.4,679.7) -- needs more inputs
[compare] dominance across runtime_ns, rss:
  sql_formatter_15_8_2 and sql_formatter_15_9_0 EQUIVALENT on every metric
      count_col_id [1,3.042) (n=111): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [3.042,9.256) (n=56): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [9.256,28.16) (n=236): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [28.16,85.67) (n=54): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [85.67,260.7) (n=25): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_col_id [260.7,793] (n=55): sql_formatter_15_9_0 not dominated
      count_ows [1,3.685) (n=31): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [3.685,13.58) (n=56): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [13.58,50.05) (n=303): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [50.05,184.4) (n=47): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [184.4,679.7) (n=40): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      count_ows [679.7,2505] (n=60): sql_formatter_15_9_0 not dominated
      sql_bytes [22,65.56) (n=87): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      sql_bytes [65.56,195.4) (n=63): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      sql_bytes [195.4,582.1) (n=255): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      sql_bytes [582.1,1735) (n=20): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      sql_bytes [1735,5169) (n=22): sql_formatter_15_8_2, sql_formatter_15_9_0 not dominated
      sql_bytes [5169,1.54e+04] (n=90): sql_formatter_15_9_0 not dominated
[interference] 6 property pair(s) tested over 1074 rows; 6 show a dependence
  count_col_id vs runtime_ns changes with sql_bytes: rho by sql_bytes stratum = [-0.45, +0.72, +0.59, +0.26], spread 1.17, p=0.003
  count_ows vs runtime_ns changes with count_col_id: rho by count_col_id stratum = [+0.95, +0.71, +0.25, +0.99], spread 0.73, p=0.003
  count_ows vs runtime_ns changes with sql_bytes: rho by sql_bytes stratum = [+0.93, +0.52, +0.31, +0.98], spread 0.66, p=0.003
  count_col_id vs runtime_ns changes with count_ows: rho by count_ows stratum = [+0.93, +0.71, +0.90, +0.28], spread 0.65, p=0.003
  sql_bytes vs runtime_ns changes with count_ows: rho by count_ows stratum = [+0.97, +0.74, +0.91, +0.41], spread 0.56, p=0.003
  sql_bytes vs runtime_ns changes with count_col_id: rho by count_col_id stratum = [+0.72, +0.81, +0.55, +0.66], spread 0.26, p=0.003
  -> a one-dimensional region on these properties states less than it appears to; they are candidates for a joint request.
