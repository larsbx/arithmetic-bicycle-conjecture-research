"""Bounded independent tests for the ABC-RD-01 triangular-family draft.

Never imports Gram-torsion formulae, accepted proof-state APIs, or a
non-surjective realization equivalence oracle.
"""

import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.triangular_family import (
    literal_bic, predicted_bic, run_checks, tower_map,
)


class TriangularFamilyTests(unittest.TestCase):
    def test_literal_potential_enumeration_and_coherent_tower_maps(self):
        self.assertEqual(
            run_checks(),
            {
                "literal_formula_cases": 1988,
                "equal_class_parameter_pairs": 155,
                "tower_map_instances": 6200,
                "index5": {
                    1: {5: 1, 10: 1, 25: 5},
                    2: {5: 5, 10: 5, 25: 5},
                },
                "index13": {
                    1: {13: 1, 26: 1, 169: 13},
                    2: {13: 1, 26: 1, 169: 13},
                },
            },
        )

    def test_negative_control_equal_arithmetic_data_different_bicycles(self):
        self.assertEqual(len(literal_bic(1, 5, 5)), 1)
        self.assertEqual(len(literal_bic(2, 5, 5)), 5)
        self.assertEqual(len(literal_bic(1, 5, 10)), 1)
        self.assertEqual(len(literal_bic(2, 5, 10)), 5)
        self.assertEqual(len(literal_bic(1, 5, 25)), 5)
        self.assertEqual(len(literal_bic(2, 5, 25)), 5)

    def test_equal_class_nonidentical_ambient_realizations(self):
        for n in (13, 26, 169):
            src = literal_bic(1, 13, n)
            dst = literal_bic(2, 13, n)
            self.assertEqual({tower_map(v, 2, n) for v in src}, dst)
            self.assertEqual(len(src), {13: 1, 26: 1, 169: 13}[n])
            self.assertEqual(len(predicted_bic(1, 13, n)), len(src))

    def test_prime_power_cyclic_group_annihilator_count(self):
        for n in (4, 8, 9, 25, 27, 49, 169):
            for b, a in ((5, 2), (7, 3), (13, 2)):
                src = literal_bic(a, b, n)
                for d in range(1, n + 1):
                    if n % d != 0:
                        continue
                    annihilated = sum(all(d * coordinate % n == 0 for coordinate in v)
                                     for v in src)
                    self.assertEqual(annihilated, math.gcd(d, len(src)))

    def test_reject_boolean_and_invalid_moduli(self):
        for n in (True, 1, 0, -2):
            with self.assertRaises(ValueError):
                literal_bic(1, 5, n)
            with self.assertRaises(ValueError):
                predicted_bic(1, 5, n)


if __name__ == "__main__":
    unittest.main()
