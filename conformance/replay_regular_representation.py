"""Rebuild source-pinned regular-representation equivalence evidence."""

import argparse
from collections import defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel.regular_bicycle import TURepresentation
from kernel.regular_equivalence import find_tu_equivalence
from oracles.regular_equivalence import brute_equivalence, matroid_signature
from oracles.regular_snf import (
    cycle_bicycles, determinant, gram_matrix, is_totally_unimodular,
    quotient_key, quotient_representatives, smith_invariants,
)

FIXTURES = "conformance/fixtures/regular-representation-v1.json"
RECEIPT = "conformance/receipts/regular-representation-v1.json"
SOURCES = (
    FIXTURES,
    "kernel/regular_equivalence.py", "oracles/regular_equivalence.py",
    "kernel/regular_bicycle.py", "kernel/graph_bicycle.py",
    "oracles/regular_snf.py", "oracles/graph_snf.py",
    "conformance/test_regular_representation.py",
    "conformance/replay_regular_representation.py",
    "proof/regular-representation-independence.md",
    "sources/regular-representation-equivalence.md",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def census():
    buckets = defaultdict(list)
    for v in product((-1, 0, 1), repeat=6):
        rows = (v[:3], v[3:])
        if is_totally_unimodular(rows) and determinant(gram_matrix(rows)):
            buckets[matroid_signature(rows)].append(TURepresentation(rows))
    records, cases = [], 0
    for signature, group in buckets.items():
        source = group[0]
        for target in group:
            w = find_tu_equivalence(source, target)
            require(brute_equivalence(source.rows, target.rows) is not None, "census witness disagreement")
            for n in (2, 3, 4, 6):
                expected = cycle_bicycles(target.rows, n)
                require({w.transport_bicycle(b, n) for b in cycle_bicycles(source.rows, n)} == expected,
                        "census tower disagreement")
                cases += 1
            records.append({"matrix": target.rows, "matroid": signature,
                            "signs": w.signs, "row_change": w.row_change})
    rejected = 0
    representatives = [group[0] for group in buckets.values()]
    for a in representatives:
        for ap in representatives:
            if a == ap:
                continue
            require(brute_equivalence(a.rows, ap.rows) is None, "cross-bucket oracle accepted")
            try:
                find_tu_equivalence(a, ap)
            except ValueError:
                rejected += 1
            else:
                raise RuntimeError("cross-bucket candidate accepted")
    require(len(records) == 456 and len(buckets) == 7 and cases == 1824 and rejected == 42,
            "ternary census scope changed")
    return {"all_matrices": 729, "full_rank_tu_matrices": len(records),
            "labeled_matroid_buckets": len(buckets), "modulus_cases": cases,
            "cross_bucket_rejections": rejected, "witness_records_sha256": digest(records)}


def evidence():
    data = json.loads((ROOT / FIXTURES).read_text())
    require(data["schema"] == 1, "unsupported fixture schema")
    ids, pairs, cases, towers = set(), [], [], []
    for f in data["pairs"]:
        require(f["id"] not in ids, "duplicate pair id")
        ids.add(f["id"])
        a, ap = (TURepresentation(f[name], f["columns"]) for name in ("source", "target"))
        aligned = tuple(tuple(row[j] for j in f["permutation"]) for row in a.rows)
        signature = matroid_signature(aligned, a.columns)
        require(signature == matroid_signature(ap.rows, ap.columns), "labeled matroid disagreement")
        require(brute_equivalence(a.rows, ap.rows, f["permutation"], a.columns) is not None,
                "brute signed-equivalence oracle found no witness")
        w = find_tu_equivalence(a, ap, f["permutation"])
        inverse = w.inverse()
        smith, target_smith = smith_invariants(a.gram), smith_invariants(ap.gram)
        require(smith == target_smith, "Gram Smith factors changed")
        classes = quotient_representatives(a.gram)
        target_classes = quotient_representatives(ap.gram)
        require({quotient_key(ap.gram, w.divisor_action(d)) for d in classes.values()} == set(target_classes),
                "Gram quotient transport is not surjective")
        pairs.append({"fixture": f["id"], "permutation": w.permutation,
                      "signs": w.signs, "row_change": w.row_change,
                      "gram_smith": smith, "quotient_order": len(classes),
                      "matroid_rank_signature_sha256": digest(signature)})
        modules = {}
        for n in f["moduli"]:
            source = cycle_bicycles(a.rows, n, a.columns)
            target = cycle_bicycles(ap.rows, n, ap.columns)
            require({w.transport_bicycle(b, n) for b in source} == target, "bicycle set transport failed")
            require(len(source) == len(target), "bicycle order changed")
            for b in source:
                value = w.transport_bicycle(b, n)
                require(inverse.transport_bicycle(value, n) == b, "inverse witness failed")
                d = a.bicycle_to_divisor(b, n)
                new_d = w.divisor_action(d)
                require(quotient_key(ap.gram, ap.bicycle_to_divisor(value, n)) == quotient_key(ap.gram, new_d),
                        "forward Gram square failed")
                require(ap.divisor_to_bicycle(new_d, n) == value, "inverse Gram square failed")
            modules[n] = source
            cases.append({"fixture": f["id"], "modulus": n, "bicycles": len(source),
                          "forward_square_checks": len(source), "inverse_square_checks": len(source),
                          "source_edge_set_sha256": digest(sorted(source)),
                          "target_edge_set_sha256": digest(sorted(target))})
        for n in modules:
            for m in modules:
                if m <= n or m % n:
                    continue
                for b in modules[m]:
                    require(w.transport_bicycle(a.reduce_bicycle(b, m, n), n) ==
                            ap.reduce_bicycle(w.transport_bicycle(b, m), m, n), "reduction transport failed")
                for b in modules[n]:
                    require(w.transport_bicycle(a.inflate_bicycle(b, n, m), m) ==
                            ap.inflate_bicycle(w.transport_bicycle(b, n), n, m), "inflation transport failed")
                towers.append({"fixture": f["id"], "n": n, "m": m,
                               "reduction_checks": len(modules[m]), "inflation_checks": len(modules[n])})
    return {
        "schema": 1, "claim": "ABC-REGULAR-REPRESENTATION-INVARIANCE",
        "scope": "finite exact witness evidence for the separate integral tower proof",
        "pair_count": len(ids), "pairs": pairs, "case_count": len(cases), "cases": cases,
        "tower_pair_count": len(towers), "tower_checks": towers, "ternary_census": census(),
        "sources_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES},
        "comparison_maps": "depend on the chosen verified witness; no unique canonical map asserted",
        "arithmetic_realization_invariance": "open",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="replace the derived receipt")
    mode.add_argument("--check", action="store_true", help="check receipt bytes (default)")
    args = parser.parse_args()
    rebuilt = canonical(evidence())
    destination = ROOT / RECEIPT
    if args.write:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rebuilt)
    else:
        require(destination.exists() and destination.read_text() == rebuilt,
                "receipt drift; investigate, then use --write to regenerate intentionally")
    result = json.loads(rebuilt)
    print(f"PASS: {result['pair_count']} TU pairs, {result['case_count']} modulus cases, "
          f"{result['tower_pair_count']} tower pairs; 456 representations in 7 labeled matroid buckets")


if __name__ == "__main__":
    main()
