#!/usr/bin/env bash
# Build one virtualenv per version of the orjson known pair.
#
# example.py reaches each version at envs/<version>/bin/python, so the
# directory names are load-bearing. The interpreter is the one the repo .venv
# was built from (CPython 3.12.1 via pyenv). orjson is one extension module, so the versions cannot share an interpreter.
# Wheels only. The envs are not tracked; each env's `pip freeze` goes to
# freeze/<version>.txt, which is.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-$("$REPO/.venv/bin/python" -c 'import sys; print(sys._base_executable)')}"
VERSIONS=(3.10.1 3.10.2 3.10.3 3.10.4 3.10.5 3.10.6)

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
