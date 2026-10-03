# Known performance pairs: Python SUTs (JSON, JSONPath Py)

2026-10-01. Per-commit rows are in `py_<package>.csv` in this directory. The `py_` prefix keeps these files apart from the JavaScript files, which already include an npm `jsonpath-rfc9535.csv`.

## Collection rule (applied identically to all seven packages)

1. Commits on the default branch since 2024-01-01 (`git log --since=2024-01-01`, blobless clone, default branch HEAD on 2026-10-01) whose full message matches, case-insensitive, `perf|performance|speed|faster|slow|optimi[sz]|quadratic|cache|memory|leak|regression`.
2. Changelog or release-note entries since 2024-01-01 matching the same regex. Each entry is mapped to its linked commit or PR. Where the entry links nothing (orjson's CHANGELOG.md), it is mapped to the code commits in that release's tag range; see judgement call 1.
3. Deduplicated by change: a merge commit and the commit it merges count once, recorded under the content commit with the PR number.

Sources: ijl/orjson (master), ultrajson/ultrajson (main, plus GitHub release notes, since the repo keeps no changelog file), simplejson/simplejson (master, CHANGES.txt), h2non/jsonpath-ng (master, CHANGELOG.md and History.md), jg-rp/python-jsonpath (main), jg-rp/python-jsonpath-rfc9535 (main), sean2077/jsonpath-python (main). Release dates are the earliest PyPI upload time. The stdlib `json` module is excluded.

What counts as measured is fixed by the frozen subjects. The json subject times `loads` only: `user_systems.py` runs `K_PARSE=3000` loads per call and never calls `dumps`. Its grammar is RFC 8259 under I-JSON, with integers within ±(2^53-1), at most 17 significant digits, and exponents up to 290. The jsonpath_py subject's `py_runner.py` compiles the query outside the timed region and reports `compile_ns` as an extra column; only evaluation is timed. Its query grammar follows RFC 9535 and its documents follow I-JSON. The recorded metrics are `bench_runner.STANDARD_METRICS` (runtime_ns, tracemalloc_peak, rss, rss_growth, and others).

## Funnel

S1 asks whether the commit is an actual performance change. S2 asks whether its effect depends on the input. S3 classifies the input-dependent changes.

| Domain | Package | Commits since 2024 | Raw keyword hits | Collected (keyword + changelog) | S1 yes | S2 yes | expressible | not_expressible | not_measurable | unclear | Release pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| JSON | orjson | 164 | 3 | 24 (3 + 21) | 22 | 20 | 5 | 0 | 15 | 0 | 3 |
| JSON | ujson | 192 | 7 | 8 (7 + 1) | 4 | 3 | 0 | 1 | 2 | 0 | 0 |
| JSON | simplejson | 54 | 18 | 20 (16 + 4) | 7 | 5 | 1 | 0 | 4 | 0 | 1 |
| JSON | total | 410 | 28 | 52 | 33 | 28 | 6 | 1 | 21 | 0 | 4 |
| JSONPath Py | jsonpath-ng | 56 | 1 | 1 (1 + 0) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| JSONPath Py | python-jsonpath | 208 | 4 | 2 (2 + 0) | 2 | 1 | 1 | 0 | 0 | 0 | 1 |
| JSONPath Py | jsonpath-rfc9535 | 105 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| JSONPath Py | jsonpath-python | 39 | 9 | 9 (9 + 0) | 4 | 3 | 3 | 0 | 0 | 0 | 3 |
| JSONPath Py | total | 408 | 14 | 12 | 6 | 4 | 4 | 0 | 0 | 0 | 4 |
| All | total | 818 | 42 | 64 | 39 | 32 | 10 | 1 | 21 | 0 | 8 |

simplejson's 18 raw hits include three merges, and python-jsonpath's 4 include two. jsonpath-python's changelog entries all link commits that the keyword pass had already found, so the changelog leg added nothing there.

### Where pairs drop out, and why

- **S1, 25 dropped.** These are CI, packaging, test and lint changes (7), release-bookkeeping commits whose long bodies carry keywords (4), correctness and memory-safety fixes with no cost effect (9: simplejson #329, #356, #357, #359, #360, #373, #379; ujson 76f5e55, 95b55fb), no-ops on the measured build (2: simplejson #365 critical sections and #367 free-threading heap types, both compiled out on GIL-enabled CPython 3.12), an encoder feature (simplejson #387), and dependency or vendoring changes (orjson aec6e70, c5af268). simplejson dominates S1 losses because its 4.0.0 PR bodies are long and mention "leak", "cache" and "speedups".
- **S2, 7 dropped.** Build configuration (orjson d55b261, 95c86e5), platform-specific changes (simplejson #339, which only affects GraalPy), import-time initialisation (simplejson #363), a leak on the error path of a failing file write (ujson 82af1d0), an API added in the same release (python-jsonpath #65, the `select()` projection), and compile-instance caching the runner never consults (jsonpath-python fe53dd5).
- **S3, not_measurable, 21.** All 21 are in the JSON domain, and 20 are serialisation (`dumps`). Some are also amd64-only or concern non-JSON types (orjson datetime/UUID, simplejson indent/skipkeys, the ujson default() and encoding leaks). The remaining one is orjson d231af6 (PyMem allocator, 3.10.14): at that version loads parses into a static 8 MiB yyjson pool allocated at import, so no per-call Rust allocations reach tracemalloc. The loads-only decision is the largest single filter in the JSON domain.
- **S3, not_expressible, 1.** ujson 4baeb95 fixes a memory leak when parsing large integers. The leaking branch (`Object_newIntegerFromString`) runs only when a literal overflows 64 bits, and the grammar caps integers at 2^53-1 (deviation 8). If the grammar allowed such integers, the leak would show as rss_growth over K_PARSE loads.
- **jsonpath_py loses nothing at S3.** Every input-dependent JSONPath change in range is on the evaluation path. No collected commit changes only compilation, so `compile_ns` (recorded, not the primary metric) did not have to absorb any.

## Expressible release pairs ready to measure

All wheels exist for CPython 3.12 macOS arm64: orjson and simplejson ship universal2 wheels, and the JSONPath packages are pure Python (`py3-none-any`).

| # | Package | Before | After | Subject | Driving commit(s) | What should move | Confounds in range | Wiring needed |
|---|---|---|---|---|---|---|---|---|
| P1 | orjson | 3.10.1 (2024-04-15) | 3.10.2 (2024-05-01) | json | a1a2ed9 (yyjson population rewrite), fcbd9a4 (key cache 1024 -> 2048) | runtime_ns on every document; the key-cache change matters only for objects with many distinct short names | c89e6d5 changes the Cargo release profile (binary-wide); the other commits are serialisation-only | add 3.10.1 and 3.10.2 to an `orjson_latest`-style `build_envs.sh` (one venv per version, `--only-binary`); `orjson_latest/py_runner.py` works unchanged (stdlib + orjson) |
| P2 | orjson | 3.10.3 (2024-05-03) | 3.10.4 (2024-06-10) | json | c96351f (drops null checks in yyjson population) | runtime_ns on nested containers; expected near the noise floor | d55b261 changes the panic/unwind strategy (binary-wide); Py_MOD_GIL_USED; cargo update | same as P1; the expected result is a null, useful as a negative control |
| P3 | orjson | 3.10.5 (2024-06-13) | 3.10.6 (2024-07-02) | json | c369ea4 (scalar PyUnicode-kind detection rewritten), 9382058 (key hash ahash -> xxh3) | runtime_ns on documents with non-ASCII strings (`<unescaped_nonascii>`) and many member names | 95c86e5 cargo update/build misc | same as P1 |
| P4 | simplejson | 3.20.2 (2025-09-26) | 4.0.0 (2026-04-18) | json | e2e5f0b, #369 (scanner key interning, one `PyDict_SetDefault` probe instead of two) | runtime_ns scaling with member count | large release: array_hook check per array, trailing-comma detection, #364 GetItemWithError, #372/#374 scanstring bounds checks, #367 templated scanner, PEP 517 build, macOS deployment target 10.9 -> 10.13 | new per-version subject mirroring `orjson_latest` with a `simplejson.loads` runner; assert `simplejson._speedups` imports in each env, or the pure-Python decoder gets measured |
| P5 | python-jsonpath | 1.3.2 (2025-08-15) | 2.0.0 (2025-09-09) | jsonpath_py | 7ed181a, #108 (LRU cache for match/search patterns) | evaluation runtime_ns for filters using `match()`/`search()` | 2.0.0 is a rewrite (parser, query model, syntax changes); the delta will mostly be the rewrite | envs per version reusing `jsonpath_py/py_runner.py` engine `pyjsonpath` (the API `jsonpath.compile(...).findall` exists in both). The frozen env has no `regex`/`iregexp-check`, so the cache only replaces `re`'s own cache. Decide whether to add `iregexp-check`, and keep it identical across both envs |
| P6 | jsonpath-python | 1.1.0 (2025-11-23) | 1.1.1 (2025-11-23) | jsonpath_py | 61152d7 (pre-compiled key regex in `_traverse`) | evaluation runtime_ns for `*`, `..` and filters over objects | none in code (CI only) | envs 1.1.0 through 1.1.3 reusing `jsonpath_py/py_runner.py` engine `jpython` (`from jsonpath import JSONPath`; `.parse(doc)` exists in all four); P6-P8 can run as one four-version series |
| P7 | jsonpath-python | 1.1.1 (2025-11-23) | 1.1.2 (2025-11-25) | jsonpath_py | 70b0103 (the eager `logger.debug(f"...{obj}")` per match is now guarded; `_build_path`) | evaluation runtime_ns and tracemalloc_peak, scaling with match count and matched-value size; likely the largest effect in this list | benchmark tooling only | same as P6 |
| P8 | jsonpath-python | 1.1.2 (2025-11-25) | 1.1.3 (2025-11-25) | jsonpath_py | 3054ca4 (`isidentifier()` instead of regex in `_build_path`) | evaluation runtime_ns for object traversal | fe53dd5 (compile cache, not on the runner path), 14f282f | same as P6 |

### Correctness flags (equivalence can break across the pair)

- P6, jsonpath-python 61152d7, adds `k.strip()` to union and field-extractor keys. Unions with blanks after commas, which the grammar generates, may match differently in 1.1.0 and 1.1.1. The same commit moves `subx` from class to instance; this is not hit, because the runner builds one instance per process.
- P5, python-jsonpath 2.0.0, changes syntax and acceptance relative to 1.3.2. Inputs must be re-checked for equal results per pair before a cost delta is attributed.
- P8, jsonpath-python 3054ca4, can change PATH strings for keys where `isalnum()` differs from `\w`. VALUE results, which are what the runner counts, are unaffected.
- Not on a measured pair: ujson 95b55fb rejects non-bytes buffers, and simplejson 0dbb9d8 fixes an `ascii_escape` overflow (dumps only).

## Judgement calls and caveats

1. **orjson changelog mapping.** orjson's commit subjects are terse ("zmij", "writer::num"), so the keyword pass finds 3 commits. Its CHANGELOG.md says "Improve performance" in seven 2024 releases without linking commits. I counted each entry and mapped it to the code commits in that release's tag range, splitting by path (`src/deserialize` versus `src/serialize`). The rule asks for a linked commit, so this is a relaxation. A strict reading would leave orjson with 3 collected, 0 expressible and 0 pairs. P1 and P3 rest on this mapping. P2's commit is a "cargo update, misc" commit, chosen because it is the only loads-side change in a release whose changelog claims a speed-up.
2. **Correctness-only memory fixes count at S1 as "no".** These are simplejson's 4.0.0 "memory safety fixes" bullet, collected via its linked PRs. Leaks are counted as performance changes (S1 yes), because a leak shows up as rss_growth.
3. **Version-gated C code.** simplejson's PyUnicodeWriter scanstring path (#370) compiles only for CPython 3.14 and later. The harness interpreter is CPython 3.12.1 (the repo `.venv`), so I classed it as not reaching loads. If the harness interpreter changes, re-check #370 and #367.
4. **Memory-relevant changes the rule misses** (not collected, listed for completeness):
   - orjson b81459f (3.11.0, "Use dynamic deserialization buffer"): the per-request yyjson buffer is directly on the loads path and should move tracemalloc_peak and runtime. The changelog text has no keyword.
   - jsonpath-python 07e2c11 (1.1.5): replaces `eval()` in filters with a custom evaluator. This is a security fix, likely with a large evaluation-time effect.
   - jsonpath-ng 1.7.0 "Only construct the parse table once": compile time only, so it would be not_measurable via compile_ns.
   - ujson's 6.0.0 decoder refactors.
   A pair on orjson 3.10.18 -> 3.11.0 would be the strongest JSON-domain addition if the rule were widened to "buffer" or "alloc".
5. **Overlap with the preregistered latest series.** P1-P3 do not overlap `orjson_latest` (3.11.5-3.12.0), and P6-P8 do not overlap jsonpath-ng's series. The json subject's repo `.venv` currently pins simplejson 4.1.1 and ujson 5.13.0, while PyPI has 4.1.2 and 6.0.0.
6. **Nothing was measured.** S3 decisions come from reading diffs and source at the release tags. P2 is expected to show no effect, and P5's attribution to the cache commit is weak.
