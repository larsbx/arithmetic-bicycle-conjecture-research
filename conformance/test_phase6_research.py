"""Exact nonparallel ABC negative controls and source-pinned evidence replay."""
from math import gcd
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiments.three_edge_family import (
    bicycles, independent_edges, matrix, signature, transition, evidence,
)
from conformance.replay_phase6_research import derive, canonical, RECEIPT

class Phase6BeyondTriangularTests(unittest.TestCase):
    def test_complete_labeled_signature(self):
        wanted=[[0,1],[1,1],[1,1],[2,7],[1,1],[2,7],[2,7],[2,7]]
        self.assertEqual(signature(1,7),wanted)
        self.assertEqual(signature(2,7),wanted)
        for a in (1,2):
            A=matrix(a,7)
            self.assertNotEqual(A[0][0]*A[1][1]-A[1][0]*A[0][1],0)

    def test_nonparallel_realization_dependence(self):
        self.assertEqual([len(bicycles(1,7,n)) for n in (2,7,14,49)],
                         [1,1,1,7])
        self.assertEqual([len(bicycles(2,7,n)) for n in (2,7,14,49)],
                         [1,7,7,7])
        self.assertEqual(gcd(7,2*(1+1+1)),1)
        self.assertEqual(gcd(7,2*(1+2+4)),7)

    def test_literal_potentials_independent_edges(self):
        for a in (1,2):
            for n in (2,7,14):
                self.assertEqual(bicycles(a,7,n),independent_edges(a,7,n))

    def test_reduction_and_scaled_inflation(self):
        for a in (1,2):
            for n,m in ((2,14),(7,14),(7,49)):
                low=bicycles(a,7,n)
                high=bicycles(a,7,m)
                self.assertTrue(transition(high,n,m,"reduce") <= low)
                self.assertTrue(transition(low,n,m,"inflate") <= high)

    def test_exploration_is_bounded(self):
        e=evidence()
        self.assertEqual(e["claim_promotions"],[])
        self.assertEqual([x["b"] for x in e["bounded_census"]],[5,7,9,11,13])

    def test_pin_and_canonical_receipt(self):
        report=derive()
        self.assertEqual(report["authority"],"non_authoritative_experiment")
        self.assertEqual(report["claim_promotions"],[])
        self.assertEqual(canonical(report),RECEIPT.read_text())

    def test_invalid_inputs(self):
        for n in (True,1,0,-1):
            with self.assertRaises(ValueError):
                bicycles(1,7,n)
        for a,b in ((1,2),(0,7),(6,7)):
            with self.assertRaises(ValueError):
                matrix(a,b)

if __name__=="__main__":
    unittest.main()
