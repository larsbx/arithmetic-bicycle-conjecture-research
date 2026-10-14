"""Exact Smith certificates and essential torsion-free realization data.

All-subset arithmetic signatures are exhaustive small-fixture machinery.
They certify arithmetic-matroid equality, not realization equivalence.
"""

from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from itertools import product
import json
from math import prod

from kernel.graph_bicycle import modulus
from kernel.regular_bicycle import integer_determinant, rectangular_matrix


def identity(size):
    return tuple(tuple(int(i == j) for j in range(size)) for i in range(size))


def multiply(a, b, width):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(width))
                 for i in range(len(a)))


@dataclass(frozen=True)
class SmithCertificate:
    matrix: tuple
    columns: int
    left: tuple
    right: tuple
    diagonal: tuple

    def __post_init__(self):
        a, width = rectangular_matrix(self.matrix, self.columns)
        height = len(a)
        left, _ = rectangular_matrix(self.left, height)
        right, _ = rectangular_matrix(self.right, width)
        diagonal, _ = rectangular_matrix(self.diagonal, width)
        if len(left) != height or len(right) != width or len(diagonal) != height:
            raise ValueError("Smith certificate has incorrect matrix dimensions")
        if abs(integer_determinant(left)) != 1 or abs(integer_determinant(right)) != 1:
            raise ValueError("Smith transformations must be integral unimodular")
        if multiply(multiply(left, a, width), right, width) != diagonal:
            raise ValueError("Smith certificate does not satisfy left A right = diagonal")
        if any(x != 0 for i, row in enumerate(diagonal) for j, x in enumerate(row) if i != j):
            raise ValueError("Smith certificate is not diagonal")
        entries = tuple(diagonal[i][i] for i in range(min(height, width)))
        previous, zero_seen = 1, False
        for value in entries:
            if value == 0:
                zero_seen = True
            elif value < 0 or zero_seen or value % previous:
                raise ValueError("Smith factors must be positive, dividing, then zero")
            else:
                previous = value
        for name, value in (("matrix", a), ("columns", width), ("left", left),
                            ("right", right), ("diagonal", diagonal)):
            object.__setattr__(self, name, value)

    @property
    def factors(self):
        return tuple(self.diagonal[i][i] for i in range(min(len(self.matrix), self.columns))
                     if self.diagonal[i][i])

    @property
    def rank(self):
        return len(self.factors)

    @property
    def torsion_order(self):
        return prod(self.factors)


def smith_certificate(rows, columns=None):
    """Integer Euclidean reduction with both unimodular transforms tracked."""
    original, width = rectangular_matrix(rows, columns)
    height = len(original)
    a, left, right = list(map(list, original)), list(map(list, identity(height))), list(map(list, identity(width)))

    def swap_rows(i, j):
        a[i], a[j] = a[j], a[i]
        left[i], left[j] = left[j], left[i]

    def swap_columns(i, j):
        for matrix in (a, right):
            for row in matrix:
                row[i], row[j] = row[j], row[i]

    def add_row(target, source, coefficient):
        for matrix in (a, left):
            matrix[target] = [x + coefficient * y for x, y in zip(matrix[target], matrix[source])]

    def add_column(target, source, coefficient):
        for matrix in (a, right):
            for row in matrix:
                row[target] += coefficient * row[source]

    for k in range(min(height, width)):
        positions = [(i, j) for i in range(k, height) for j in range(k, width) if a[i][j]]
        if not positions:
            break
        i, j = min(positions, key=lambda ij: (abs(a[ij[0]][ij[1]]), ij))
        swap_rows(k, i)
        swap_columns(k, j)
        while True:
            row = next((i for i in range(k + 1, height) if a[i][k]), None)
            if row is not None:
                add_row(row, k, -(a[row][k] // a[k][k]))
                if a[row][k]:
                    swap_rows(row, k)
                continue
            col = next((j for j in range(k + 1, width) if a[k][j]), None)
            if col is not None:
                add_column(col, k, -(a[k][col] // a[k][k]))
                if a[k][col]:
                    swap_columns(col, k)
                continue
            bad = next(((i, j) for i in range(k + 1, height) for j in range(k + 1, width)
                        if a[i][j] % a[k][k]), None)
            if bad is None:
                break
            add_row(k, bad[0], 1)
        if a[k][k] < 0:
            a[k] = [-x for x in a[k]]
            left[k] = [-x for x in left[k]]
    return SmithCertificate(original, width, tuple(map(tuple, left)), tuple(map(tuple, right)), tuple(map(tuple, a)))


@dataclass(frozen=True)
class IntegralRealization:
    """An essential list of integer columns in the fixed ambient lattice Z^r."""

    rows: tuple
    columns: int | None = None
    full_smith: SmithCertificate = field(init=False)

    def __post_init__(self):
        rows, width = rectangular_matrix(self.rows, self.columns)
        certificate = smith_certificate(rows, width)
        if certificate.rank != len(rows):
            raise ValueError("realization must be essential: full row rank in its ambient lattice")
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "columns", width)
        object.__setattr__(self, "full_smith", certificate)

    @property
    def rank(self):
        return len(self.rows)

    def subset_smith(self, mask):
        if type(mask) is not int or not 0 <= mask < (1 << self.columns):
            raise ValueError("subset mask must be an integer in the ground-set range")
        return self._subset_smith(mask)

    @lru_cache(maxsize=None)
    def _subset_smith(self, mask):
        cols = tuple(j for j in range(self.columns) if mask >> j & 1)
        return smith_certificate(tuple(tuple(row[j] for j in cols) for row in self.rows), len(cols))

    @cached_property
    def signature(self):
        return tuple((c.rank, c.torsion_order) for c in
                     (self.subset_smith(mask) for mask in range(1 << self.columns)))

    def canonical_data(self):
        return {"schema": "abc-arithmetic-matroid-v1", "ambient_rank": self.rank,
                "ground_set_size": self.columns,
                "subsets": [{"mask": mask, "rank": rank, "multiplicity": str(m)}
                            for mask, (rank, m) in enumerate(self.signature)]}

    def canonical_encoding(self):
        return (json.dumps(self.canonical_data(), indent=2, sort_keys=True) + "\n").encode()

    def bicycles(self, n):
        modulus(n)  # Reject bool/float cache aliases before entering the cache.
        return self._bicycles(n)

    @lru_cache(maxsize=None)
    def _bicycles(self, n):
        cuts = set()
        for y in product(range(n), repeat=self.rank):
            b = tuple(sum(self.rows[i][j] * y[i] for i in range(self.rank)) % n for j in range(self.columns))
            if all(sum(row[j] * b[j] for j in range(self.columns)) % n == 0 for row in self.rows):
                cuts.add(b)
        return frozenset(cuts)


def comparison_permutation(permutation, width):
    p = tuple(range(width)) if permutation is None else tuple(permutation)
    if len(p) != width or any(type(x) is not int for x in p) or set(p) != set(range(width)):
        raise ValueError("expected a bijection from target labels to source labels")
    return p


def arithmetic_equal(source, target, permutation=None):
    if not isinstance(source, IntegralRealization) or not isinstance(target, IntegralRealization):
        raise ValueError("comparison requires validated essential lattice realizations")
    p = comparison_permutation(permutation, source.columns)
    if source.columns != target.columns or source.rank != target.rank:
        return False
    for mask in range(1 << target.columns):
        source_mask = sum(1 << p[j] for j in range(target.columns) if mask >> j & 1)
        if target.signature[mask] != source.signature[source_mask]:
            return False
    return True
