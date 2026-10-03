#!/usr/bin/env bash
# Resource-bounded launcher for Coreografa on a shared server.
#
#   ./run_safe.sh <subject> [--quick] [--seed=N] [more run.py args]
#
# Why this exists: src/core/fuzzer.py:collect_metrics() calls the system under
# test with no timeout and no memory limit, on randomly generated input. A
# single unlucky input can consume far more than a typical one -- an observed
# `sql` full run peaked at 12.8 GB / 9 min, while other runs of the same
# command finished in 4 s / 240 MB. These caps bound the blast radius.
#
# Override any of these inline, e.g.  MEM_MAX=16G ./run_safe.sh sql
set -euo pipefail

MEM_MAX="${MEM_MAX:-8G}"        # hard ceiling; process is OOM-killed above this
CPU_QUOTA="${CPU_QUOTA:-100%}"  # 100% = one core. The pipeline is single-threaded.
TIME_LIMIT="${TIME_LIMIT:-1800}" # wall-clock seconds before SIGTERM
NICE="${NICE:-10}"              # yield to interactive work by other users

cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { echo "No venv: see Environment in RUNNING.md (python3.12 -m venv .venv)" >&2; exit 1; }

# run.py itself pins numpy's BLAS to one thread, so no thread env vars here.

echo "[run_safe] mem<=$MEM_MAX cpu<=$CPU_QUOTA wall<=${TIME_LIMIT}s nice=$NICE :: run.py $*" >&2

exec systemd-run --user --scope --quiet \
    -p MemoryMax="$MEM_MAX" -p CPUQuota="$CPU_QUOTA" \
    nice -n "$NICE" timeout --signal=TERM --kill-after=30 "$TIME_LIMIT" \
    .venv/bin/python run.py "$@"
