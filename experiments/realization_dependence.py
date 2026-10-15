"""Replay explicit code-hull and realization-dependence seeds, not a census."""

import argparse
import hashlib
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel.arithmetic_matroid import IntegralRealization
from oracles.arithmetic_matroid import (
    arithmetic_signature, lattice_bicycles, rectangular_factors,
)
from oracles.regular_snf import matrix_data

FIXTURE = ROOT / "conformance/fixtures/realization-dependence-v1.json"
RECEIPT = ROOT / "conformance/receipts/realization-dependence-v1.json"
SOURCES = (
    "experiments/realization_dependence.py",
    "conformance/fixtures/realization-dependence-v1.json",
    "conformance/test_realization_dependence.py",
    "kernel/arithmetic_matroid.py", "kernel/regular_bicycle.py",
    "kernel/graph_bicycle.py", "oracles/arithmetic_matroid.py",
    "oracles/regular_snf.py", "oracles/graph_snf.py",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def literal_code_hull(rows, n, columns=None):
    """Test every edge vector against every codeword with the coordinate form.

    This deliberately uses neither a Gram-torsion formula nor a kernel
    membership test. It is exponential small-fixture evidence only.
    """
    if type(n) is not int or n < 2:
        raise ValueError("modulus must be an integer at least two")
    a, width = matrix_data(rows, columns)
    code = {
        tuple(sum(a[i][j] * y[i] for i in range(len(a))) % n
              for j in range(width))
        for y in product(range(n), repeat=len(a))
    }
    dual = {
        edge for edge in product(range(n), repeat=width)
        if all(sum(x * y for x, y in zip(edge, word)) % n == 0
               for word in code)
    }
    return code, dual, code & dual


def annihilator_profile(group, n):
    return {
        str(d): sum(all(d * x % n == 0 for x in v) for v in group)
        for d in range(1, n + 1) if n % d == 0
    }


def load_fixture():
    fixture = json.loads(FIXTURE.read_text())
    require(fixture["schema"] == 1 and fixture["cases"], "invalid fixture schema")
    seen = set()
    for case in fixture["cases"]:
        label, moduli = case["id"], case["moduli"]
        require(isinstance(label, str) and label and label not in seen,
                "duplicate or invalid fixture ID")
        seen.add(label)
        require(moduli and all(type(n) is int and n >= 2 for n in moduli)
                and moduli == sorted(set(moduli)), "invalid fixture moduli")
        require(set(case["expected_orders"]) == {str(n) for n in moduli},
                "expected orders must cover every listed modulus")
        require(all(type(v) is int and v >= 1
                    for v in case["expected_orders"].values()), "invalid expected order")
    return fixture


def evidence():
    fixture = load_fixture()
    records, groups, signatures, subset_factors = [], {}, {}, {}
    tower_pairs, crt_cases = 0, 0
    for case in fixture["cases"]:
        label, width = case["id"], case["columns"]
        model = IntegralRealization(case["matrix"], width)
        signatures[label] = arithmetic_signature(model.rows, width)
        require(model.signature == signatures[label], "arithmetic signature disagreement")
        require(str(model.full_smith.torsion_order) == case["ambient_index"],
                "fixture changed its declared ambient index")
        subset_factors[label] = []
        for mask in range(1 << width):
            indices = [j for j in range(width) if mask >> j & 1]
            rows = tuple(tuple(row[j] for j in indices) for row in model.rows)
            independent = rectangular_factors(rows, len(indices))
            require(model.subset_smith(mask).factors == independent,
                    "subset quotient-factor disagreement")
            subset_factors[label].append(independent)

        groups[label], cases, maps, crt = {}, [], [], []
        for n in case["moduli"]:
            code, dual, hull = literal_code_hull(model.rows, n, width)
            require(hull == set(model.bicycles(n)) == lattice_bicycles(model.rows, n, width),
                    f"literal hull, candidate, and edge/lattice oracle disagree: {label}/{n}")
            require(len(hull) == case["expected_orders"][str(n)],
                    f"expected control order changed: {label}/{n}")
            groups[label][n] = hull
            cases.append({"modulus": n, "code_order": len(code), "dual_order": len(dual),
                          "hull_order": len(hull), "hull_vectors": sorted(hull),
                          "annihilator_profile": annihilator_profile(hull, n)})

        for n, m in combinations(case["moduli"], 2):
            if m % n:
                continue
            source, target = groups[label][n], groups[label][m]
            reduction = {tuple(x % n for x in v) for v in target}
            inflation = {tuple((m // n) * x % m for x in v) for v in source}
            require(reduction <= source and inflation <= target,
                    f"modulus map leaves the hull: {label}/{n}/{m}")
            require(len(inflation) == len(source), "scaled inflation is not injective")
            maps.append({"small": n, "large": m,
                         "reduction_image": sorted(reduction),
                         "scaled_inflation_image": sorted(inflation)})
            tower_pairs += 1

        for n, m in combinations(case["moduli"], 2):
            if gcd(n, m) != 1 or n * m not in groups[label]:
                continue
            actual = {(tuple(x % n for x in v), tuple(x % m for x in v))
                      for v in groups[label][n * m]}
            expected = set(product(groups[label][n], groups[label][m]))
            require(actual == expected and len(actual) == len(groups[label][n * m]),
                    f"Chinese-remainder hull comparison failed: {label}/{n}/{m}")
            crt.append({"coprime_factors": [n, m], "modulus": n * m,
                        "hull_order": len(actual)})
            crt_cases += 1

        records.append({"id": label, "matrix": model.rows, "columns": width,
                        "ambient_index": case["ambient_index"],
                        "arithmetic_signature": signatures[label],
                        "subset_smith_factors": subset_factors[label],
                        "cases": cases, "tower_maps": maps, "crt": crt})

    require(signatures["index5-a1"] == signatures["index5-a2"],
            "lost complete arithmetic equality of the counterexample")
    require(subset_factors["index5-a1"] == subset_factors["index5-a2"],
            "lost equal subset quotient groups")
    require(all([len(groups[label][n]) for label in ("index5-a1", "index5-a2")] == [1, 5]
                for n in (5, 10)), "lost realization-dependence negative control")
    require([len(groups[label][25]) for label in ("index5-a1", "index5-a2")] == [5, 5],
            "lost equal-order-at-another-modulus control")
    require(len(groups["scalar2"][2]) == 1 and len(groups["scalar2"][4]) == 2,
            "lost the universal torsion-model obstruction")
    bad_inflation = sorted(groups["surjective-c13"][13] - groups["surjective-c13"][26])
    require(bad_inflation, "unscaled inflation control is ineffective")

    return {
        "schema": 1, "authority": "non_authoritative_experiment",
        "scope": fixture["scope"],
        "questions": ["ABC-HULL-01", "ABC-RD-01", "ABC-MODULE-01"],
        "summary": {"realizations": len(records),
                    "modulus_cases": sum(len(r["cases"]) for r in records),
                    "proper_tower_pairs": tower_pairs, "crt_cases": crt_cases},
        "controls": {"complete_arithmetic_data_agree": True,
                     "all_subset_quotient_groups_agree": True,
                     "counterexample_orders_at_5_and_10": [1, 5],
                     "counterexample_orders_at_25": [5, 5],
                     "scalar_two_orders_at_2_and_4": [1, 2],
                     "unscaled_inflation_rejected": {"small": 13, "large": 26,
                                                     "vector": bad_inflation[0]}},
        "records": records,
        "sources_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                           for p in SOURCES},
        "claim_promotions": [],
    }


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
        require(RECEIPT.read_text() == serialized,
                "receipt drift; investigate before regeneration")
    print("PASS: realization-dependence/code-hull seeds; "
          + json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
