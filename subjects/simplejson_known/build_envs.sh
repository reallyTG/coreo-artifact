#!/usr/bin/env bash
# Build one virtualenv per version of the simplejson known pair.
#
# example.py reaches each version at envs/<version>/bin/python, so the
# directory names are load-bearing. The interpreter is the one the repo .venv
# was built from (CPython 3.12.1 via pyenv). Both releases must ship the C extension simplejson._speedups as a binary wheel for this interpreter; otherwise the pair compares C against pure Python.
# Wheels only. The envs are not tracked; each env's `pip freeze` goes to
# freeze/<version>.txt, which is.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-$("$REPO/.venv/bin/python" -c 'import sys; print(sys._base_executable)')}"
VERSIONS=(3.20.2 4.0.0)

mkdir -p "$HERE/freeze"
for v in "${VERSIONS[@]}"; do
    dir="$HERE/envs/$v"
    echo "==> simplejson $v"
    rm -rf "$dir"
    "$PYTHON" -m venv "$dir"
    "$dir/bin/python" -m pip install --quiet --upgrade pip
    "$dir/bin/python" -m pip install --quiet --only-binary=:all: "simplejson==$v"
    "$dir/bin/python" -m pip freeze --all > "$HERE/freeze/$v.txt"
done

echo
echo "built:"
for v in "${VERSIONS[@]}"; do
    printf '  %-8s %s\n' "$v" "$(grep -v '^pip=\|^setuptools=' "$HERE/freeze/$v.txt" | tr '\n' ' ')"
done
