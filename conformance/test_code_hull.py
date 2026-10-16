"""Quotient-sensitive regressions and independent coordinate pairing checks."""

from itertools import combinations, product
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.realization_dependence import literal_code_hull, require
from kernel.code_hull import (
    CodeHull, HullIsometry, inverse_mod, matvec, orthogonal,
    reduction, scaled_inflation, transpose,
)


def coordinate_controls():
    fixtures = [
        ("signed-integral", ((1, 2), (0, 5)), ((1, 1), (0, 1)), ((0, -1), (1, 0)), [5, 10, 25]),
        ("redundant-signed", ((2, 2), (4, 4)), ((1, 0), (1, 1)), ((0, 1), (-1, 0)), [2, 4, 8]),
        ("finite-ring", ((1, 1),), ((1,),), ((2, 3), (3, -2)), [2, 3, 6, 12]),
        ("row-unit-only-mod-six", ((2, 2), (4, 4)), ((5, 0), (0, 1)), ((1, 0), (0, 1)), [6]),
    ]
    report = []
    for label, a, u, s, moduli in fixtures:
        maps = {}
        for n in moduli:
            h = CodeHull(a, n)
            f = HullIsometry(h, u, s)
            maps[n] = f
            vectors = list(product(range(n), repeat=h.columns))
            # Evaluate the pairing, independently of the matrix identity check.
            for x, z in product(vectors, repeat=2):
                sx, sz = matvec(s, x, n), matvec(s, z, n)
                require(sum(v * w for v, w in zip(x, z)) % n
                        == sum(v * w for v, w in zip(sx, sz)) % n, "pairing not preserved")
            require({f.edge(x) for x in h.hull} == literal_code_hull(f.target.rows, n)[2],
                    "transport differs from independent literal hull")
            require({f.quotient(y) for y in h.classes} == f.target.classes, "quotient transport not onto")
            for y in h.gram_kernel:
                q = f.quotient(y)
                require(f.target.project(q) == f.edge(h.project(y)), "coordinate square fails")
                require(q == f.quotient(h.class_of(y)), "coordinate map depends on representative")
                require(h.class_of(matvec(transpose(u, len(u)), q, n)) == h.class_of(y),
                        "inverse quotient transport fails")
            for x in h.hull:
                require(matvec(transpose(s, len(s)), f.edge(x), n) == x, "inverse edge transport fails")
        pairs = []
        for n, m in combinations(moduli, 2):
            if m % n:
                continue
            lo, hi = maps[n], maps[m]
            for y in hi.source.gram_kernel:
                require(lo.quotient(hi.source.reduce_class(y, n)) == hi.target.reduce_class(hi.quotient(y), n),
                        "coordinate/reduction quotient square fails")
            for y in lo.source.gram_kernel:
                require(hi.quotient(lo.source.inflate_class(y, m)) == lo.target.inflate_class(lo.quotient(y), m),
                        "coordinate/inflation quotient square fails")
            for x in hi.source.hull:
                require(lo.edge(reduction(x, m, n)) == reduction(hi.edge(x), m, n),
                        "coordinate/reduction edge square fails")
            for x in lo.source.hull:
                require(hi.edge(scaled_inflation(x, n, m)) == scaled_inflation(lo.edge(x), n, m),
                        "coordinate/inflation edge square fails")
            pairs.append([n, m])
        report.append({"id": label, "matrix": a, "row_map": u, "edge_map": s,
                       "moduli": moduli, "tower_pairs": pairs})
    return report


def negative_controls():
    a, b = ((1, 1), (0, 5)), ((1, 2), (0, 5))
    h, changed = CodeHull(a, 5), CodeHull(b, 5)
    require((len(h.hull), len(changed.hull)) == (1, 5), "lost shear obstruction")
    s = ((1, 0), (1, 1))
    require(not orthogonal(s, 5), "shear incorrectly accepted as orthogonal")
    # Transport the form as well: J' = S^{-T} S^{-1} = [[2,-1],[-1,1]].
    code = literal_code_hull(b, 5)[0]
    j = ((2, -1), (-1, 1))
    weighted_hull = {x for x in code if all(sum(v * w for v, w in zip(x, matvec(j, z, 5))) % 5 == 0
                                          for z in code)}
    require(weighted_hull == {matvec(s, x, 5) for x in h.hull}, "transported pairing fails")
    lo, hi = CodeHull(((2, 3),), 13), CodeHull(((2, 3),), 26)
    require((2, 3) in lo.hull and (2, 3) not in hi.hull and (4, 6) in hi.hull,
            "unscaled edge control lost")
    require((1,) in lo.gram_kernel and (1,) not in hi.gram_kernel and (2,) in hi.gram_kernel,
            "unscaled potential control lost")
    small, large = CodeHull(((1, 1),), 2), CodeHull(((1, 1),), 4)
    require({large.reduce_class(y, 2) for y in large.classes} < small.classes,
            "lost nonsurjective quotient reduction")
    scalar = CodeHull(((2,),), 4)
    require((len(scalar.gram_kernel), len(scalar.cut_kernel), len(scalar.classes)) == (4, 2, 2),
            "quotient denominator control lost")
    # Orthogonality at 12 does not imply a single integral tower isometry.
    finite = ((2, 3), (3, -2))
    require(orthogonal(finite, 12) and not orthogonal(finite) and not orthogonal(finite, 5),
            "fixed-ring versus integral distinction lost")
    return {"shear_standard_hull_orders_mod5": [1, 5], "shear_transported_hull_order_mod5": len(weighted_hull),
            "unscaled_edge": [2, 3], "unscaled_potential": [1], "small": 13, "large": 26,
            "reduction_4_to_2_not_surjective": True, "scalar2_mod4_kernel_denominator_quotient": [4, 2, 2],
            "mod12_isometry_not_integral_or_mod5": True}


class CodeHullTests(unittest.TestCase):
    def test_finite_coordinate_controls(self):
        self.assertEqual(len(coordinate_controls()), 4)

    def test_negative_controls(self):
        self.assertEqual(negative_controls()["shear_standard_hull_orders_mod5"], [1, 5])

    def test_all_listed_quotient_and_tower_fixtures(self):
        from conformance.replay_code_hull import evidence
        result = evidence()
        self.assertEqual(result["summary"]["matrices"], 11)

    def test_reject_invalid_domains(self):
        for n in (True, 4.0, 1, 0, -2):
            with self.assertRaises(ValueError):
                CodeHull(((2,),), n)
        for rows, width in ((((True,),), None), (((1,), (1, 2)), None), ((), -1)):
            with self.assertRaises(ValueError):
                CodeHull(rows, 4, width)
        h = CodeHull(((2, 3),), 26)
        for y in ((1,), (True,), (1, 2), (1.0,)):
            with self.assertRaises(ValueError):
                h.class_of(y)
        with self.assertRaises(ValueError):
            h.lift((2, 3))
        for function in (reduction, scaled_inflation):
            with self.assertRaises(ValueError):
                function((0,), 4, 6)
        with self.assertRaises(ValueError):
            HullIsometry(CodeHull(((1, 1),), 5), ((1,),), ((1, 1), (0, 1)))
        with self.assertRaises(ValueError):
            HullIsometry(CodeHull(((1, 1),), 6), ((2,),), ((1, 0), (0, 1)))
        with self.assertRaises(ValueError):
            HullIsometry(CodeHull(((1, 1),), 5), ((1,),), ((1,),))

    def test_composite_inverse_without_unit_pivot(self):
        a = ((2, 3), (3, 2))  # No entry is a unit mod 6, determinant -5 is.
        self.assertEqual(inverse_mod(a, 6), a)

    def test_empty_coordinate_witness(self):
        f = HullIsometry(CodeHull((), 4, 0), (), ())
        self.assertEqual(f.quotient(()), ())
        self.assertEqual(f.edge(()), ())

    def test_incoherent_witnesses_do_not_commute(self):
        lo = HullIsometry(CodeHull(((2, 3),), 13), ((1,),), ((1, 0), (0, 1)))
        hi = HullIsometry(CodeHull(((2, 3),), 26), ((1,),), ((-1, 0), (0, -1)))
        self.assertNotEqual(hi.edge(scaled_inflation((2, 3), 13, 26)),
                            scaled_inflation(lo.edge((2, 3)), 13, 26))

    def test_iterable_representatives_are_consumed_once(self):
        lo, hi = CodeHull(((2, 3),), 13), CodeHull(((2, 3),), 26)
        self.assertEqual(lo.project(iter([1])), (2, 3))
        self.assertEqual(lo.inflate_class(iter([1]), 26), (2,))
        self.assertEqual(hi.reduce_class(iter([2]), 13), (2,))
        self.assertEqual(lo.inflate_edge(iter([2, 3]), 26), (4, 6))
        self.assertEqual(hi.reduce_edge(iter([4, 6]), 13), (4, 6))
        f = HullIsometry(lo, ((-1,),), ((0, -1), (1, 0)))
        self.assertEqual(f.potential(iter([1])), (12,))
        self.assertEqual(f.edge(iter([2, 3])), (10, 2))
        self.assertEqual(reduction(iter([27]), 26, 13), (1,))
        self.assertEqual(scaled_inflation(iter([14]), 13, 26), (2,))


if __name__ == "__main__":
    unittest.main()
