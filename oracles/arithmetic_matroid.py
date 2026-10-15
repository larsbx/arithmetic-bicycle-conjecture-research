"""Independent rectangular minor indices and modular lattice membership.

No kernel imports and no Euclidean Smith reduction. Modular cuts are
tested by lattice-index equality, valid over every composite modulus.
"""

from itertools import combinations, product
from math import gcd, prod

from oracles.graph_snf import determinant
from oracles.regular_snf import matrix_data


def minor_gcd(rows, size, width):
    value = 0
    for rr in combinations(range(len(rows)), size):
        for cc in combinations(range(width), size):
            value = gcd(value, abs(determinant([[rows[i][j] for j in cc] for i in rr])))
    return value


def rectangular_factors(rows, columns=None):
    a, width = matrix_data(rows, columns)
    factors, previous = [], 1
    for size in range(1, min(len(a), width) + 1):
        delta = minor_gcd(a, size, width)
        if not delta:
            break
        factor, remainder = divmod(delta, previous)
        if remainder or (factors and factor % factors[-1]):
            raise ArithmeticError("invalid determinantal-divisor chain")
        factors.append(factor)
        previous = delta
    return tuple(factors)


def arithmetic_signature(rows, columns=None):
    a, width = matrix_data(rows, columns)
    if len(rectangular_factors(a, width)) != len(a):
        raise ValueError("oracle requires an essential ambient lattice realization")
    signature = []
    for mask in range(1 << width):
        cols = tuple(j for j in range(width) if mask >> j & 1)
        factors = rectangular_factors(tuple(tuple(row[j] for j in cols) for row in a), len(cols))
        signature.append((len(factors), prod(factors)))
    return tuple(signature)


def lattice_bicycles(rows, n, columns=None):
    """Enumerate edge vectors; exact image membership uses [A^T | n I]."""
    if type(n) is not int or n < 2:
        raise ValueError("modulus must be an integer at least two")
    a, width = matrix_data(rows, columns)
    rank = len(a)
    generators = tuple(tuple(a[i][j] for i in range(rank)) +
                       tuple(n * int(j == k) for k in range(width)) for j in range(width))
    index = minor_gcd(generators, width, rank + width)
    if index < 1:
        raise ArithmeticError("modular image lattice is not full rank")
    answer = set()
    for b in product(range(n), repeat=width):
        if any(sum(row[j] * b[j] for j in range(width)) % n for row in a):
            continue
        extended = tuple(row + (b[j],) for j, row in enumerate(generators))
        if minor_gcd(extended, width, rank + width + 1) == index:
            answer.add(b)
    return answer
