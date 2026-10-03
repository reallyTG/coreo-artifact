# Subjects

One directory per subject. Each holds a grammar (`.fan`), the systems under
test, property functions (`user_def_functions.py`), and `example.py`, whose
docstring explains the subject in full. `_template/` is the skeleton to copy.
This file is generated from `src/core/manifest.py`.

## Mined known pairs, blind grammar

Version pairs mined from each library's history. The grammar is the domain's specification grammar, written before the diffs were read.

| Subject | What it compares | Systems | Setup |
|---|---|---|---|
| `css_select_known` (JavaScript) | css-select 5.1.0 and 5.2.0: a known-pair subject. | `css_select_5_1_0`, `css_select_5_2_0` | Node; `npm install` in `subjects/css_select_known/` |
| `domselector_known` (JavaScript) | @asamuzakjp/dom-selector 8.2.4 to 9.2.2: a known-pair subject. | 9 releases, `domselector_8_2_4` to `domselector_9_2_2` | Node; `npm install` in `subjects/domselector_known/` |
| `jpython_known` (Python) | jsonpath-python 1.1.0 to 1.1.3: a known-pair subject in the jsonpath_py domain. | 4 releases, `jpython_1_1_0` to `jpython_1_1_3` | `bash subjects/jpython_known/build_envs.sh` |
| `nwsapi_known` (JavaScript) | nwsapi 2.2.21 to 2.2.27: a known-pair subject. | 7 releases, `nwsapi_2_2_21` to `nwsapi_2_2_27` | Node; `npm install` in `subjects/nwsapi_known/` |
| `orjson_known` (Python) | orjson 3.10.1 to 3.10.6: a known-pair subject in the json domain. | 6 releases, `orjson_3_10_1` to `orjson_3_10_6` | `bash subjects/orjson_known/build_envs.sh` |
| `pyjsonpath_known` (Python) | python-jsonpath 1.3.2 vs 2.0.0: a known-pair subject in the jsonpath_py domain. | `pyjsonpath_1_3_2`, `pyjsonpath_2_0_0` | `bash subjects/pyjsonpath_known/build_envs.sh` |
| `simplejson_known` (Python) | simplejson 3.20.2 vs 4.0.0: a known-pair subject in the json domain. | `simplejson_3_20_2`, `simplejson_4_0_0` | `bash subjects/simplejson_known/build_envs.sh` |
| `sqlcst_known` (JavaScript) | sql-parser-cst 0.21.2 and 0.22.0: a known-pair subject. | `sqlcst_0_21_2`, `sqlcst_0_22_0` | Node; `npm install` in `subjects/sqlcst_known/` |

## Mined known pairs, tailored grammar

The same pairs on grammars shaped by reading the diff.

| Subject | What it compares | Systems | Setup |
|---|---|---|---|
| `cssselect_tailored` (JavaScript) | css-select 5.1.0 and 5.2.0 on a grammar tailored to the commit's diff (RQ1, tailored setting). | `css_select_5_1_0`, `css_select_5_2_0` | Node; `npm install` in `subjects/cssselect_tailored/` |
| `domselector_tailored` (JavaScript) | @asamuzakjp/dom-selector 8.2.4 to 9.2.2 on a grammar tailored to the commits' diffs (RQ1, tailored setting). | 9 releases, `domselector_8_2_4` to `domselector_9_2_2` | Node; `npm install` in `subjects/domselector_tailored/` |
| `jpython_tailored` (Python) | jsonpath-python 1.1.0 to 1.1.3 on a grammar tailored to the commits' diffs (RQ1, tailored setting). | 4 releases, `jpython_1_1_0` to `jpython_1_1_3` | the setup of `jpython_known`, `jsonpath_py` |
| `nwsapi_tailored` (JavaScript) | nwsapi 2.2.21 to 2.2.27 on a grammar tailored to the commits' diffs (RQ1, tailored setting). | 7 releases, `nwsapi_2_2_21` to `nwsapi_2_2_27` | Node; `npm install` in `subjects/nwsapi_tailored/` |
| `orjson_tailored` (Python) | orjson 3.10.1 to 3.10.6 on a grammar tailored to the commits' diffs (RQ1, tailored setting). | 6 releases, `orjson_3_10_1` to `orjson_3_10_6` | the setup of `orjson_known` |
| `pyjsonpath_tailored` (Python) | python-jsonpath 1.3.2 and 2.0.0 on a grammar tailored to the commit's diff (RQ1, tailored setting). | `pyjsonpath_1_3_2`, `pyjsonpath_2_0_0` | the setup of `jsonpath_py`, `pyjsonpath_known` |
| `simplejson_tailored` (Python) | simplejson 3.20.2 and 4.0.0 on a grammar tailored to the commit's diff (RQ1, tailored setting). | `simplejson_3_20_2`, `simplejson_4_0_0` | the setup of `simplejson_known` |
| `sqlformatter_tailored` (JavaScript) | sql-formatter 15.8.2 and 15.9.0 on a grammar tailored to the commit's diff (RQ1, tailored setting). | `sql_formatter_15_8_2`, `sql_formatter_15_9_0` | the setup of `sql_formatter_latest`, `sql_js` |

## Latest release series

The most recent releases of one library per domain, with no known answer.

| Subject | What it compares | Systems | Setup |
|---|---|---|---|
| `css_select_latest` (JavaScript) | css-select, last six releases: a latest-release-series subject. | 5 releases, `css_select_5_1_0` to `css_select_7_0_0` | Node; `npm install` in `subjects/css_select_latest/` |
| `jsonpath_ng_latest` (Python) | jsonpath-ng, last six releases: a latest-release-series subject. | 6 releases, `jsonpath_ng_1_5_2` to `jsonpath_ng_1_8_0` | `bash subjects/jsonpath_ng_latest/build_envs.sh` |
| `jsonpath_plus_latest` (JavaScript) | jsonpath-plus, last six releases: a latest-release-series subject. | 6 releases, `jsonpath_plus_10_2_0` to `jsonpath_plus_11_1_0` | Node; `npm install` in `subjects/jsonpath_plus_latest/` |
| `orjson_latest` (Python) | orjson, last six releases: a latest-release-series subject. | 6 releases, `orjson_3_11_5` to `orjson_3_12_0` | `bash subjects/orjson_latest/build_envs.sh` |
| `sql_formatter_latest` (JavaScript) | sql-formatter, last six releases: a latest-release-series subject. | 6 releases, `sql_formatter_15_7_3` to `sql_formatter_15_9_0` | Node; `npm install` in `subjects/sql_formatter_latest/` |

## Competing implementations

Independent implementations of one specification, compared head to head.

| Subject | What it compares | Systems | Setup |
|---|---|---|---|
| `json` (Python) | JSON parsing: four Python implementations. | `json_orjson`, `json_ujson`, `json_stdlib`, `json_simplejson` | none beyond `requirements.txt` |
| `jsonpath_js` (JavaScript) | JSONPath evaluation: five independent JavaScript implementations. | `dchester`, `jsonpathly`, `p3`, `plus`, `rfc9535` | Node; `npm install` in `subjects/jsonpath_js/` |
| `jsonpath_py` (Python) | JSONPath evaluation: four independent Python implementations. | `ng`, `jpython`, `pyjsonpath`, `rfc9535` | `bash subjects/jsonpath_py/build_envs.sh` |
| `selectors_js` (JavaScript) | CSS selector matching: three JavaScript selector engines over one document. | `nwsapi`, `nwsapi_prev`, `cssselect`, `domselector` | Node; `npm install` in `subjects/selectors_js/` |
| `sql_js` (JavaScript) | SQL parsing: three JavaScript parsers over one PostgreSQL statement. | `pgsql`, `formatter`, `cst` | Node; `npm install` in `subjects/sql_js/` |
