"""Independent exact evidence for regular-matroid tower independence."""

from collections import defaultdict
from itertools import product
import json
from pathlib import Path
import unittest

from kernel.regular_bicycle import TURepresentation
from kernel.regular_equivalence import TUEquivalence, find_tu_equivalence
from oracles.regular_equivalence import brute_equivalence, matroid_signature
from oracles.regular_snf import (
    cycle_bicycles, determinant, gram_matrix, integral_cramer_inverse,
    is_totally_unimodular, literal_bicycles, quotient_key,
    quotient_representatives, smith_invariants,
)

DATA = json.loads((Path(__file__).parent / "fixtures/regular-representation-v1.json").read_text())


def pair(f):
    return TURepresentation(f["source"], f["columns"]), TURepresentation(f["target"], f["columns"])


class RepresentationWitnessTests(unittest.TestCase):
    def test_fixture_witnesses_against_all_subset_ranks_and_brute_sign_search(self):
        for f in DATA["pairs"]:
            with self.subTest(pair=f["id"]):
                a, ap = pair(f)
                p = f["permutation"]
                aligned = tuple(tuple(row[j] for j in p) for row in a.rows)
                self.assertEqual(matroid_signature(aligned, a.columns), matroid_signature(ap.rows, ap.columns))
                oracle = brute_equivalence(a.rows, ap.rows, p, a.columns)
                self.assertIsNotNone(oracle)
                independent = TUEquivalence(a, ap, oracle["permutation"], oracle["signs"], oracle["row_change"])
                w = find_tu_equivalence(a, ap, p)
                self.assertEqual(w.permutation, tuple(p))
                self.assertEqual(abs(determinant(w.row_change)), 1)
                self.assertEqual(smith_invariants(a.gram), smith_invariants(ap.gram))
                for n in f["moduli"]:
                    bikes = cycle_bicycles(a.rows, n, a.columns)
                    target = cycle_bicycles(ap.rows, n, ap.columns)
                    self.assertEqual({w.transport_bicycle(b, n) for b in bikes}, target)
                    self.assertEqual({independent.transport_bicycle(b, n) for b in bikes}, target)

    def test_changed_basis_fixtures_change_gram_coordinates(self):
        for f in DATA["pairs"]:
            if "normalizing_basis" not in f:
                continue
            a, ap = pair(f)
            basis = f["normalizing_basis"]
            c = tuple(tuple(row[j] for j in basis) for row in a.rows)
            inverse = integral_cramer_inverse(c)
            normalized = tuple(tuple(sum(inverse[i][k] * a.rows[k][j] for k in range(a.rank))
                                     for j in range(a.columns)) for i in range(a.rank))
            expected = tuple(tuple((-1) ** j * row[f["permutation"][j]] for j in range(a.columns))
                             for row in normalized)
            self.assertEqual(ap.rows, expected)
            self.assertTrue(is_totally_unimodular(normalized))
            self.assertNotEqual(gram_matrix(a.rows), gram_matrix(ap.rows))

    def test_all_ternary_representations_in_seven_labeled_matroid_buckets(self):
        buckets = defaultdict(list)
        for v in product((-1, 0, 1), repeat=6):
            rows = (v[:3], v[3:])
            if is_totally_unimodular(rows) and determinant(gram_matrix(rows)):
                buckets[matroid_signature(rows)].append(TURepresentation(rows))
        self.assertEqual(len(buckets), 7)
        self.assertEqual(sum(map(len, buckets.values())), 456)
        for group in buckets.values():
            source = group[0]
            for target in group:
                w = find_tu_equivalence(source, target)
                self.assertIsNotNone(brute_equivalence(source.rows, target.rows))
                for n in (2, 3, 4, 6):
                    oracle = cycle_bicycles(target.rows, n)
                    self.assertEqual({w.transport_bicycle(b, n) for b in cycle_bicycles(source.rows, n)}, oracle)
        representatives = [group[0] for group in buckets.values()]
        for a in representatives:
            for ap in representatives:
                if a == ap:
                    continue
                self.assertIsNone(brute_equivalence(a.rows, ap.rows))
                with self.assertRaises(ValueError):
                    find_tu_equivalence(a, ap)

    def test_invalid_witnesses_domains_and_label_bijections(self):
        a = TURepresentation(((1, -1),))
        for p, s, u in (((0, 0), (1, 1), ((1,),)),
                        ((False, 1), (1, 1), ((1,),)),
                        ((0, 1), (1, 0), ((1,),)),
                        ((0, 1), (True, 1), ((1,),)),
                        ((0, 1), (1, 1), ((2,),)),
                        ((0, 1), (1, 1), ((1.0,),)),
                        ((1, 0), (1, 1), ((1,),))):
            with self.assertRaises(ValueError):
                TUEquivalence(a, a, p, s, u)
        w = find_tu_equivalence(a, a)
        for n in (0, 1, -2, True, 2.0):
            with self.assertRaises(ValueError):
                w.transport_bicycle((0, 0), n)
        for b in ((0,), (0.0, 0), (True, 0), (1, 0)):
            with self.assertRaises(ValueError):
                w.transport_bicycle(b, 2)
        with self.assertRaises(ValueError):
            w.divisor_action((0, 0))
        with self.assertRaises(ValueError):
            w.divisor_action((True,))
        with self.assertRaises(ValueError):
            find_tu_equivalence(a, TURepresentation(((1,),)))
        with self.assertRaises(ValueError):
            find_tu_equivalence(a.rows, a)
        with self.assertRaises(ValueError):
            w.then(find_tu_equivalence(TURepresentation(((1, 1),)), TURepresentation(((1, 1),))))
        # A sign flip on only one entry of a chordless support cycle makes a minor 2.
        bad = ((1, 0, 0, 1, 1, 0), (0, 1, 0, 0, 1, 1), (0, 0, 1, 1, 0, 1))
        self.assertFalse(is_totally_unimodular(bad))
        with self.assertRaises(ValueError):
            TURepresentation(bad)

    def test_identical_smith_data_does_not_certify_labeled_matroid_equality(self):
        a = TURepresentation(((1, 1, 0),))
        ap = TURepresentation(((1, 0, 1),))
        self.assertEqual(a.gram, ap.gram)
        self.assertNotEqual(matroid_signature(a.rows), matroid_signature(ap.rows))
        self.assertIsNone(brute_equivalence(a.rows, ap.rows))
        with self.assertRaises(ValueError):
            find_tu_equivalence(a, ap)
        p = (0, 2, 1)  # A prescribed relabeling restores the matroid isomorphism.
        self.assertEqual(find_tu_equivalence(a, ap, p).permutation, p)


class RepresentationTowerTests(unittest.TestCase):
    def test_forward_inverse_squares_and_integral_divisor_representatives(self):
        for f in DATA["pairs"]:
            a, ap = pair(f)
            w = find_tu_equivalence(a, ap, f["permutation"])
            inverse = w.inverse()
            classes = quotient_representatives(a.gram)
            target_classes = quotient_representatives(ap.gram)
            images = {quotient_key(ap.gram, w.divisor_action(d)) for d in classes.values()}
            self.assertEqual(images, set(target_classes))
            z = tuple((-1) ** j * 2 ** (70 + j) for j in range(a.rank))
            for n in f["moduli"]:
                source_bikes = cycle_bicycles(a.rows, n, a.columns)
                for b in source_bikes:
                    transformed = w.transport_bicycle(iter(b), n)
                    self.assertEqual(inverse.transport_bicycle(transformed, n), b)
                    d = a.bicycle_to_divisor(b, n)
                    new_d = w.divisor_action(d)
                    self.assertEqual(quotient_key(ap.gram, ap.bicycle_to_divisor(transformed, n)),
                                     quotient_key(ap.gram, new_d))
                    self.assertEqual(ap.divisor_to_bicycle(new_d, n), transformed)
                    shifted = tuple(x + y for x, y in zip(d, a.gram_action(z)))
                    self.assertEqual(quotient_key(ap.gram, w.divisor_action(shifted)),
                                     quotient_key(ap.gram, new_d))
                    lifted = tuple(x + n * 2 ** (80 + j) for j, x in enumerate(b))
                    self.assertEqual(w.transport_bicycle(lifted, n), transformed)
                for key, d in classes.items():
                    if all(n * x % 1 == 0 for x in key):
                        self.assertEqual(w.transport_bicycle(a.divisor_to_bicycle(d, n), n),
                                         ap.divisor_to_bicycle(w.divisor_action(d), n))

    def test_both_modulus_maps_and_every_fixture_chain(self):
        for f in DATA["pairs"]:
            a, ap = pair(f)
            w = find_tu_equivalence(a, ap, f["permutation"])
            modules = {n: cycle_bicycles(a.rows, n, a.columns) for n in f["moduli"]}
            for n in modules:
                for m in modules:
                    if m <= n or m % n:
                        continue
                    for b in modules[m]:
                        self.assertEqual(w.transport_bicycle(a.reduce_bicycle(b, m, n), n),
                                         ap.reduce_bicycle(w.transport_bicycle(b, m), m, n))
                    for b in modules[n]:
                        self.assertEqual(w.transport_bicycle(a.inflate_bicycle(b, n, m), m),
                                         ap.inflate_bicycle(w.transport_bicycle(b, n), n, m))
                    for ell in modules:
                        if ell <= m or ell % m:
                            continue
                        for b in modules[ell]:
                            via = ap.reduce_bicycle(w.transport_bicycle(a.reduce_bicycle(b, ell, m), m), m, n)
                            self.assertEqual(via, w.transport_bicycle(a.reduce_bicycle(b, ell, n), n))
                        for b in modules[n]:
                            via = ap.inflate_bicycle(w.transport_bicycle(a.inflate_bicycle(b, n, m), m), m, ell)
                            self.assertEqual(via, w.transport_bicycle(a.inflate_bicycle(b, n, ell), ell))

    def test_nontrivial_witness_composition_inverse_and_identity(self):
        f = next(f for f in DATA["pairs"] if f["id"] == "triangle-row-and-label-change")
        a, ap = pair(f)
        first = find_tu_equivalence(a, ap, f["permutation"])
        p = (2, 1, 0)
        app = TURepresentation(tuple(tuple(-(-1) ** j * row[p[j]] for j in range(3)) for row in ap.rows))
        second = find_tu_equivalence(ap, app, p)
        composite = first.then(second)
        for n in (3, 4, 6, 9, 12):
            for b in cycle_bicycles(a.rows, n):
                value = composite.transport_bicycle(b, n)
                self.assertEqual(value, second.transport_bicycle(first.transport_bicycle(b, n), n))
                self.assertEqual(composite.inverse().transport_bicycle(value, n), b)
                self.assertEqual(first.then(first.inverse()).transport_bicycle(b, n), b)
            for d in quotient_representatives(a.gram).values():
                self.assertEqual(composite.divisor_action(d), second.divisor_action(first.divisor_action(d)))
                self.assertEqual(composite.inverse().divisor_action(composite.divisor_action(d)), d)

    def test_large_composite_modulus_without_potential_enumeration(self):
        f = next(f for f in DATA["pairs"] if f["id"] == "cographic-k33-alternate-basis")
        a, ap = pair(f)
        w = find_tu_equivalence(a, ap, f["permutation"])
        classes = quotient_representatives(a.gram)
        for n in (18, 36, 9 * 2 ** 80 * 5 ** 4):
            for key, d in classes.items():
                if all(n * x % 1 == 0 for x in key):
                    b = a.divisor_to_bicycle(d, n)
                    transformed = w.transport_bicycle(b, n)
                    self.assertEqual(transformed, ap.divisor_to_bicycle(w.divisor_action(d), n))
                    self.assertEqual(quotient_key(ap.gram, ap.bicycle_to_divisor(transformed, n)),
                                     quotient_key(ap.gram, w.divisor_action(d)))

    def test_edge_sets_and_comparison_maps_need_not_be_equal(self):
        a = TURepresentation(((1, 1, 1),))
        ap = TURepresentation(((1, 1, -1),))
        self.assertNotEqual(cycle_bicycles(a.rows, 3), cycle_bicycles(ap.rows, 3))
        w = find_tu_equivalence(a, ap)
        self.assertEqual({w.transport_bicycle(b, 3) for b in cycle_bicycles(a.rows, 3)}, cycle_bicycles(ap.rows, 3))
        identity = TUEquivalence(a, a, (0, 1, 2), (1, 1, 1), ((1,),))
        negative = TUEquivalence(a, a, (0, 1, 2), (-1, -1, -1), ((-1,),))
        self.assertNotEqual(identity.transport_bicycle((1, 1, 1), 3), negative.transport_bicycle((1, 1, 1), 3))
        self.assertEqual(identity.divisor_action((1,)), (1,))
        self.assertEqual(negative.divisor_action((1,)), (-1,))

    def test_non_tu_integer_representations_are_outside_the_regular_gate(self):
        a, ap = ((1, 1),), ((1, 2),)
        self.assertEqual(matroid_signature(a), matroid_signature(ap))
        self.assertEqual(len(literal_bicycles(a, 2)), 2)
        self.assertEqual(len(literal_bicycles(ap, 2)), 1)
        self.assertEqual(smith_invariants(gram_matrix(a)), (2,))
        self.assertEqual(smith_invariants(gram_matrix(ap)), (5,))
        with self.assertRaises(ValueError):
            TURepresentation(ap)
        with self.assertRaises(ValueError):
            brute_equivalence(a, ap)


if __name__ == "__main__":
    unittest.main()
