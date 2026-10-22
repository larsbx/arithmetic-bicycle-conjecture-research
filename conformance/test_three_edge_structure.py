"""Independent regression for 3-edge full-tower subgroup and group structure."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from experiments.three_edge_structure import (
    admissible, literal_potentials, presented_edges,
    gram_order, group_exponent, audit,
)


class ThreeEdgeStructureTests(unittest.TestCase):
    def test_full_module_presentation_and_smith_order(self):
        self.assertEqual(audit(), 256)

    def test_noncyclic_prime_power_group(self):
        group = literal_potentials(1, 3, 9)
        self.assertEqual(group, presented_edges(1, 3, 9))
        self.assertEqual(len(group), gram_order(1, 3, 9))
        self.assertEqual(len(group), 9)
        self.assertEqual(group_exponent(group, 9), 3)
        self.assertEqual(len(literal_potentials(1, 3, 3)), 3)
        self.assertNotEqual(group_exponent(group, 9), len(group))

    def test_composite_orders_and_negative_pair(self):
        self.assertEqual([gram_order(1, 7, n) for n in (7, 14, 49)], [1, 1, 7])
        self.assertEqual([gram_order(2, 7, n) for n in (7, 14, 49)], [7, 7, 7])

    def test_parameter_guards(self):
        self.assertFalse(admissible(True, 7))
        self.assertFalse(admissible(1, 2))
        for n in (True, 0, 1, -3):
            with self.assertRaises(ValueError):
                literal_potentials(1, 7, n)
            with self.assertRaises(ValueError):
                presented_edges(1, 7, n)
            with self.assertRaises(ValueError):
                gram_order(1, 7, n)


if __name__ == "__main__":
    unittest.main()
