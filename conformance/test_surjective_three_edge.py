"""Bounded falsification, literal group and coherent tower checks."""
from itertools import combinations, product
from math import gcd
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kernel.arithmetic_matroid import smith_certificate
from kernel.surjective_bicycle import SurjectiveRepresentation
from oracles.arithmetic_matroid import arithmetic_signature
from oracles.regular_snf import literal_bicycles


def minors(a):
    return tuple(a[0][i]*a[1][j]-a[0][j]*a[1][i] for i,j in combinations(range(3),2))


def literal_edges(a,n):
    cuts={tuple(sum(a[i][j]*y[i] for i in range(2))%n for j in range(3))
          for y in product(range(n),repeat=2)}
    cycles={b for b in product(range(n),repeat=3)
            if all(sum(s*t for s,t in zip(row,b))%n==0 for row in a)}
    return cuts & cycles


class SurjectiveThreeEdgeTests(unittest.TestCase):
    def test_complete_box_matching_signatures(self):
        buckets={}
        count=0
        for v in product(range(-2,3),repeat=6):
            a=(v[:3],v[3:])
            ds=minors(a)
            if gcd(*ds)!=1:
                continue
            count+=1
            u,v=a
            x,y,z=sum(t*t for t in u),sum(s*t for s,t in zip(u,v)),sum(t*t for t in v)
            delta=sum(d*d for d in ds)
            self.assertEqual(x*z-y*y,delta)
            self.assertEqual(gcd(x,y,z),1)
            self.assertGreater(delta,0)
            self.assertEqual(smith_certificate(((x,y),(y,z))).factors,(1,delta))
            sig=arithmetic_signature(a)
            self.assertEqual(buckets.setdefault(sig,delta),delta)
        self.assertEqual(count,7176)

    def test_literal_cyclic_groups_and_towers(self):
        reps={}
        for v in product((-1,0,1),repeat=6):
            a=(v[:3],v[3:])
            if gcd(*minors(a))==1:
                reps.setdefault(arithmetic_signature(a),a)
        self.assertEqual(len(reps),10)
        # Last two have no unit maximal minor and Delta=49; same signature.
        extra=[((2,0,1),(0,3,1)),((2,3,2),(0,3,1))]
        self.assertEqual(arithmetic_signature(extra[0]),arithmetic_signature(extra[1]))
        for a in list(reps.values())+extra:
            s=SurjectiveRepresentation(a)
            delta=sum(d*d for d in minors(a))
            cert=smith_certificate(s.gram)
            def edge(n,t):
                g=gcd(n,delta)
                y=tuple(cert.right[i][1]*(n//g)*t for i in range(2))
                return tuple(x%n for x in s.gradient(y))
            cases=(2,3,4,6,7,14,49) if delta==49 else (2,3,4,6,8,12)
            for n in cases:
                g=gcd(n,delta)
                actual=literal_bicycles(a,n)
                self.assertEqual(actual,set(s.bicycles(n)))
                self.assertEqual(actual,{edge(n,t) for t in range(g)})
                self.assertEqual(len(actual),g)
                if n<=7:
                    self.assertEqual(actual,literal_edges(a,n))
                for t in range(g):
                    for u in range(g):
                        self.assertEqual(tuple((x+y)%n for x,y in zip(edge(n,t),edge(n,u))),
                                         edge(n,(t+u)%g))
            for n,m in product(cases,repeat=2):
                if m%n:
                    continue
                gn,gm,k=gcd(n,delta),gcd(m,delta),m//n
                self.assertEqual((k*gn)%gm,0)
                for t in range(gm):
                    reduced=tuple(x%n for x in edge(m,t))
                    self.assertEqual(reduced,edge(n,(k*gn//gm)*t))
                    self.assertEqual(reduced,s.reduce_bicycle(edge(m,t),m,n))
                for t in range(gn):
                    inflated=tuple(k*x%m for x in edge(n,t))
                    self.assertEqual(inflated,edge(m,(gm//gn)*t))
                    self.assertEqual(inflated,s.inflate_bicycle(edge(n,t),n,m))
            if delta==49:
                self.assertEqual({tuple(x%7 for x in edge(343,t)) for t in range(49)},
                                 {(0,0,0)})
                self.assertEqual(len(s.bicycles(7)),7)

    def test_fixed_cyclic_torsion_model(self):
        # Independent scalar model: exercise nontrivial maps and composition.
        for delta in (1,2,3,6,7,12,49):
            cases=(2,4,8,3,6,12,7,14,49,98,343)
            def phi(n,z):
                self.assertEqual(delta*z%n,0)
                return (delta*z//n)%delta
            for n in cases:
                h={z for z in range(n) if delta*z%n==0}
                target={d for d in range(delta) if n*d%delta==0}
                self.assertEqual({phi(n,z) for z in h},target)
                self.assertEqual(len(h),len(target))
                for m in cases:
                    if m%n:
                        continue
                    k=m//n
                    for z in range(m):
                        if delta*z%m==0:
                            self.assertEqual(phi(n,z%n),k*phi(m,z)%delta)
                    for z in h:
                        self.assertEqual(phi(m,k*z),phi(n,z))
                    for ell in cases:
                        if ell%m==0:
                            for z in h:
                                self.assertEqual((ell//m)*(k*z)%ell,(ell//n)*z%ell)

    def test_boundaries(self):
        with self.assertRaises(ValueError):
            SurjectiveRepresentation(((1,1,2),(0,7,7)))
        a=SurjectiveRepresentation(((1,0,1,0),(0,1,0,1)))
        self.assertEqual(a.gram,((2,0),(0,2)))
        self.assertEqual(len(a.bicycles(2)),4)

if __name__=='__main__':
    unittest.main()
