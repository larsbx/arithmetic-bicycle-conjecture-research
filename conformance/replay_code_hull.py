"""Source-pinned finite checks of the code-hull quotient and tower squares."""

import argparse
from collections import defaultdict
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.realization_dependence import canonical, literal_code_hull, require
from kernel.arithmetic_matroid import IntegralRealization
from kernel.code_hull import CodeHull, matvec, reduction, scaled_inflation
from oracles.arithmetic_matroid import lattice_bicycles

FIXTURE = "conformance/fixtures/code-hull-tower-v1.json"
RECEIPT = ROOT / "conformance/receipts/code-hull-tower-v1.json"
SOURCES = (
    FIXTURE, "conformance/fixtures/realization-dependence-v1.json",
    "kernel/code_hull.py", "conformance/replay_code_hull.py",
    "conformance/test_code_hull.py", "proof/code-hull-tower.md",
    "experiments/realization_dependence.py", "kernel/arithmetic_matroid.py",
    "kernel/regular_bicycle.py", "kernel/graph_bicycle.py",
    "oracles/arithmetic_matroid.py", "oracles/regular_snf.py", "oracles/graph_snf.py",
)


def add(a, b, n):
    return tuple((x + y) % n for x, y in zip(a, b))


def verify_level(h, essential=False):
    code, dual, hull = literal_code_hull(h.rows, h.n, h.columns)
    cycle = {x for x in product(range(h.n), repeat=h.columns)
             if not any(matvec(h.rows, x, h.n))}
    require(dual == cycle, "literal dual differs from cycle kernel")
    require(h.hull == hull == lattice_bicycles(h.rows, h.n, h.columns),
            "quotient, literal hull and independent lattice oracle disagree")
    if essential:
        require(h.hull == IntegralRealization(h.rows, h.columns).bicycles(h.n),
                "existing potential route disagrees")
    fibers = defaultdict(set)
    for y in h.gram_kernel:
        fibers[h.cut(y)].add(y)
    require(h.cut_kernel <= h.gram_kernel, "kernel inclusion fails")
    require(len(h.classes) == len(hull), "quotient has wrong size")
    for y in h.gram_kernel:
        coset = {add(y, z, h.n) for z in h.cut_kernel}
        require(coset == fibers[h.cut(y)], "fiber is not the full kernel coset")
        require(h.lift(h.project(y)) == h.class_of(y), "inverse on quotient fails")
        require(h.class_of(tuple(v + h.n for v in y)) == h.class_of(y),
                "integer lift dependence")
    for x in hull:
        require(h.project(h.lift(x)) == x, "inverse on hull fails")
    for y, z in product(h.classes, repeat=2):
        require(h.project(h.class_of(add(y, z, h.n))) == add(h.project(y), h.project(z), h.n),
                "quotient addition fails")
    for y in h.classes:
        for a in range(h.n):
            require(h.project(tuple(a * v for v in y)) == tuple(a * v % h.n for v in h.project(y)),
                    "quotient scalar action fails")
        require(h.reduce_class(y, h.n) == y == h.inflate_class(y, h.n),
                "identity transition fails")
    return {"modulus": h.n, "code_order": len(code), "dual_order": len(dual),
            "gram_kernel_order": len(h.gram_kernel), "cut_kernel_order": len(h.cut_kernel),
            "classes": [{"potential": y, "edge": h.project(y)} for y in sorted(h.classes)]}


def verify_pair(lo, hi):
    n, m = lo.n, hi.n
    d = m // n
    red, inc = {}, {}
    # Every Gram-kernel representative, not only chosen coset representatives.
    for y in hi.gram_kernel:
        q = hi.reduce_class(y, n)
        require(lo.project(q) == reduction(hi.project(y), m, n), "reduction square fails")
        require(q == hi.reduce_class(hi.class_of(y), n), "reduction depends on coset representative")
        require(q == hi.reduce_class(tuple(v + m for v in y), n), "reduction depends on integer lift")
        require(lo.inflate_class(q, m) == hi.class_of(tuple(d * v for v in y)),
                "large round trip fails")
        red[hi.class_of(y)] = q
    for y in lo.gram_kernel:
        q = lo.inflate_class(y, m)
        require(hi.project(q) == scaled_inflation(lo.project(y), n, m), "inflation square fails")
        require(q == lo.inflate_class(lo.class_of(y), m), "inflation depends on coset representative")
        require(q == lo.inflate_class(tuple(v + n for v in y), m), "inflation depends on integer lift")
        require(hi.reduce_class(q, n) == lo.class_of(tuple(d * v for v in y)),
                "small round trip fails")
        inc[lo.class_of(y)] = q
    require(len(set(inc.values())) == len(lo.classes), "quotient inflation not injective")
    for source, target, mapping in ((hi, lo, red), (lo, hi, inc)):
        for a, b in product(source.classes, repeat=2):
            require(mapping[source.class_of(add(a, b, source.n))]
                    == target.class_of(add(mapping[a], mapping[b], target.n)),
                    "quotient transition not additive")
    for x in hi.hull:
        require(hi.reduce_edge(x, n) == reduction(x, m, n), "edge reduction fails")
    for x in lo.hull:
        require(lo.inflate_edge(x, m) == scaled_inflation(x, n, m), "edge inflation fails")
    return {"small": n, "large": m,
            "reduction": [{"source": y, "target": red[y]} for y in sorted(red)],
            "scaled_inflation": [{"source": y, "target": inc[y]} for y in sorted(inc)]}


def verify_triple(lo, mid, hi):
    for y in hi.gram_kernel:
        require(mid.reduce_class(hi.reduce_class(y, mid.n), lo.n) == hi.reduce_class(y, lo.n),
                "three-level quotient reduction fails")
    for y in lo.gram_kernel:
        require(mid.inflate_class(lo.inflate_class(y, mid.n), hi.n) == lo.inflate_class(y, hi.n),
                "three-level quotient inflation fails")
    for x in hi.hull:
        require(reduction(reduction(x, hi.n, mid.n), mid.n, lo.n) == reduction(x, hi.n, lo.n),
                "three-level edge reduction fails")
    for x in lo.hull:
        require(scaled_inflation(scaled_inflation(x, lo.n, mid.n), mid.n, hi.n)
                == scaled_inflation(x, lo.n, hi.n), "three-level edge inflation fails")


def evidence():
    fixture = json.loads((ROOT / FIXTURE).read_text())
    require(fixture["schema"] == 1, "invalid fixture schema")
    seeds = json.loads((ROOT / fixture["seed_fixture"]).read_text())["cases"]
    cases = seeds + fixture["extra_cases"]
    require(len({c["id"] for c in cases}) == len(cases), "duplicate matrix ID")
    records = []
    for c in cases:
        require(c["moduli"] == sorted(set(c["moduli"])), "moduli not unique and sorted")
        levels = {n: CodeHull(c["matrix"], n, c["columns"]) for n in c["moduli"]}
        reports = [verify_level(h, c in seeds) for h in levels.values()]
        maps = [verify_pair(levels[n], levels[m]) for n, m in combinations(levels, 2) if m % n == 0]
        triples = []
        for n, m, l in combinations(levels, 3):
            if m % n == 0 and l % m == 0:
                verify_triple(levels[n], levels[m], levels[l])
                triples.append([n, m, l])
        records.append({"id": c["id"], "matrix": c["matrix"], "columns": c["columns"],
                        "levels": reports, "maps": maps, "composition_triples": triples})
    # Reuse the finite coordinate and negative-control checks in this receipt.
    from conformance.test_code_hull import coordinate_controls, negative_controls
    coordinates = coordinate_controls()
    negatives = negative_controls()
    return {"schema": 1, "authority": "non_authoritative_experiment", "claim_promotions": [],
            "questions": ["ABC-HULL-01"], "scope": fixture["scope"],
            "summary": {"matrices": len(records), "modulus_cases": sum(len(r["levels"]) for r in records),
                        "proper_tower_pairs": sum(len(r["maps"]) for r in records),
                        "composition_triples": sum(len(r["composition_triples"]) for r in records)},
            "coordinate_controls": coordinates, "negative_controls": negatives, "records": records,
            "sources_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = evidence()
    serialized = canonical(result)
    if args.write:
        RECEIPT.write_text(serialized)
    else:
        require(RECEIPT.read_text() == serialized, "receipt drift; investigate before regeneration")
    print("PASS: code-hull tower; " + json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
