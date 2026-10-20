"""Direct checks of the boundary claims, without representation uniqueness."""

from itertools import product
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kernel.arithmetic_matroid import IntegralRealization
from kernel.surjective_bicycle import SurjectiveRepresentation
from oracles.arithmetic_matroid import arithmetic_signature, lattice_bicycles
from oracles.regular_snf import determinant, literal_bicycles


class Phase6Boundaries(unittest.TestCase):
    def test_square_modular_kernels(self):
        # Exhaust every bounded unimodular matrix and every modular vector.
        count = 0
        for v in product((-1, 0, 1), repeat=4):
            a = (v[:2], v[2:])
            if abs(determinant(a)) != 1:
                continue
            count += 1
            for n in (2, 3, 4, 6):
                kernel = {b for b in product(range(n), repeat=2)
                          if all(sum(x*y for x, y in zip(row, b)) % n == 0 for row in a)}
                self.assertEqual(kernel, {(0, 0)})
                self.assertEqual(lattice_bicycles(a, n), {(0, 0)})
        self.assertEqual(count, 40)
        with self.assertRaises(ValueError):
            SurjectiveRepresentation(((1, 2), (0, 5)))
        self.assertEqual(len(lattice_bicycles(((1, 2), (0, 5)), 5)), 5)

    def test_rank_one_all_bounded_signs(self):
        count = 0
        for row in product(range(-2, 3), repeat=3):
            if not any(row):
                continue
            a = (row,)
            signature = arithmetic_signature(a)
            source = {n: literal_bicycles(a, n) for n in (2, 3, 4, 6)}
            for signs in product((-1, 1), repeat=3):
                ap = (tuple(s*x for s, x in zip(signs, row)),)
                self.assertEqual(arithmetic_signature(ap), signature)
                self.assertEqual(IntegralRealization(ap).signature, signature)
                for n, bicycles in source.items():
                    mapped = {tuple(s*x % n for s, x in zip(signs, b)) for b in bicycles}
                    self.assertEqual(mapped, literal_bicycles(ap, n))
                count += 1
        self.assertEqual(count, 992)
        self.assertNotEqual(arithmetic_signature(((0, 1),)), arithmetic_signature(((1, 1),)))

    def test_nontrivial_rank_one_and_tower_signs(self):
        a, ap = ((2, 3, 0),), ((-2, 3, 0),)
        sign = lambda b, n: (-b[0] % n, b[1] % n, b[2] % n)
        source = {n: lattice_bicycles(a, n) for n in (2, 4, 6, 13, 26)}
        self.assertEqual(len(source[13]), 13)
        for n, bicycles in source.items():
            self.assertEqual({sign(b, n) for b in bicycles}, literal_bicycles(ap, n))
            for m, larger in source.items():
                if m <= n or m % n:
                    continue
                for b in larger:
                    self.assertEqual(sign(tuple(x % n for x in b), n),
                                     tuple(x % n for x in sign(b, m)))
                for b in bicycles:
                    self.assertEqual(sign(tuple((m//n)*x for x in b), m),
                                     tuple((m//n)*x % m for x in sign(b, n)))


if __name__ == '__main__':
    unittest.main()
