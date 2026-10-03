#!/usr/bin/env bash
# Build one virtualenv per preregistered jsonpath-ng release (the last six
# non-prerelease versions, eval/latest_series_2026-09-30.json).
#
# example.py reaches each version at envs/<version>/bin/python, so the
# directory names are load-bearing. The interpreter is the one the repo .venv
# was built from (CPython 3.12.1 via pyenv), the same as subjects/jsonpath_py.
# Each env holds jsonpath-ng and whatever that release itself requires
# (1.5.x: ply, decorator, six; 1.6.x and 1.7.0: ply; 1.8.0 vendors ply and
# needs nothing). subjects/jsonpath_py's ng env also carries
# jsonpath-rfc9535, iregexp-check and regex, which jsonpath_ng never imports,
# so they are left out here. Wheels only. The envs are not tracked; each env's
# `pip freeze` goes to freeze/<version>.txt, which is.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-$("$REPO/.venv/bin/python" -c 'import sys; print(sys._base_executable)')}"
VERSIONS=(1.5.2 1.5.3 1.6.0 1.6.1 1.7.0 1.8.0)

mkdir -p "$HERE/freeze"
for v in "${VERSIONS[@]}"; do
    dir="$HERE/envs/$v"
    echo "==> jsonpath-ng $v"
    rm -rf "$dir"
    "$PYTHON" -m venv "$dir"
    "$dir/bin/python" -m pip install --quiet --upgrade pip
    "$dir/bin/python" -m pip install --quiet --only-binary=:all: "jsonpath-ng==$v"
    "$dir/bin/python" -m pip freeze --all > "$HERE/freeze/$v.txt"
done

echo
echo "built:"
for v in "${VERSIONS[@]}"; do
    printf '  %-8s %s\n' "$v" "$(grep -v '^pip=\|^setuptools=' "$HERE/freeze/$v.txt" | tr '\n' ' ')"
done
