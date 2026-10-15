"""Rebuild exact source-pinned evidence for the separately scoped surjective theorem."""

import argparse
from collections import defaultdict
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from math import gcd, lcm, prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel.surjective_bicycle import SurjectiveRepresentation
from kernel.surjective_equivalence import find_surjective_equivalence
from oracles.arithmetic_matroid import arithmetic_signature, lattice_bicycles, rectangular_factors
from oracles.regular_snf import (
    determinant, is_totally_unimodular, literal_bicycles, quotient_key,
    quotient_representatives, smith_invariants,
)
from oracles.surjective_equivalence import brute_surjective_equivalence

FIXTURES = "conformance/fixtures/surjective-representation-v1.json"
RECEIPT = "conformance/receipts/surjective-representation-v1.json"
SOURCES = (
    FIXTURES, "conformance/fixtures/regular-modular-bicycle-v1.json",
    "kernel/surjective_bicycle.py", "kernel/surjective_equivalence.py",
    "oracles/surjective_equivalence.py", "kernel/arithmetic_matroid.py",
    "oracles/arithmetic_matroid.py", "kernel/regular_bicycle.py", "kernel/graph_bicycle.py",
    "oracles/regular_snf.py", "oracles/graph_snf.py",
    "conformance/test_surjective_representation.py",
    "conformance/replay_surjective_representation.py",
    "proof/surjective-realization-invariance.md", "sources/surjective-representation-equivalence.md",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


@lru_cache(maxsize=None)
def oracle_edges(rows, width, n):
    return frozenset(lattice_bicycles(rows, n, width))


def order_profile(bicycles, n):
    counts = defaultdict(int)
    for b in bicycles:
        counts[lcm(*(n // gcd(n, x) for x in b))] += 1
    return [{"order": order, "count": count} for order, count in sorted(counts.items())]


def census():
    buckets = defaultdict(list)
    non_tu = 0
    for values in product((-1, 0, 1), repeat=6):
        rows = (values[:3], values[3:])
        if rectangular_factors(rows) != (1, 1):
            continue
        non_tu += not is_totally_unimodular(rows)
        buckets[arithmetic_signature(rows)].append(SurjectiveRepresentation(rows))
    records, cases = [], 0
    for signature, group in buckets.items():
        a = group[0]
        for ap in group:
            w = find_surjective_equivalence(a, ap)
            require(a.realization.signature == signature == ap.realization.signature,
                    "candidate and independent all-subset signatures disagree")
            require(brute_surjective_equivalence(a.rows, ap.rows) is not None,
                    "independent sign search disagrees in census")
            require(smith_invariants(a.gram) == smith_invariants(ap.gram), "census Gram factors changed")
            for n in (2, 3, 4, 6):
                source, target = oracle_edges(a.rows, 3, n), oracle_edges(ap.rows, 3, n)
                require(set(ap.bicycles(n)) == target, "census bicycle enumeration disagrees")
                require({w.transport_bicycle(b, n) for b in source} == target,
                        "census transport disagrees with modular lattice oracle")
                cases += 1
            records.append({"matrix": ap.rows, "arithmetic_signature": signature,
                            "signs": w.signs, "row_change": w.row_change})
    rejected = 0
    representatives = [group[0] for group in buckets.values()]
    for a in representatives:
        for ap in representatives:
            if a == ap:
                continue
            require(brute_surjective_equivalence(a.rows, ap.rows) is None,
                    "independent oracle accepted a cross-bucket comparison")
            try:
                find_surjective_equivalence(a, ap)
            except ValueError:
                rejected += 1
            else:
                raise RuntimeError("candidate accepted a cross-bucket comparison")
    size = sum(map(len, buckets.values()))
    require((size, non_tu, len(buckets), cases, rejected) == (552, 96, 10, 2208, 90),
            "ternary surjective census scope changed")
    return {"all_matrices": 729, "surjective_matrices": size, "non_tu_matrices": non_tu,
            "arithmetic_buckets": len(buckets), "modulus_cases": cases,
            "cross_bucket_rejections": rejected, "witness_records_sha256": digest(records)}


def evidence():
    data = json.loads((ROOT / FIXTURES).read_text())
    require(data["schema"] == 1, "unsupported fixture schema")
    ids, pairs, cases, towers = set(), [], [], []
    for f in data["pairs"]:
        require(f["id"] not in ids, "duplicate pair id")
        ids.add(f["id"])
        a, ap = (SurjectiveRepresentation(f[k], f["columns"]) for k in ("source", "target"))
        w = find_surjective_equivalence(a, ap, f["permutation"])
        require(brute_surjective_equivalence(a.rows, ap.rows, w.permutation, a.columns) is not None,
                "independent sign search found no fixture witness")
        signature = arithmetic_signature(tuple(tuple(row[j] for j in w.permutation) for row in a.rows), a.columns)
        require(signature == arithmetic_signature(ap.rows, ap.columns), "fixture arithmetic data changed")
        smith = smith_invariants(a.gram)
        require(smith == tuple(f["gram_smith"]) == smith_invariants(ap.gram), "fixture Gram factors changed")
        minors = [abs(determinant([[row[j] for j in cc] for row in a.rows]))
                  for cc in combinations(range(a.columns), a.rank)]
        require((1 not in minors) == f["no_unit_basis"], "unit-basis fixture annotation changed")
        classes = quotient_representatives(a.gram)
        target_classes = quotient_representatives(ap.gram)
        require({quotient_key(ap.gram, w.divisor_action(d)) for d in classes.values()} == set(target_classes),
                "Gram quotient transport is not onto")
        pairs.append({"fixture": f["id"], "permutation": w.permutation, "signs": w.signs,
                      "row_change": w.row_change, "source_right_inverse": a.right_inverse,
                      "target_right_inverse": ap.right_inverse, "gram_smith": smith,
                      "quotient_order": len(classes), "no_unit_basis": f["no_unit_basis"],
                      "arithmetic_signature_sha256": digest(signature)})
        modules = {}
        for n in f["moduli"]:
            source, target = oracle_edges(a.rows, a.columns, n), oracle_edges(ap.rows, ap.columns, n)
            require(set(a.bicycles(n)) == source and set(ap.bicycles(n)) == target,
                    "fixture edge enumeration disagrees with modular lattice oracle")
            require(literal_bicycles(a.rows, n, a.columns) == source and
                    literal_bicycles(ap.rows, n, ap.columns) == target, "literal cuts disagree")
            require(len(source) == prod(gcd(n, factor) for factor in smith), "Smith count disagrees")
            torsion = {key for key in classes if all((n * v).denominator == 1 for v in key)}
            require({quotient_key(a.gram, a.bicycle_to_divisor(b, n)) for b in source} == torsion,
                    "forward map misses independently enumerated torsion")
            for key, d in classes.items():
                if key in torsion:
                    b = a.divisor_to_bicycle(d, n)
                    require(b in source and quotient_key(a.gram, a.bicycle_to_divisor(b, n)) == key,
                            "divisor inverse identity failed")
            for b in source:
                d = a.bicycle_to_divisor(b, n)
                require(a.divisor_to_bicycle(d, n) == b, "bicycle inverse identity failed")
                bp = w.transport_bicycle(b, n)
                require(bp in target and w.inverse().transport_bicycle(bp, n) == b, "witness inverse failed")
                dp = w.divisor_action(d)
                require(quotient_key(ap.gram, ap.bicycle_to_divisor(bp, n)) == quotient_key(ap.gram, dp),
                        "forward Gram square failed")
                require(ap.divisor_to_bicycle(dp, n) == bp, "inverse Gram square failed")
            require({w.transport_bicycle(b, n) for b in source} == target, "fixture transport is not onto")
            modules[n] = source
            cases.append({"fixture": f["id"], "modulus": n, "bicycles": len(source),
                          "order_profile": order_profile(source, n), "both_inverse_checks": len(source),
                          "both_gram_square_checks": len(source), "torsion_classes": len(torsion),
                          "source_edge_set_sha256": digest(sorted(source)),
                          "target_edge_set_sha256": digest(sorted(target))})
        for n in modules:
            for m in modules:
                if m <= n or m % n:
                    continue
                for b in modules[m]:
                    small = a.reduce_bicycle(b, m, n)
                    require(a.class_key(a.bicycle_to_divisor(small, n)) ==
                            a.class_key(tuple((m // n) * x for x in a.bicycle_to_divisor(b, m))),
                            "Gram reduction is not multiplication by m/n")
                    require(w.transport_bicycle(small, n) == ap.reduce_bicycle(w.transport_bicycle(b, m), m, n),
                            "reduction transport failed")
                for b in modules[n]:
                    large = a.inflate_bicycle(b, n, m)
                    require(a.class_key(a.bicycle_to_divisor(large, m)) == a.class_key(a.bicycle_to_divisor(b, n)),
                            "Gram inflation is not torsion inclusion")
                    require(w.transport_bicycle(large, m) == ap.inflate_bicycle(w.transport_bicycle(b, n), n, m),
                            "inflation transport failed")
                towers.append({"fixture": f["id"], "n": n, "m": m,
                               "reduction_checks": len(modules[m]), "inflation_checks": len(modules[n])})
    for f in data["negative_pairs"]:
        a, ap = (SurjectiveRepresentation(f[k], f["columns"]) for k in ("source", "target"))
        require(brute_surjective_equivalence(a.rows, ap.rows, f["permutation"], a.columns) is None,
                "independent oracle accepted a negative fixture")
        try:
            find_surjective_equivalence(a, ap, f["permutation"])
        except ValueError:
            pass
        else:
            raise RuntimeError("candidate accepted a negative fixture")
    for f in data["out_of_domain"]:
        try:
            SurjectiveRepresentation(f["rows"], f["columns"])
        except ValueError:
            pass
        else:
            raise RuntimeError("candidate accepted a nonsurjective fixture")
    return {
        "schema": 1, "claim": "ABC-SURJECTIVE-REALIZATION-INVARIANCE",
        "domain": "essential free-lattice realizations with m(empty)=m(E)=1",
        "scope": "finite exact evidence supporting the separate arbitrary-modulus integral proof",
        "pair_count": len(pairs), "pairs": pairs, "case_count": len(cases), "cases": cases,
        "tower_pair_count": len(towers), "tower_checks": towers,
        "negative_pairs": [f["id"] for f in data["negative_pairs"]],
        "out_of_domain": [f["id"] for f in data["out_of_domain"]], "ternary_census": census(),
        "sources_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES},
        "comparison_maps": "depend on a verified witness; the invariant is the tower isomorphism class",
        "original_unrestricted_ABC": "retracted by the nonsurjective rank-two counterexample",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rebuilt = canonical(evidence())
    path = ROOT / RECEIPT
    if args.write:
        path.write_text(rebuilt)
    else:
        require(path.is_file() and path.read_text() == rebuilt, "receipt drift; investigate before intentional --write")
    result = json.loads(rebuilt)
    print(f"PASS: {result['pair_count']} surjective pairs, {result['case_count']} modulus cases, "
          f"{result['tower_pair_count']} tower pairs; 552 matrices in 10 arithmetic buckets")


if __name__ == "__main__":
    main()
