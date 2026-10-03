"""Sub-language check for a tailored grammar (RQ1 tailored setting).

Generates inputs from the tailored grammar, one Fandango run per stratify band
of the subject's example.py, and parses every input with the frozen spec
grammar subjects/jsonpath_py/jsonpath_py.fan; the spec grammar's one `where`
clause (unique_member_names) is checked on the same string. No SUT is run.

    .venv/bin/python subjects/jpython_tailored/check_sublanguage.py <subject> [n]
"""
import importlib, json, sys, time
from pathlib import Path

sys.setrecursionlimit(60000)
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "src"))

from fandango.api import parse
from fandango.evolution.algorithm import Fandango
from core.grammar_emit import rewrite_repetition

SPEC = REPO / "subjects" / "jsonpath_py" / "jsonpath_py.fan"


def unique_names(text):
    ok = [True]
    def hook(pairs):
        keys = [k for k, _ in pairs]
        ok[0] &= len(set(keys)) == len(keys)
        return dict(pairs)
    json.loads(text.partition("\n@@@\n")[2], object_pairs_hook=hook)
    return ok[0]


def generate(fan_text, stratify, per_band):
    specs = [stratify] if isinstance(stratify, dict) else list(stratify or [])
    import itertools
    combos = list(itertools.product(*[[(s["nt"], lo, hi) for lo, hi in s["bands"]]
                                      for s in specs])) or [()]
    out = []
    for combo in combos:
        text = fan_text
        for nt, lo, hi in combo:
            text = rewrite_repetition(text, nt, lo, hi)
        g, c = parse(text, use_stdlib=False)
        t0 = time.time()
        sols = Fandango(g, c, population_size=20, best_effort=True,
                        max_nodes=800).evolve(desired_solutions=per_band,
                                              max_generations=40)
        print(f"  band {combo}: {len(sols)} inputs in {time.time()-t0:.1f}s",
              flush=True)
        out += [str(s) for s in sols[:per_band]]
    return out


def main():
    subject = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    ex = importlib.import_module(f"subjects.{subject}.example")
    fan = Path(ex.FAN).read_text()
    stratify = getattr(ex, "STRATIFY", None)
    nb = 1
    for s in ([stratify] if isinstance(stratify, dict) else (stratify or [])):
        nb *= len(s["bands"])
    inputs = generate(fan, stratify, max(1, -(-n // nb)))
    spec_g, _ = parse(SPEC.read_text(), use_stdlib=False)
    bad = 0
    for s in inputs:
        t0 = time.time()
        tree = spec_g.parse(s)
        ok = tree is not None and unique_names(s)
        bad += not ok
        q, _, d = s.partition("\n@@@\n")
        print(f"{'OK ' if ok else 'BAD'} parse={time.time()-t0:5.1f}s "
              f"query={q!r} doc_bytes={len(d)} "
              f"root_keys={len(json.loads(d)) if isinstance(json.loads(d), dict) else 0}",
              flush=True)
    print(f"{len(inputs) - bad}/{len(inputs)} inputs parse under {SPEC.name} "
          f"and satisfy unique_member_names")
    return inputs


if __name__ == "__main__":
    main()
