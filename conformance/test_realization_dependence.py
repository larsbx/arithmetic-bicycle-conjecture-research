"""Negative controls for pairing, module exponents, and tower conventions."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.realization_dependence import annihilator_profile, literal_code_hull
from kernel.arithmetic_matroid import IntegralRealization, arithmetic_equal


class RealizationDependenceControls(unittest.TestCase):
    def test_general_edge_basis_change_does_not_preserve_the_coordinate_hull(self):
        # Right multiplication by [[1,1],[0,1]] is unimodular, but it
        # changes the pairing unless the form is transported as well.
        a = ((1, 1), (0, 5))
        transformed = tuple((row[0], row[0] + row[1]) for row in a)
        self.assertEqual(transformed, ((1, 2), (0, 5)))
        self.assertTrue(arithmetic_equal(IntegralRealization(a), IntegralRealization(transformed)))
        self.assertEqual(len(literal_code_hull(a, 5)[2]), 1)
        self.assertEqual(len(literal_code_hull(transformed, 5)[2]), 5)

    def test_equal_orders_do_not_determine_a_prime_power_module(self):
        cyclic = literal_code_hull(((1, 1, 1, 1),), 4)[2]
        klein = literal_code_hull(((1, 1, 0, 0), (0, 0, 1, 1)), 4)[2]
        self.assertEqual(len(cyclic), 4)
        self.assertEqual(len(klein), 4)
        self.assertEqual(annihilator_profile(cyclic, 4), {"1": 1, "2": 2, "4": 4})
        self.assertEqual(annihilator_profile(klein, 4), {"1": 1, "2": 4, "4": 4})

    def test_inflation_requires_scaling(self):
        source = literal_code_hull(((2, 3),), 13)[2]
        target = literal_code_hull(((2, 3),), 26)[2]
        self.assertIn((2, 3), source)
        self.assertNotIn((2, 3), target)
        self.assertIn((4, 6), target)
        self.assertEqual({tuple(2 * x for x in v) for v in source}, target)


if __name__ == "__main__":
    unittest.main()
