"""Exact small-fixture TU equivalence witnesses and compatible tower maps."""

from dataclasses import dataclass

from kernel.graph_bicycle import integer_vector, modulus
from kernel.regular_bicycle import (
    TURepresentation, integer_determinant, rational_inverse, rectangular_matrix,
)


def permutation_data(values, width):
    values = tuple(range(width)) if values is None else tuple(values)
    if len(values) != width or any(type(x) is not int for x in values) or set(values) != set(range(width)):
        raise ValueError("expected a permutation of source column indices")
    return values


def multiply(a, b):
    if not a:
        return ()
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def integral(matrix):
    if any(x.denominator != 1 for row in matrix for x in row):
        raise ArithmeticError("unit-basis calculation became nonintegral")
    return tuple(tuple(int(x) for x in row) for row in matrix)


def compatible_inputs(source, target):
    if not isinstance(source, TURepresentation) or not isinstance(target, TURepresentation):
        raise ValueError("expected certified full-row-rank TU representations")
    if source.rank != target.rank or source.columns != target.columns:
        raise ValueError("representations have different dimensions")


@dataclass(frozen=True)
class TUEquivalence:
    """A verified A'=U A S witness; target column j uses source permutation[j]."""

    source: TURepresentation
    target: TURepresentation
    permutation: tuple
    signs: tuple
    row_change: tuple

    def __post_init__(self):
        compatible_inputs(self.source, self.target)
        p = permutation_data(self.permutation, self.source.columns)
        s = integer_vector(self.signs, self.source.columns)
        if any(x not in (-1, 1) for x in s):
            raise ValueError("column signs must be units +/-1")
        u, width = rectangular_matrix(self.row_change, self.source.rank)
        if len(u) != width or abs(integer_determinant(u)) != 1:
            raise ValueError("row change must be integral unimodular")
        changed = tuple(tuple(s[j] * self.source.rows[i][p[j]] for j in range(self.source.columns))
                        for i in range(self.source.rank))
        if multiply(u, changed) != self.target.rows:
            raise ValueError("witness does not satisfy target = U source S")
        object.__setattr__(self, "permutation", p)
        object.__setattr__(self, "signs", s)
        object.__setattr__(self, "row_change", u)

    def edge_action(self, edge_values):
        b = integer_vector(edge_values, self.source.columns)
        return tuple(sign * b[j] for j, sign in zip(self.permutation, self.signs))

    def divisor_action(self, divisor):
        d = integer_vector(divisor, self.source.rank)
        return tuple(sum(x * y for x, y in zip(row, d)) for row in self.row_change)

    def transport_bicycle(self, edge_values, n):
        modulus(n)
        b = integer_vector(edge_values, self.source.columns)
        self.source.bicycle_potential(b, n)
        value = tuple(x % n for x in self.edge_action(b))
        self.target.bicycle_potential(value, n)
        return value

    def inverse(self):
        p = tuple(self.permutation.index(j) for j in range(self.source.columns))
        s = tuple(self.signs[j] for j in p)
        u = integral(rational_inverse(self.row_change))
        return TUEquivalence(self.target, self.source, p, s, u)

    def then(self, other):
        if not isinstance(other, TUEquivalence) or self.target != other.source:
            raise ValueError("equivalence witnesses have different intermediate representations")
        p = tuple(self.permutation[j] for j in other.permutation)
        s = tuple(sign * self.signs[j] for j, sign in zip(other.permutation, other.signs))
        u = multiply(other.row_change, self.row_change)
        return TUEquivalence(self.source, other.target, p, s, u)


def find_tu_equivalence(source, target, permutation=None):
    """Find a witness for a prescribed label bijection, or reject exactly.

    Normalized support ratios are solved on a bipartite graph. Final
    integral determinant and matrix-identity verification are mandatory.
    All TU inputs have already been certified by TURepresentation.
    """
    compatible_inputs(source, target)
    width, rank = source.columns, source.rank
    p = permutation_data(permutation, width)
    if rank == 0:
        return TUEquivalence(source, target, p, (1,) * width, ())
    aligned = tuple(tuple(row[j] for j in p) for row in source.rows)
    basis = tuple(j for j in range(width) if p[j] in source.basis)
    c = tuple(tuple(row[j] for j in basis) for row in aligned)
    cp = tuple(tuple(row[j] for j in basis) for row in target.rows)
    if abs(integer_determinant(cp)) != 1:
        raise ValueError("label bijection does not preserve a basis")
    inverse = rational_inverse(c)
    h = integral(multiply(inverse, aligned))
    hp = integral(multiply(rational_inverse(cp), target.rows))
    if any((h[i][j] == 0) != (hp[i][j] == 0) for i in range(rank) for j in range(width)):
        raise ValueError("label bijection does not preserve fundamental-circuit supports")
    if any(abs(x) > 1 for matrix in (h, hp) for row in matrix for x in row):
        raise ArithmeticError("TU unit-basis normal form is not TU-valued")
    adjacency = [[] for _ in range(rank + width)]
    for i in range(rank):
        for j in range(width):
            if j not in basis and h[i][j]:
                ratio = h[i][j] * hp[i][j]
                adjacency[i].append((rank + j, ratio))
                adjacency[rank + j].append((i, ratio))
    colors = [None] * len(adjacency)
    for root in range(len(adjacency)):
        if colors[root] is not None:
            continue
        colors[root], pending = 1, [root]
        for vertex in pending:
            for neighbor, ratio in adjacency[vertex]:
                expected = colors[vertex] * ratio
                if colors[neighbor] is None:
                    colors[neighbor] = expected
                    pending.append(neighbor)
                elif colors[neighbor] != expected:
                    raise ValueError("support sign ratios are inconsistent around a cycle")
    signs = [colors[rank + j] for j in range(width)]
    for i, j in enumerate(basis):
        signs[j] = colors[i]
    scaled_cp = tuple(tuple(x * colors[j] for j, x in enumerate(row)) for row in cp)
    u = integral(multiply(scaled_cp, inverse))
    return TUEquivalence(source, target, p, tuple(signs), u)
