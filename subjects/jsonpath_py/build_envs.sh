#!/usr/bin/env bash
# Build the four per-engine virtualenvs this subject measures.
#
# Each library gets its own env because several of them install modules under
# colliding names, so one env holding all four would not be measuring four
# independent implementations. `example.py` reaches each engine at
# envs/<name>/bin/python, so the directory names here are load-bearing.
#
# The envs are ~68MB of platform binaries and are not tracked. This script
# reproduces them.
#
# Versions are pinned to what the recorded measurements were taken against.
# Changing one changes the subject.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

build() {
    local name="$1"; shift
    local dir="$HERE/envs/$name"
    echo "==> $name: $*"
    rm -rf "$dir"
    "$PYTHON" -m venv "$dir"
    "$dir/bin/python" -m pip install --quiet --upgrade pip
    "$dir/bin/python" -m pip install --quiet "$@"
}

build jpython    'jsonpath-python==1.1.6'
build ng         'jsonpath-ng==1.8.0' 'jsonpath-rfc9535==1.0.0' \
                 'iregexp-check==0.1.4' 'regex==2026.9.10'
build pyjsonpath 'python-jsonpath==2.2.1'
build rfc9535    'jsonpath-rfc9535==1.0.0' 'iregexp-check==0.1.4' \
                 'regex==2026.9.10'

echo
echo "built:"
for e in jpython ng pyjsonpath rfc9535; do
    printf '  %-12s %s\n' "$e" \
        "$("$HERE/envs/$e/bin/python" -m pip freeze | grep -v '^pip\|^setuptools' | tr '\n' ' ')"
done
