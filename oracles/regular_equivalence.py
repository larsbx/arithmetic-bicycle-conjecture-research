"""Independent all-subset matroid data and brute signed-equivalence oracle.

No kernel imports. Unit inverses use Bareiss/Cramer determinants; witness
search enumerates column signs rather than solving a support graph.
"""

from itertools import combinations, product

from oracles.regular_snf import (
    determinant, integral_cramer_inverse, is_totally_unimodular,
    last_unimodular_basis, matrix_data,
)


def rank_of_columns(rows, cols):
    for size in range(min(len(rows), len(cols)), 0, -1):
        for rr in combinations(range(len(rows)), size):
            for cc in combinations(cols, size):
                if determinant([[rows[i][j] for j in cc] for i in rr]):
                    return size
    return 0


def matroid_signature(rows, columns=None):
    a, width = matrix_data(rows, columns)
    return tuple(rank_of_columns(a, tuple(j for j in range(width) if mask >> j & 1))
                 for mask in range(1 << width))


def brute_equivalence(source, target, permutation=None, columns=None):
    a, width = matrix_data(source, columns)
    ap, target_width = matrix_data(target, columns)
    if len(a) != len(ap) or width != target_width:
        raise ValueError("incompatible matrix dimensions")
    p = tuple(range(width)) if permutation is None else tuple(permutation)
    if len(p) != width or any(type(x) is not int for x in p) or set(p) != set(range(width)):
        raise ValueError("invalid label bijection")
    if not is_totally_unimodular(a, width) or not is_totally_unimodular(ap, width):
        raise ValueError("oracle requires TU inputs")
    aligned = tuple(tuple(row[j] for j in p) for row in a)
    if matroid_signature(aligned, width) != matroid_signature(ap, width):
        return None
    if not a:
        return {"permutation": p, "signs": (1,) * width, "row_change": ()}
    basis = last_unimodular_basis(aligned, width)
    c = tuple(tuple(row[j] for j in basis) for row in aligned)
    cp = tuple(tuple(row[j] for j in basis) for row in ap)
    inverse = integral_cramer_inverse(c)
    rank = len(a)
    for signs in product((-1, 1), repeat=width):
        u = tuple(tuple(sum(cp[i][k] * signs[basis[k]] * inverse[k][j] for k in range(rank))
                        for j in range(rank)) for i in range(rank))
        if abs(determinant(u)) != 1:
            continue
        changed = tuple(tuple(signs[j] * sum(u[i][k] * aligned[k][j] for k in range(rank))
                              for j in range(width)) for i in range(rank))
        if changed == ap:
            return {"permutation": p, "signs": signs, "row_change": u}
    return None
