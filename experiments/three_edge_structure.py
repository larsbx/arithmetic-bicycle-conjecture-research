"""Independent exact tests for the nonparallel three-edge full-tower presentation.

A(a,b) = [[1,a,a+1],[0,b,b]], with primitive a and a+1.
This evidence is not theorem acceptance or an unrestricted invariance claim.
"""
from itertools import product
from math import gcd


def admissible(a, b):
    return type(a) is int and type(b) is int and b >= 2 and gcd(a, b) == gcd(a + 1, b) == 1


def literal_potentials(a, b, n):
    """Enumerate every potential; do not use Gram torsion."""
    if not admissible(a, b) or type(n) is not int or n < 2:
        raise ValueError("invalid parameter/modulus")
    result = set()
    for s, t in product(range(n), repeat=2):
        v = (s, (a * s + b * t) % n, ((a + 1) * s + b * t) % n)
        if ((v[0] + a * v[1] + (a + 1) * v[2]) % n == 0
                and b * (v[1] + v[2]) % n == 0):
            result.add(v)
    return result


def presented_edges(a, b, n):
    """Enumerate independent (s,u) cut+cycle congruences."""
    if not admissible(a, b) or type(n) is not int or n < 2:
        raise ValueError("invalid parameter/modulus")
    g = gcd(b, n)
    return {(s, u, (s + u) % n)
            for s, u in product(range(n), repeat=2)
            if (u - a * s) % g == 0
            and ((a + 2) * s + (2 * a + 1) * u) % n == 0
            and (b * (s + 2 * u)) % n == 0}


def gram_order(a, b, n):
    """Different oracle: 2x2 Gram Smith factors, quotient by potential kernel."""
    if not admissible(a, b) or type(n) is not int or n < 2:
        raise ValueError("invalid parameter/modulus")
    gram11 = 2 * (a * a + a + 1)
    gram12 = b * (2 * a + 1)
    gram22 = 2 * b * b
    d1 = gcd(gram11, gram12, gram22)
    d2 = 3 * b * b // d1
    assert (3 * b * b) % d1 == 0 and d2 % d1 == 0
    kernel_order = gcd(n, d1) * gcd(n, d2)
    assert kernel_order % gcd(n, b) == 0
    return kernel_order // gcd(n, b)


def group_exponent(group, n):
    """Compute the least annihilating integer; used only on finite sets."""
    return next(k for k in range(1, n + 1)
                if all(all(k * c % n == 0 for c in v) for v in group))


def audit():
    """Exact fixed, disclosed bounds; returns deterministic coverage."""
    count = 0
    for b in range(3, 14):
        for a in range(b):
            if not admissible(a, b):
                continue
            for n in (2, 3, 5, 7, 9, 14, 21, 27):
                literal = literal_potentials(a, b, n)
                presented = presented_edges(a, b, n)
                assert literal == presented, (a, b, n, "presentation")
                assert len(literal) == gram_order(a, b, n), (a, b, n, "Smith")
                count += 1

    exceptional = literal_potentials(1, 3, 9)
    assert len(exceptional) == 9
    assert group_exponent(exceptional, 9) == 3
    assert len(literal_potentials(1, 3, 3)) == 3
    v, w = (3, 3, 6), (0, 3, 3)
    generated = {tuple((i * v[k] + j * w[k]) % 9 for k in range(3))
                 for i, j in product(range(3), repeat=2)}
    assert generated == exceptional

    assert [(len(literal_potentials(a, 7, n)), gram_order(a, 7, n))
            for a, n in ((1, 7), (2, 7), (1, 14), (2, 14), (1, 49), (2, 49))] == [
                (1, 1), (7, 7), (1, 1), (7, 7), (7, 7), (7, 7)]
    return count


if __name__ == "__main__":
    print("PASS:", audit(), "literal/presentation/Smith comparisons")
