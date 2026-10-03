// Coreografa measurement runner for Node.js.
//
// The JavaScript counterpart of core/bench_runner.py. A subject's runner
// requires this, builds a zero-argument closure over its parsed input, and
// calls report() — which runs the closure K times and prints the one
// `key=value` line that core/subprocess_sut.py scrapes off stdout.
//
// Invoked as:  node <subject-runner>.js <input-file> <k> [extra args...]
//
// The K loop lives here rather than in the framework because a leak only
// accumulates within a single process, so the repetition has to happen inside
// one interpreter. Everything around the loop is generic.
//
// process.resourceUsage() maps almost 1:1 onto getrusage(2), so Node reaches
// every metric the Python runner emits except tracemalloc_peak, which is a
// CPython-level counter with no JS equivalent. heap_peak is reported in its
// place: the high-water mark of V8 heapUsed across the K calls.

'use strict';

const fs = require('fs');

function slope(ys) {
  // Least-squares slope of ys against index 0..n-1 (0 if fewer than 2 points).
  const n = ys.length;
  if (n < 2) return 0;
  const xbar = (n - 1) / 2;
  const ybar = ys.reduce((a, b) => a + b, 0) / n;
  let num = 0;
  let den = 0;
  for (let i = 0; i < n; i++) {
    num += (i - xbar) * (ys[i] - ybar);
    den += (i - xbar) ** 2;
  }
  return den === 0 ? 0 : num / den;
}

function median(xs) {
  const s = [...xs].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function pstdev(xs) {
  if (xs.length < 2) return 0;
  const mean = xs.reduce((a, b) => a + b, 0) / xs.length;
  return Math.sqrt(xs.reduce((a, x) => a + (x - mean) ** 2, 0) / xs.length);
}

/**
 * Run `callableOnce` k times after `warmup` discarded calls, and return the
 * metrics dict. The return value of the callable is ignored; it exists purely
 * to be measured.
 */
function run(callableOnce, k = 1, warmup = 1) {
  for (let i = 0; i < warmup; i++) callableOnce();

  // Baseline the counters *after* warm-up so deltas cover only the K measured
  // calls, not module load and first-call initialisation.
  const ru0 = process.resourceUsage();
  const times = [];
  const rssTrace = [];
  let heapPeak = 0;

  for (let i = 0; i < k; i++) {
    const t = process.hrtime.bigint();
    callableOnce();
    times.push(Number(process.hrtime.bigint() - t));
    const mem = process.memoryUsage();
    rssTrace.push(mem.rss);
    if (mem.heapUsed > heapPeak) heapPeak = mem.heapUsed;
  }
  const ru1 = process.resourceUsage();

  return {
    runtime_ns: median(times),
    runtime_spread_ns: pstdev(times),
    heap_peak: heapPeak,
    rss: rssTrace[rssTrace.length - 1],
    rss_growth: rssTrace[rssTrace.length - 1] - rssTrace[0],
    rss_slope: slope(rssTrace),
    // resourceUsage reports CPU time in microseconds.
    utime_ns: Math.round((ru1.userCPUTime - ru0.userCPUTime) * 1e3),
    stime_ns: Math.round((ru1.systemCPUTime - ru0.systemCPUTime) * 1e3),
    minflt: ru1.minorPageFault - ru0.minorPageFault,
    majflt: ru1.majorPageFault - ru0.majorPageFault,
  };
}

/** Measure and print the standard `key=value` line on stdout. */
function report(callableOnce, k = 1, warmup = 1, extraFn = null) {
  const metrics = run(callableOnce, k, warmup);
  if (extraFn) Object.assign(metrics, extraFn());
  console.log(Object.entries(metrics).map(([key, val]) => `${key}=${val}`).join(' '));
  return metrics;
}

/**
 * Standard argv handling for a subject runner: returns the input file's text
 * and K. Every runner is invoked the same way, so this keeps that contract in
 * one place.
 */
function inputAndK(argv = process.argv) {
  const path = argv[2];
  const k = parseInt(argv[3] || '1', 10);
  return { text: fs.readFileSync(path, 'utf8'), k, rest: argv.slice(4) };
}

module.exports = { run, report, inputAndK, slope, median, pstdev };
