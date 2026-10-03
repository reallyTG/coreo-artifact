#!/usr/bin/env bash
# Build one virtualenv per preregistered orjson release (the last six
# non-prerelease versions, eval/latest_series_2026-09-30.json).
#
# orjson is one extension module named `orjson`, so the six versions cannot
# share an interpreter; each gets envs/<version>/ and example.py reaches it at
# envs/<version>/bin/python, so the directory names are load-bearing.
#
# The interpreter is the one the repo .venv was built from (CPython 3.12.1 via
# pyenv), so the six differ from each other and from subjects/json only in the
# orjson build. Wheels only: a source build would need a Rust toolchain and
# would not be the artifact users install. The envs are not tracked; each
# env's `pip freeze` is written to freeze/<version>.txt, which is.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-$("$REPO/.venv/bin/python" -c 'import sys; print(sys._base_executable)')}"
VERSIONS=(3.11.5 3.11.6 3.11.7 3.11.8 3.11.9 3.12.0)

mkdir -p "$HERE/freeze"
for v in "${VERSIONS[@]}"; do
    dir="$HERE/envs/$v"
    echo "==> orjson $v"
    rm -rf "$dir"
    "$PYTHON" -m venv "$dir"
    "$dir/bin/python" -m pip install --quiet --upgrade pip
    "$dir/bin/python" -m pip install --quiet --only-binary=:all: "orjson==$v"
    "$dir/bin/python" -m pip freeze --all > "$HERE/freeze/$v.txt"
done

echo
echo "built:"
for v in "${VERSIONS[@]}"; do
    printf '  %-8s %s\n' "$v" "$(grep -v '^pip=\|^setuptools=' "$HERE/freeze/$v.txt" | tr '\n' ' ')"
done
