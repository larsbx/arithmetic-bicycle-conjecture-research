#!/usr/bin/env python3
"""Independent bounded cross-check of nonsurjective triangular ABC bicycles.

A(a,b)=[[1,a],[0,b]], b>=2, gcd(a,b)=1.  At modulus n,
g=gcd(b,n), q=n/g, c=1+a*a.  Bic_n(A) is in bijection with
k in Z/g satisfying c*q*k=0 (mod g), via
k -> (-a*q*k, q*k) (mod n).  Thus its order is gcd(g,c*q).

At fixed b, two full towers are additively equivalent iff
gcd(b,1+a*a) agrees; the second-coordinate map commutes with
reduction and scaled inflation. These are *not* claims of ambient
pairing-preserving equivalence. This script never imports repository
kernels or a nonsurjective Gram-torsion oracle.

No finite enumeration promotes a research claim to proved.
"""

from math import gcd


def literal_bic(a, b, n):
    """Enumerate all potentials independently of the derived formula."""
    if not all(type(x) is int for x in (a, b, n)) or b < 2 or n < 2:
        raise ValueError("integers required, with b>=2 and n>=2")
    return {
        (s, (a * s + b * t) % n)
        for s in range(n)
        for t in range(n)
        if (s + a * (a * s + b * t)) % n == 0
        and (b * (a * s + b * t)) % n == 0
    }


def predicted_bic(a, b, n):
    """Exact subgroup presentation; also a separate check of members."""
    if not all(type(x) is int for x in (a, b, n)) or b < 2 or n < 2:
        raise ValueError("integers required, with b>=2 and n>=2")
    g = gcd(b, n)
    q = n // g
    c = 1 + a * a
    return {
        ((-a * q * k) % n, (q * k) % n)
        for k in range(g)
        if c * q * k % g == 0
    }


def tower_map(edge, ap, n):
    """Map the bicycle subgroup to parameter ap, leaving z unchanged."""
    return (-ap * edge[1] % n, edge[1] % n)


def run_checks():
    """Return deterministic counts after exact bounded comparisons."""
    modulus_checks = 0
    for b in range(2, 16):
        for a in range(b):
            if gcd(a, b) != 1:
                continue
            for n in range(2, 30):
                actual = literal_bic(a, b, n)
                expected = predicted_bic(a, b, n)
                assert actual == expected, (a, b, n)
                g = gcd(b, n)
                assert len(actual) == gcd(g, (1 + a * a) * (n // g))
                modulus_checks += 1

    compared_pairs = tower_checks = 0
    for b in range(2, 15):
        primitive = [a for a in range(b) if gcd(a, b) == 1]
        for i, a in enumerate(primitive):
            for ap in primitive[i + 1:]:
                if gcd(b, 1 + a * a) != gcd(b, 1 + ap * ap):
                    continue
                compared_pairs += 1
                for n in range(2, 33):
                    src, target = literal_bic(a, b, n), literal_bic(ap, b, n)
                    assert {tower_map(v, ap, n) for v in src} == target
                    for scale in (2, 3, 4):
                        m = n * scale
                        if m > 40:
                            continue
                        big_src = literal_bic(a, b, m)
                        big_target = literal_bic(ap, b, m)
                        assert {tower_map(v, ap, m) for v in big_src} == big_target
                        def reduce(v):
                            return (v[0] % n, v[1] % n)
                        def inflate(v):
                            return (scale * v[0] % m, scale * v[1] % m)
                        assert all(tower_map(reduce(v), ap, n)
                                   == reduce(tower_map(v, ap, m)) for v in big_src)
                        assert all(tower_map(inflate(v), ap, m)
                                   == inflate(tower_map(v, ap, n)) for v in src)
                        tower_checks += 1

    index5 = {
        a: {n: len(literal_bic(a, 5, n)) for n in (5, 10, 25)}
        for a in (1, 2)
    }
    assert index5 == {
        1: {5: 1, 10: 1, 25: 5},
        2: {5: 5, 10: 5, 25: 5},
    }

    index13 = {
        a: {n: len(literal_bic(a, 13, n)) for n in (13, 26, 169)}
        for a in (1, 2)
    }
    assert index13 == {
        1: {13: 1, 26: 1, 169: 13},
        2: {13: 1, 26: 1, 169: 13},
    }
    return {
        "literal_formula_cases": modulus_checks,
        "equal_class_parameter_pairs": compared_pairs,
        "tower_map_instances": tower_checks,
        "index5": index5,
        "index13": index13,
    }


def main():
    results = run_checks()
    assert results["literal_formula_cases"] == 1988
    assert results["equal_class_parameter_pairs"] == 155
    assert results["tower_map_instances"] == 6200
    print("PASS: triangular-family bounded independent checks")
    for key, value in results.items():
        print(key, value)


if __name__ == "__main__":
    main()
