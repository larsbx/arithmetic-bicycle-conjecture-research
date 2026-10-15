"""Exact arithmetic signatures, Smith certificates, and the ABC counterexample."""

from dataclasses import replace
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
import unittest

from kernel.arithmetic_matroid import (
    IntegralRealization, SmithCertificate, arithmetic_equal, identity, smith_certificate,
)
from oracles.arithmetic_matroid import arithmetic_signature, lattice_bicycles, rectangular_factors
from oracles.graph_snf import determinant, edge_order
from oracles.regular_snf import literal_bicycles

HERE = Path(__file__).parent
DATA = json.loads((HERE / "fixtures/arithmetic-matroid-v1.json").read_text())
FIXTURES = {f["id"]: f for f in DATA["fixtures"]}


def realization(name):
    f = FIXTURES[name]
    return IntegralRealization(f["matrix"], f["columns"])


def matrix_product(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


class SmithCertificateTests(unittest.TestCase):
    def test_all_15625_integer_two_by_three_matrices(self):
        for v in product((-2, -1, 0, 1, 2), repeat=6):
            rows = (v[:3], v[3:])
            certificate = smith_certificate(rows)
            self.assertEqual(certificate.factors, rectangular_factors(rows))
            self.assertEqual(abs(determinant(certificate.left)), 1)
            self.assertEqual(abs(determinant(certificate.right)), 1)
            self.assertEqual(matrix_product(matrix_product(certificate.left, rows), certificate.right), certificate.diagonal)

    def test_rectangular_singular_empty_and_large_certificates(self):
        cases = (((), 3), ((), 0), (((), ()), 0),
                 (((0, 0, 0), (0, 0, 0)), 3),
                 (((6, 0), (0, 10)), 2),
                 (((-6, 10, 0),), 3),
                 (((2,), (6,), (0,)), 1),
                 (((2**80, 0), (0, 3 * 2**80)), 2))
        for rows, width in cases:
            c = smith_certificate(rows, width)
            self.assertEqual(c.factors, rectangular_factors(rows, width))
            self.assertEqual(abs(determinant(c.left)), 1)
            self.assertEqual(abs(determinant(c.right)), 1)
        d = ((2, 0, 0, 0), (0, 6, 0, 0), (0, 0, 30, 0))
        u = ((1, 2, 0), (0, 1, 3), (0, 0, 1))
        v = ((1, 0, 0, 2), (0, 1, 3, 0), (0, 0, 1, 5), (0, 0, 0, 1))
        planted = matrix_product(matrix_product(u, d), v)
        c = smith_certificate(planted)
        self.assertEqual(c.factors, (2, 6, 30))
        self.assertEqual(rectangular_factors(planted), c.factors)
        self.assertEqual(smith_certificate(((6, 0), (0, 10))).factors, (2, 30))

    def test_forged_or_noncanonical_certificates_are_rejected(self):
        c = smith_certificate(((2, 0), (0, 6)))
        for changes in ({"left": ((2, 0), (0, 1))},
                        {"right": ((1, 0), (0, 0))},
                        {"diagonal": ((2, 1), (0, 6))},
                        {"diagonal": ((2, 0), (0, 7))},
                        {"left": ((True, 0), (0, 1))},
                        {"columns": 3}):
            with self.assertRaises(ValueError):
                replace(c, **changes)
        for rows in (((6, 0), (0, 10)), ((-2, 0), (0, 6)), ((0, 0), (0, 6))):
            with self.assertRaises(ValueError):
                SmithCertificate(rows, 2, identity(2), identity(2), rows)


class ArithmeticSignatureTests(unittest.TestCase):
    def test_every_fixture_subset_against_independent_minor_indices(self):
        for f in DATA["fixtures"]:
            a = realization(f["id"])
            self.assertEqual(a.signature, tuple(map(tuple, f["signature"])))
            self.assertEqual(a.signature, arithmetic_signature(a.rows, a.columns))
            for mask, (rank, m) in enumerate(a.signature):
                c = a.subset_smith(mask)
                cols = tuple(j for j in range(a.columns) if mask >> j & 1)
                rows = tuple(tuple(row[j] for j in cols) for row in a.rows)
                self.assertEqual(c.factors, rectangular_factors(rows, len(cols)))
                self.assertEqual(c.rank, rank)
                self.assertEqual(c.torsion_order, m)
                self.assertEqual(abs(determinant(c.left)), 1)
                self.assertEqual(abs(determinant(c.right)), 1)
            encoded = json.loads(a.canonical_encoding())
            self.assertEqual(len(encoded["subsets"]), 1 << a.columns)
            self.assertNotIn("matrix", encoded)
            self.assertEqual(encoded["subsets"][0], {"mask": 0, "rank": 0, "multiplicity": "1"})
            self.assertEqual(tuple((record["rank"], int(record["multiplicity"])) for record in encoded["subsets"]), a.signature)

    def test_signed_relabeling_and_unimodular_ambient_changes(self):
        for f in DATA["fixtures"]:
            a = realization(f["id"])
            u = [list(row) for row in identity(a.rank)]
            if a.rank >= 2:
                u[0][1] = 3
            elif a.rank == 1:
                u[0][0] = -1
            changed = matrix_product(u, a.rows) if a.rank else ()
            p = tuple(reversed(range(a.columns)))
            changed = tuple(tuple((-1) ** j * row[p[j]] for j in range(a.columns)) for row in changed)
            target = IntegralRealization(changed, a.columns)
            self.assertTrue(arithmetic_equal(a, target, p))
            self.assertEqual(target.signature, arithmetic_signature(changed, a.columns))

    def test_comparison_requires_every_labeled_subset(self):
        for f in DATA["comparisons"]:
            self.assertEqual(arithmetic_equal(realization(f["source"]), realization(f["target"]), f["permutation"]), f["equal"])
        a, b = realization("dependent-a"), realization("dependent-b")
        self.assertEqual(tuple(rank for rank, _ in a.signature), tuple(rank for rank, _ in b.signature))
        self.assertEqual(a.signature[-1], b.signature[-1])
        for j in range(a.columns):
            self.assertEqual(a.signature[1 << j], b.signature[1 << j])
        self.assertNotEqual(a.signature[5], b.signature[5])
        self.assertEqual(a.signature[7], (2, 2))  # Dependent subset: index, not a zero determinant.
        a, b = realization("same-full-smith-a"), realization("same-full-smith-b")
        self.assertEqual(a.full_smith.factors, b.full_smith.factors)
        self.assertFalse(arithmetic_equal(a, b))

    def test_tu_specialization_has_unit_multiplicities(self):
        data = json.loads((HERE / "fixtures/regular-modular-bicycle-v1.json").read_text())
        for f in data["fixtures"]:
            a = IntegralRealization(f["matrix"], f["columns"])
            self.assertTrue(all(m == 1 for _, m in a.signature))
            self.assertEqual(a.signature, arithmetic_signature(a.rows, a.columns))

    def test_invalid_domains_and_cache_aliases_fail_closed(self):
        for rows, width in (([[1], [0]], None), ([[0]], None), ([[1.0]], None),
                            ([[True]], None), ([[1], [1, 0]], None), ([], -1), ([], True)):
            with self.assertRaises(ValueError):
                IntegralRealization(rows, width)
        a = realization("counterexample-a")
        a.subset_smith(1)
        a.bicycles(5)
        for mask in (-1, 4, True, 1.0):
            with self.assertRaises(ValueError):
                a.subset_smith(mask)
        for n in (0, 1, -2, True, 5.0):
            with self.assertRaises(ValueError):
                a.bicycles(n)
            with self.assertRaises(ValueError):
                lattice_bicycles(a.rows, n)
        for p in ((0, 0), (False, 1), (1,), (0, 2)):
            with self.assertRaises(ValueError):
                arithmetic_equal(a, a, p)
        with self.assertRaises(ValueError):
            arithmetic_equal(a.rows, a)
        self.assertFalse(arithmetic_equal(a, realization("scalar-two")))

    def test_saturation_is_not_a_permitted_change_of_ambient_lattice(self):
        a = realization("scalar-two")
        saturated = IntegralRealization(((1,),))
        self.assertEqual(a.signature[-1], (1, 2))
        self.assertEqual(saturated.signature[-1], (1, 1))
        self.assertFalse(arithmetic_equal(a, saturated))
        self.assertEqual(len(a.bicycles(4)), 2)
        self.assertEqual(len(saturated.bicycles(4)), 1)


class ArithmeticCounterexampleTests(unittest.TestCase):
    def test_same_complete_arithmetic_data_with_different_bicycle_orders(self):
        a, b = realization("counterexample-a"), realization("counterexample-b")
        expected = ((0, 1), (1, 1), (1, 1), (2, 5))
        self.assertEqual(a.signature, expected)
        self.assertEqual(b.signature, expected)
        self.assertEqual(arithmetic_signature(a.rows), expected)
        self.assertEqual(arithmetic_signature(b.rows), expected)
        self.assertTrue(arithmetic_equal(a, b))
        self.assertEqual(a.canonical_encoding(), b.canonical_encoding())
        self.assertEqual(a.full_smith.factors, (1, 5))
        self.assertEqual(b.full_smith.factors, (1, 5))
        for n, generator in ((5, (1, 2)), (10, (2, 4))):
            expected_b = {tuple(k * x % n for x in generator) for k in range(5)}
            self.assertEqual(a.bicycles(n), {(0, 0)})
            self.assertEqual(b.bicycles(n), expected_b)
            self.assertEqual(lattice_bicycles(a.rows, n), {(0, 0)})
            self.assertEqual(lattice_bicycles(b.rows, n), expected_b)
            self.assertEqual(edge_order(generator, n), 5)

    def test_prime_prime_power_and_mixed_composite_profiles(self):
        data = DATA["counterexample"]
        a, b = realization(data["source"]), realization(data["target"])
        for n, acount, bcount in zip(data["moduli"], data["source_counts"], data["target_counts"]):
            for realization_, count in ((a, acount), (b, bcount)):
                bikes = realization_.bicycles(n)
                self.assertEqual(len(bikes), count)
                self.assertEqual(bikes, lattice_bicycles(realization_.rows, n))
                self.assertEqual(bikes, literal_bicycles(realization_.rows, n))
        self.assertEqual(len(a.bicycles(25)), len(b.bicycles(25)))
        self.assertNotEqual(len(a.bicycles(5)), len(b.bicycles(5)))
        # Gram torsion is not a valid bicycle oracle without an integral splitting.
        self.assertEqual(rectangular_factors(((2, 5), (5, 25))), (1, 25))
        self.assertEqual(rectangular_factors(((5, 10), (10, 25))), (5, 5))
        self.assertEqual(determinant(((2, 5), (5, 25))), 25)
        self.assertEqual(determinant(((5, 10), (10, 25))), 25)

    def test_modular_lattice_membership_against_literal_potentials(self):
        for f in DATA["fixtures"]:
            if f["columns"] > 3:
                continue
            a = realization(f["id"])
            for n in (2, 3, 4, 6):
                self.assertEqual(a.bicycles(n), lattice_bicycles(a.rows, n, a.columns))
                self.assertEqual(a.bicycles(n), literal_bicycles(a.rows, n, a.columns))

    def test_no_integral_signed_equivalence_even_with_column_permutation(self):
        a, b = realization("counterexample-a"), realization("counterexample-b")
        for p in permutations(range(2)):
            for signs in product((-1, 1), repeat=2):
                changed = tuple(tuple(signs[j] * row[p[j]] for j in range(2)) for row in a.rows)
                det = determinant(changed)
                inverse = ((Fraction(changed[1][1], det), Fraction(-changed[0][1], det)),
                           (Fraction(-changed[1][0], det), Fraction(changed[0][0], det)))
                u = matrix_product(b.rows, inverse)
                self.assertTrue(any(x.denominator != 1 for row in u for x in row))


if __name__ == "__main__":
    unittest.main()
