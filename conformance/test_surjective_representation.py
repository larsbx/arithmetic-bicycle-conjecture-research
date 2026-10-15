"""Exact positive and negative regressions for the explicitly surjective theorem."""

from dataclasses import replace
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import json
from math import gcd, lcm, prod
from pathlib import Path
import unittest

from kernel.arithmetic_matroid import IntegralRealization, arithmetic_equal, multiply
from kernel.regular_bicycle import TURepresentation
from kernel.surjective_bicycle import SurjectiveRepresentation
from kernel.surjective_equivalence import SurjectiveEquivalence, find_surjective_equivalence
from oracles.arithmetic_matroid import arithmetic_signature, lattice_bicycles, rectangular_factors
from oracles.regular_snf import (
    determinant, gram_matrix, literal_bicycles, quotient_key,
    quotient_representatives, smith_invariants,
)
from oracles.surjective_equivalence import brute_surjective_equivalence

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "conformance/fixtures/surjective-representation-v1.json").read_text())


@lru_cache(maxsize=None)
def edges(rows, width, n):
    return frozenset(lattice_bicycles(rows, n, width))


def edge_order(b, n):
    return lcm(*(n // gcd(n, x) for x in b))


class SurjectiveRepresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pairs = []
        for f in DATA["pairs"]:
            a, ap = (SurjectiveRepresentation(f[k], f["columns"]) for k in ("source", "target"))
            cls.pairs.append((f, a, ap, find_surjective_equivalence(a, ap, f["permutation"])))

    def test_smith_right_inverse_without_a_unit_basis(self):
        no_unit = []
        for f, a, ap, _ in self.pairs:
            for x in (a, ap):
                self.assertEqual(rectangular_factors(x.rows, x.columns), (1,) * x.rank)
                self.assertTrue(all(type(v) is int for row in x.right_inverse for v in row))
                self.assertEqual(multiply(x.rows, x.right_inverse, x.rank),
                                 tuple(tuple(int(i == j) for j in range(x.rank)) for i in range(x.rank)))
            minors = [abs(determinant([[row[j] for j in cc] for row in a.rows]))
                      for cc in combinations(range(a.columns), a.rank)]
            self.assertEqual(1 not in minors, f["no_unit_basis"])
            if f["no_unit_basis"]:
                no_unit.append(f["id"])
                self.assertEqual(gcd(*minors), 1)
        self.assertEqual(no_unit, ["rank-one-no-unit-basis", "rank-two-no-unit-basis", "disconnected-loop"])
        self.assertEqual([abs(determinant([[row[j] for j in cc] for row in self.pairs[4][1].rows]))
                          for cc in combinations(range(3), 2)], [6, 2, 3])

    def test_complete_arithmetic_data_and_independent_witnesses(self):
        for f, a, ap, w in self.pairs:
            self.assertTrue(arithmetic_equal(a.realization, ap.realization, f["permutation"]))
            aligned = tuple(tuple(row[j] for j in w.permutation) for row in a.rows)
            self.assertEqual(arithmetic_signature(aligned, a.columns),
                             arithmetic_signature(ap.rows, ap.columns))
            other = brute_surjective_equivalence(a.rows, ap.rows, w.permutation, a.columns)
            self.assertIsNotNone(other)
            SurjectiveEquivalence(a, ap, other["permutation"], other["signs"], other["row_change"])
            self.assertEqual(abs(determinant(w.row_change)), 1)
        for i in (3, 4, 5, 6, 7, 8):
            with self.assertRaises(ValueError):
                TURepresentation(self.pairs[i][1].rows)
        with self.assertRaises(ValueError):
            TURepresentation(self.pairs[9][2].rows)

    def test_literal_edges_smith_counts_and_order_profiles(self):
        for f, a, ap, _ in self.pairs:
            self.assertEqual(smith_invariants(a.gram), tuple(f["gram_smith"]))
            self.assertEqual(smith_invariants(ap.gram), tuple(f["gram_smith"]))
            for n in f["moduli"]:
                for x in (a, ap):
                    expected = edges(x.rows, x.columns, n)
                    self.assertEqual(set(x.bicycles(n)), expected)
                    self.assertEqual(literal_bicycles(x.rows, n, x.columns), expected)
                    self.assertEqual(len(expected), prod(gcd(n, s) for s in f["gram_smith"]))
                    classes = quotient_representatives(x.gram)
                    torsion = {key for key in classes if all((n * v).denominator == 1 for v in key)}
                    self.assertEqual(len(torsion), len(expected))
                    self.assertEqual(sorted(edge_order(b, n) for b in expected),
                                     sorted(lcm(*(v.denominator for v in key)) for key in torsion))

    def test_both_inverse_directions_on_all_fixture_classes(self):
        for f, a, ap, _ in self.pairs:
            for x in (a, ap):
                classes = quotient_representatives(x.gram)
                for n in f["moduli"]:
                    observed = set()
                    for b in edges(x.rows, x.columns, n):
                        d = x.bicycle_to_divisor(b, n)
                        self.assertEqual(x.divisor_to_bicycle(d, n), b)
                        observed.add(quotient_key(x.gram, d))
                    for key, d in classes.items():
                        if all((n * v).denominator == 1 for v in key):
                            b = x.divisor_to_bicycle(d, n)
                            self.assertIn(b, edges(x.rows, x.columns, n))
                            self.assertEqual(quotient_key(x.gram, x.bicycle_to_divisor(b, n)), key)
                            self.assertIn(key, observed)
                        else:
                            with self.assertRaises(ValueError):
                                x.divisor_to_bicycle(d, n)

    def test_representative_independence_and_linearity(self):
        for f, a, _, _ in self.pairs:
            z = tuple((-1) ** i * (10**30 + i) for i in range(a.rank))
            for n in f["moduli"]:
                bicycles = sorted(edges(a.rows, a.columns, n))
                for b in bicycles:
                    y = a.bicycle_potential(b, n)
                    d = a.bicycle_to_divisor(b, n)
                    lifted = tuple(v + n * w for v, w in zip(y, z))
                    self.assertEqual(a.bicycle_to_divisor(b, n, lifted),
                                     tuple(v + w for v, w in zip(d, a.gram_action(z))))
                    edge_lift = tuple(v + n * (10**20 + j) for j, v in enumerate(b))
                    self.assertEqual(a.class_key(a.bicycle_to_divisor(edge_lift, n)), a.class_key(d))
                    self.assertEqual(a.divisor_to_bicycle(tuple(v + w for v, w in zip(d, a.gram_action(z))), n), b)
                    self.assertEqual(a.class_order(d), edge_order(b, n))
                    self.assertEqual(a.class_key(a.bicycle_to_divisor(tuple(-7 * v for v in b), n)),
                                     a.class_key(tuple(-7 * v for v in d)))
                for b in bicycles:
                    for c in bicycles:
                        total = tuple((v + w) % n for v, w in zip(b, c))
                        d = tuple(v + w for v, w in zip(a.bicycle_to_divisor(b, n),
                                                       a.bicycle_to_divisor(c, n)))
                        self.assertEqual(a.class_key(a.bicycle_to_divisor(total, n)), a.class_key(d))

    def test_transport_potentials_and_both_gram_squares(self):
        for f, a, ap, w in self.pairs:
            for n in f["moduli"]:
                image = set()
                for b in edges(a.rows, a.columns, n):
                    bp = w.transport_bicycle(b, n)
                    image.add(bp)
                    self.assertEqual(w.inverse().transport_bicycle(bp, n), b)
                    y = a.bicycle_potential(b, n)
                    yp = w.potential_action(y)
                    self.assertEqual(tuple(v % n for v in ap.gradient(yp)), bp)
                    d = w.divisor_action(a.bicycle_to_divisor(b, n))
                    self.assertEqual(ap.divisor_to_bicycle(d, n), bp)
                    self.assertEqual(ap.class_key(ap.bicycle_to_divisor(bp, n)), ap.class_key(d))
                    self.assertEqual(ap.gram_action(yp), w.divisor_action(a.gram_action(y)))
                self.assertEqual(image, edges(ap.rows, ap.columns, n))

    def test_both_modulus_maps_and_all_fixture_chains(self):
        pairs, chains = 0, 0
        for f, a, ap, w in self.pairs:
            for n, m in product(f["moduli"], repeat=2):
                if m <= n or m % n:
                    continue
                pairs += 1
                k = m // n
                for b in edges(a.rows, a.columns, m):
                    small = a.reduce_bicycle(b, m, n)
                    self.assertEqual(a.class_key(a.bicycle_to_divisor(small, n)),
                                     a.class_key(tuple(k * x for x in a.bicycle_to_divisor(b, m))))
                    self.assertEqual(w.transport_bicycle(small, n),
                                     ap.reduce_bicycle(w.transport_bicycle(b, m), m, n))
                for b in edges(a.rows, a.columns, n):
                    large = a.inflate_bicycle(b, n, m)
                    self.assertEqual(a.class_key(a.bicycle_to_divisor(large, m)),
                                     a.class_key(a.bicycle_to_divisor(b, n)))
                    self.assertEqual(w.transport_bicycle(large, m),
                                     ap.inflate_bicycle(w.transport_bicycle(b, n), n, m))
            for n, m, ell in product(f["moduli"], repeat=3):
                if not n < m < ell or m % n or ell % m:
                    continue
                chains += 1
                for b in edges(a.rows, a.columns, ell):
                    self.assertEqual(a.reduce_bicycle(a.reduce_bicycle(b, ell, m), m, n),
                                     a.reduce_bicycle(b, ell, n))
                for b in edges(a.rows, a.columns, n):
                    self.assertEqual(a.inflate_bicycle(a.inflate_bicycle(b, n, m), m, ell),
                                     a.inflate_bicycle(b, n, ell))
        self.assertGreater(pairs, 25)
        self.assertGreater(chains, 2)

    def test_large_composite_moduli_without_potential_enumeration(self):
        _, a, ap, w = self.pairs[4]
        n, m, ell = 7, 49 * 2**40, 49 * 2**40 * 15
        for key, d in quotient_representatives(a.gram).items():
            b = a.divisor_to_bicycle(d, ell)
            self.assertEqual(a.class_key(a.bicycle_to_divisor(b, ell)), key)
            self.assertEqual(w.transport_bicycle(b, ell), ap.divisor_to_bicycle(w.divisor_action(d), ell))
            self.assertEqual(a.reduce_bicycle(a.reduce_bicycle(b, ell, m), m, n),
                             a.reduce_bicycle(b, ell, n))
            if all((n * v).denominator == 1 for v in key):
                small = a.divisor_to_bicycle(d, n)
                self.assertEqual(a.inflate_bicycle(a.inflate_bicycle(small, n, m), m, ell),
                                 a.inflate_bicycle(small, n, ell))

    def test_witness_composition_inverse_and_nonunique_maps(self):
        for f, a, ap, w in self.pairs:
            p = tuple(reversed(range(a.columns)))
            signs = tuple((-1) ** j for j in range(a.columns))
            third_rows = tuple(tuple(signs[j] * row[p[j]] for j in range(a.columns)) for row in ap.rows)
            third = SurjectiveRepresentation(third_rows, a.columns)
            v = find_surjective_equivalence(ap, third, p)
            composite = w.then(v)
            for b in a.bicycles(6):
                self.assertEqual(w.then(w.inverse()).transport_bicycle(b, 6), b)
                self.assertEqual(composite.transport_bicycle(b, 6), v.transport_bicycle(w.transport_bicycle(b, 6), 6))
        a = SurjectiveRepresentation(((2, 3),))
        identity = SurjectiveEquivalence(a, a, (0, 1), (1, 1), ((1,),))
        negative = SurjectiveEquivalence(a, a, (0, 1), (-1, -1), ((-1,),))
        b = a.divisor_to_bicycle((1,), 13)
        self.assertNotEqual(identity.transport_bicycle(b, 13), negative.transport_bicycle(b, 13))

    def test_composite_negatives_invisible_to_field_counts(self):
        a = SurjectiveRepresentation(((2, 0, 1), (0, 3, 1)))
        self.assertEqual(len(a.bicycles(7)), 7)
        self.assertEqual(len(a.bicycles(49)), 49)
        self.assertEqual(max(edge_order(b, 49) for b in a.bicycles(49)), 49)
        x = SurjectiveRepresentation(((2, 3),))
        self.assertTrue(all(x.reduce_bicycle(b, 169, 13) == (0, 0) for b in x.bicycles(169)))
        self.assertEqual(len(x.bicycles(13)), 13)
        b = next(b for b in x.bicycles(13) if b != (0, 0))
        self.assertNotIn(b, x.bicycles(169))
        # Dividing an arbitrary edge lift is not the Gram-potential map.
        b = (2, 3)
        self.assertEqual(x.bicycle_to_divisor(b, 13), (1,))
        self.assertNotEqual(x.divergence(b)[0] // 13, x.divergence((15, 3))[0] // 13)
        self.assertNotEqual(x.class_key((x.divergence(b)[0] // 13,)),
                            x.class_key((x.divergence((15, 3))[0] // 13,)))

    def test_existing_tu_specialization(self):
        data = json.loads((ROOT / "conformance/fixtures/regular-modular-bicycle-v1.json").read_text())
        for f in data["fixtures"]:
            tu = TURepresentation(f["matrix"], f["columns"])
            a = SurjectiveRepresentation(f["matrix"], f["columns"])
            for n in f["moduli"]:
                self.assertEqual(set(a.bicycles(n)), set(tu.bicycles(n)))
                for b in tu.bicycles(n):
                    self.assertEqual(a.bicycle_potential(b, n), tu.bicycle_potential(b, n))
                    d = a.bicycle_to_divisor(b, n)
                    self.assertEqual(a.class_key(d), tu.class_key(tu.bicycle_to_divisor(b, n)))
                    self.assertEqual(a.divisor_to_bicycle(d, n), b)

    def test_arithmetic_and_cycle_sign_negative_pairs(self):
        for f in DATA["negative_pairs"]:
            a, ap = (SurjectiveRepresentation(f[k], f["columns"]) for k in ("source", "target"))
            self.assertFalse(arithmetic_equal(a.realization, ap.realization, f["permutation"]))
            self.assertIsNone(brute_surjective_equivalence(a.rows, ap.rows, f["permutation"], a.columns))
            with self.assertRaises(ValueError):
                find_surjective_equivalence(a, ap, f["permutation"])
        a, b = DATA["negative_pairs"][1]["source"], DATA["negative_pairs"][1]["target"]
        self.assertEqual([[abs(v) for v in row] for row in a], [[abs(v) for v in row] for row in b])
        self.assertEqual(abs(determinant([row[3:] for row in a])), 25)
        self.assertEqual(abs(determinant([row[3:] for row in b])), 23)

    def test_nonsurjective_counterexample_remains_outside_domain(self):
        for f in DATA["out_of_domain"]:
            with self.assertRaises(ValueError):
                SurjectiveRepresentation(f["rows"], f["columns"])
            with self.assertRaises(ValueError):
                brute_surjective_equivalence(f["rows"], f["rows"], columns=f["columns"])
        a, ap = [IntegralRealization(f["rows"]) for f in DATA["out_of_domain"][1:]]
        self.assertTrue(arithmetic_equal(a, ap))
        self.assertEqual((len(a.bicycles(5)), len(ap.bicycles(5))), (1, 5))

    def test_invalid_representatives_domains_and_witnesses(self):
        a = SurjectiveRepresentation(((2, 3),))
        for rows, width in [(((1, 2), (2, 4)), 2), (((True,),), 1), (((1.0,),), 1), (((1,),), True)]:
            with self.assertRaises(ValueError):
                SurjectiveRepresentation(rows, width)
        # These vectors isolate cycle failure and cut failure modulo two.
        with self.assertRaisesRegex(ValueError, "cycle"):
            a.bicycle_potential((0, 1), 2)
        with self.assertRaisesRegex(ValueError, "cut"):
            a.bicycle_potential((1, 0), 2)
        b = a.divisor_to_bicycle((1,), 13)
        with self.assertRaises(ValueError):
            a.bicycle_to_divisor(b, 13, (0,))
        with self.assertRaises(ValueError):
            a.divisor_to_bicycle((1,), 2)
        # Warm caches first: bool and float equality must not bypass integer validation.
        a.bicycles(2)
        for bad in (True, 2.0, 1, 0, -2):
            for operation in (lambda: a.bicycles(bad), lambda: a.bicycle_potential((0, 0), bad),
                              lambda: a.divisor_to_bicycle((0,), bad)):
                with self.assertRaises(ValueError):
                    operation()
        for operation in (lambda: a.reduce_bicycle((0, 0), 6, 4),
                          lambda: a.inflate_bicycle((0, 0), 4, 6)):
            with self.assertRaises(ValueError):
                operation()
        w = SurjectiveEquivalence(a, a, (0, 1), (1, 1), ((1,),))
        for change in ({"permutation": (0, 0)}, {"signs": (1, 0)}, {"row_change": ((2,),)},
                       {"row_change": ((-1,),)}, {"row_change": ((Fraction(1),),)}):
            with self.assertRaises(ValueError):
                replace(w, **change)
        with self.assertRaises(ValueError):
            find_surjective_equivalence(a, a, (True, 0))
        with self.assertRaises(ValueError):
            find_surjective_equivalence(IntegralRealization(((2, 3),)), a)
        with self.assertRaises(ValueError):
            other = SurjectiveRepresentation(((1,),))
            w.then(SurjectiveEquivalence(other, other, (0,), (1,), ((1,),)))

    def test_complete_ternary_surjective_census(self):
        from conformance.replay_surjective_representation import census
        record = census()
        self.assertEqual(record["all_matrices"], 729)
        self.assertEqual(record["surjective_matrices"], 552)
        self.assertEqual(record["non_tu_matrices"], 96)
        self.assertEqual(record["arithmetic_buckets"], 10)
        self.assertEqual(record["modulus_cases"], 2208)
        self.assertEqual(record["cross_bucket_rejections"], 90)


if __name__ == "__main__":
    unittest.main()
