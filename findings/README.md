# Findings

Bugs found while building and running Coreógrafa subjects. Each finding has
its own directory holding a proof of concept (`poc.js` or `poc.py`), a
`package.json` or `requirements.txt` that pins the affected version, and a
`README.md` giving the mechanism, the measurements, and a suggested fix.

| Directory | Contents |
|---|---|
| `fixed/` | Findings since fixed upstream |
| `candidates/` | Findings from the latest-series and head-to-head runs, one directory each, not yet reported |
| top level | Further findings from the head-to-head subjects, not yet reported |

Run one with:

```bash
cd <finding> && npm install && node poc.js          # JavaScript findings
cd <finding> && python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python poc.py   # Python findings
```

## Why each one is a defect

Each finding names a sibling implementation of the same specification, in the
same language, that handles the triggering input correctly and in linear time.
The cost or failure therefore belongs to the implementation and not to the
query or the document. Each performance PoC prints the sibling's time next to
the affected package's.

## Anonymization

How and when each finding reached its maintainers is left out, since it
would identify the authors.

## Withheld pending disclosure

The following superlinear-cost findings have no public fix yet. Their
proofs of concept are denial-of-service inputs, so the directories are
left out of this public copy and will be added as each is fixed
upstream. The paper's bug table describes each defect.

- `jsonpath-quadratic-partials`
- `jsonpath-plus-nested-filter-regex-quadratic`
- `jsonpathly-nested-parens-quadratic` (the parser that is exponential in filter nesting depth)
- `css-select-has-nested-matching-ancestors`
- `jsonpath-rfc9535-py-root-query-in-filter-quadratic`
- `sql-formatter-nested-parens-inline-retry`
