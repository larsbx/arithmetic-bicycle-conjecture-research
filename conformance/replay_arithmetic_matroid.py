"""Rebuild exact arithmetic signatures and the two-realization counterexample."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel.arithmetic_matroid import IntegralRealization, arithmetic_equal
from oracles.arithmetic_matroid import arithmetic_signature, lattice_bicycles, rectangular_factors
from oracles.graph_snf import edge_order
from oracles.regular_snf import literal_bicycles

FIXTURES = "conformance/fixtures/arithmetic-matroid-v1.json"
RECEIPT = "conformance/receipts/arithmetic-matroid-v1.json"
SOURCES = (
    FIXTURES, "kernel/arithmetic_matroid.py", "oracles/arithmetic_matroid.py",
    "kernel/graph_bicycle.py", "kernel/regular_bicycle.py",
    "oracles/graph_snf.py", "oracles/regular_snf.py",
    "conformance/test_arithmetic_matroid.py",
    "conformance/fixtures/regular-modular-bicycle-v1.json",
    "conformance/replay_arithmetic_matroid.py",
    "proof/arithmetic-matroid-signature.md",
    "proof/arithmetic-realization-counterexample.md",
    "sources/arithmetic-matroid-background.md",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def evidence():
    data = json.loads((ROOT / FIXTURES).read_text())
    require(data["schema"] == 1, "unsupported fixture schema")
    objects, records, subset_count = {}, [], 0
    for f in data["fixtures"]:
        require(f["id"] not in objects, "duplicate realization id")
        a = IntegralRealization(f["matrix"], f["columns"])
        objects[f["id"]] = a
        expected = tuple(map(tuple, f["signature"]))
        require(a.signature == expected == arithmetic_signature(a.rows, a.columns), "arithmetic signature disagreement")
        subsets = []
        for mask, (rank, m) in enumerate(a.signature):
            c = a.subset_smith(mask)
            cols = tuple(j for j in range(a.columns) if mask >> j & 1)
            rows = tuple(tuple(row[j] for j in cols) for row in a.rows)
            require(c.factors == rectangular_factors(rows, len(cols)), "subset Smith-factor disagreement")
            require(c.rank == rank and c.torsion_order == m, "subset rank/index disagreement")
            subsets.append({"mask": mask, "rank": rank, "multiplicity": str(m),
                            "smith_factors": [str(x) for x in c.factors],
                            "certificate_sha256": digest({"columns": c.columns, "left": c.left,
                                                          "right": c.right, "diagonal": c.diagonal})})
        subset_count += len(subsets)
        records.append({"fixture": f["id"], "arithmetic_data": a.canonical_data(),
                        "encoding_sha256": hashlib.sha256(a.canonical_encoding()).hexdigest(), "subsets": subsets})
    comparisons = []
    for f in data["comparisons"]:
        actual = arithmetic_equal(objects[f["source"]], objects[f["target"]], f["permutation"])
        require(actual == f["equal"], "comparison outcome changed")
        comparisons.append({**f, "result": actual})
    control = data["counterexample"]
    a, b = objects[control["source"]], objects[control["target"]]
    require(arithmetic_equal(a, b) and a.canonical_encoding() == b.canonical_encoding(),
            "counterexample arithmetic data no longer agree")
    require(a.signature == ((0, 1), (1, 1), (1, 1), (2, 5)), "counterexample hypotheses changed")
    require(len(control["moduli"]) == len(control["source_counts"]) == len(control["target_counts"]),
            "counterexample count-vector lengths differ")
    cases = []
    for n, count_a, count_b in zip(control["moduli"], control["source_counts"], control["target_counts"]):
        sizes = []
        for label, realization, count in (("source", a, count_a), ("target", b, count_b)):
            bikes = realization.bicycles(n)
            require(bikes == lattice_bicycles(realization.rows, n) == literal_bicycles(realization.rows, n),
                    "independent modular image/cycle disagreement")
            require(len(bikes) == count, "counterexample profile changed")
            orders = Counter(edge_order(edge, n) for edge in bikes)
            cases.append({"side": label, "modulus": n, "bicycles": len(bikes),
                          "orders": {str(k): v for k, v in sorted(orders.items())},
                          "edges": sorted(bikes), "edge_set_sha256": digest(sorted(bikes))})
            sizes.append(len(bikes))
        if n in (5, 10):
            require(sizes == [1, 5], "refuting order discrepancy changed")
    require(a.bicycles(5) == {(0, 0)} and b.bicycles(5) == {(u, 2 * u % 5) for u in range(5)},
            "literal prime counterexample changed")
    require(a.bicycles(10) == {(0, 0)} and b.bicycles(10) == {(2 * u, 4 * u % 10) for u in range(5)},
            "literal mixed-composite counterexample changed")
    return {"schema": 1, "claims": ["ABC-ARITHMETIC-SIGNATURE", "ABC-ARITHMETIC-REALIZATION-COUNTEREXAMPLE"],
            "scope": "exact essential arithmetic data and explicit refutation, not an exhaustive realization census",
            "fixture_count": len(objects), "subset_count": subset_count, "fixtures": records,
            "comparison_count": len(comparisons), "comparisons": comparisons,
            "bicycle_case_count": len(cases), "bicycle_cases": cases,
            "refuted_claims": ["ABC-MAIN", "ABC-REALIZATION-INVARIANCE"],
            "counterexample_moduli": [5, 10],
            "common_arithmetic_encoding_sha256": hashlib.sha256(a.canonical_encoding()).hexdigest(),
            "sources_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES}}


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
    print(f"PASS: {result['fixture_count']} realizations, {result['subset_count']} subset records, "
          f"{result['comparison_count']} comparisons, {result['bicycle_case_count']} bicycle cases; "
          "counterexample verified at moduli 5 and 10")


if __name__ == "__main__":
    main()
