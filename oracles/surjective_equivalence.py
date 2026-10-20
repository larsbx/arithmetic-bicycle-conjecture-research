"""Independent brute sign search using all-minor indices and Bareiss/Cramer.

No kernel imports, Smith transforms, support-graph signs, or unit-basis
assumption. The last rational basis is used, not the candidate's first.
"""

from fractions import Fraction
from itertools import combinations, product

from oracles.arithmetic_matroid import arithmetic_signature, rectangular_factors
from oracles.regular_snf import determinant, matrix_data


def cramer_inverse(matrix):
    denominator = determinant(matrix)
    if not denominator:
        raise ValueError("basis is singular")
    size = len(matrix)
    answer = [[Fraction(0)] * size for _ in range(size)]
    for rhs in range(size):
        for col in range(size):
            replaced = [list(row) for row in matrix]
            for row in range(size):
                replaced[row][col] = int(row == rhs)
            answer[col][rhs] = Fraction(determinant(replaced), denominator)
    return tuple(map(tuple, answer))


def brute_surjective_equivalence(source, target, permutation=None, columns=None):
    a, width = matrix_data(source, columns)
    ap, target_width = matrix_data(target, columns)
    if len(a) != len(ap) or width != target_width:
        raise ValueError("incompatible dimensions")
    p = tuple(range(width)) if permutation is None else tuple(permutation)
    if len(p) != width or any(type(x) is not int for x in p) or set(p) != set(range(width)):
        raise ValueError("invalid label bijection")
    if any(rectangular_factors(x, width) != (1,) * len(a) for x in (a, ap)):
        raise ValueError("oracle requires surjections in the declared lattices")
    aligned = tuple(tuple(row[j] for j in p) for row in a)
    if arithmetic_signature(aligned, width) != arithmetic_signature(ap, width):
        return None
    if not a:
        return {"permutation": p, "signs": (1,) * width, "row_change": ()}
    rank = len(a)
    basis = next(cc for cc in reversed(tuple(combinations(range(width), rank)))
                 if determinant([[row[j] for j in cc] for row in aligned]))
    c = tuple(tuple(row[j] for j in basis) for row in aligned)
    cp = tuple(tuple(row[j] for j in basis) for row in ap)
    inverse = cramer_inverse(c)
    for signs in product((-1, 1), repeat=width):
        u = tuple(tuple(sum(cp[i][k] * signs[basis[k]] * inverse[k][j] for k in range(rank))
                        for j in range(rank)) for i in range(rank))
        if any(x.denominator != 1 for row in u for x in row):
            continue
        u = tuple(tuple(int(x) for x in row) for row in u)
        if abs(determinant(u)) != 1:
            continue
        if tuple(tuple(signs[j] * sum(u[i][k] * aligned[k][j] for k in range(rank))
                       for j in range(width)) for i in range(rank)) == ap:
            return {"permutation": p, "signs": signs, "row_change": u}
    return None
