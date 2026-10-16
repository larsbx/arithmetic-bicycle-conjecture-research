"""Exact small-fixture code-hull quotients; no Python proof authority.

Arbitrary rectangular integer matrices, including redundant/empty rows.
Enumeration is exhaustive and exponential, with no silent size cap.
"""

from dataclasses import dataclass
from functools import cached_property
from itertools import product

from kernel.graph_bicycle import integer_vector, modulus
from kernel.regular_bicycle import integer_determinant, rectangular_matrix


def matvec(rows, vector, n):
    return tuple(sum(a * b for a, b in zip(row, vector)) % n for row in rows)


def transpose(rows, width):
    return tuple(tuple(row[j] for row in rows) for j in range(width))


def reduction(vector, large, small):
    modulus(large)
    modulus(small)
    if large % small:
        raise ValueError("reduction requires small dividing large")
    vector = tuple(vector)
    v = integer_vector(vector, len(vector))
    return tuple(x % small for x in v)


def scaled_inflation(vector, small, large):
    modulus(small)
    modulus(large)
    if large % small:
        raise ValueError("inflation requires small dividing large")
    vector = tuple(vector)
    v = integer_vector(vector, len(vector))
    return tuple((large // small) * x % large for x in v)


def orthogonal(rows, n=None):
    """Check S^T S = I, over integers or at the supplied modulus."""
    a, width = rectangular_matrix(rows)
    if len(a) != width:
        raise ValueError("coordinate matrix must be square")
    if n is not None:
        modulus(n)
    defects = [sum(a[k][i] * a[k][j] for k in range(width)) - int(i == j)
               for i in range(width) for j in range(width)]
    return all(x == 0 if n is None else x % n == 0 for x in defects)


def inverse_mod(rows, n):
    """Adjugate inverse over Z/n; no field Gaussian-elimination shortcut."""
    modulus(n)
    a, size = rectangular_matrix(rows)
    if len(a) != size:
        raise ValueError("row map must be square")
    unit = pow(integer_determinant(a), -1, n)
    return tuple(tuple(
        unit * (-1) ** (i + j) * integer_determinant(
            tuple(tuple(a[r][c] for c in range(size) if c != i)
                  for r in range(size) if r != j)) % n
        for j in range(size)) for i in range(size))


@dataclass(frozen=True)
class CodeHull:
    rows: tuple
    n: int
    columns: int | None = None

    def __post_init__(self):
        modulus(self.n)
        rows, width = rectangular_matrix(self.rows, self.columns)
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "columns", width)

    def cut(self, potential):
        y = integer_vector(potential, len(self.rows))
        return matvec(transpose(self.rows, self.columns), y, self.n)

    @cached_property
    def gram(self):
        return tuple(tuple(sum(a * b for a, b in zip(row, other))
                           for other in self.rows) for row in self.rows)

    @cached_property
    def gram_kernel(self):
        return frozenset(y for y in product(range(self.n), repeat=len(self.rows))
                         if not any(matvec(self.gram, y, self.n)))

    @cached_property
    def cut_kernel(self):
        return frozenset(y for y in product(range(self.n), repeat=len(self.rows))
                         if not any(self.cut(y)))

    def class_of(self, potential):
        """Lexicographically least representative of y + ker(A^T)."""
        y = tuple(x % self.n for x in integer_vector(potential, len(self.rows)))
        if any(matvec(self.gram, y, self.n)):
            raise ValueError("potential is outside the Gram kernel")
        return min(tuple((a + b) % self.n for a, b in zip(y, z))
                   for z in self.cut_kernel)

    @cached_property
    def classes(self):
        return frozenset(self.class_of(y) for y in self.gram_kernel)

    @cached_property
    def hull(self):
        return frozenset(self.cut(y) for y in self.gram_kernel)

    def project(self, potential):
        potential = integer_vector(potential, len(self.rows))
        self.class_of(potential)  # Validate the restricted map's domain.
        return self.cut(potential)

    def lift(self, edge):
        x = tuple(v % self.n for v in integer_vector(edge, self.columns))
        for y in sorted(self.classes):
            if self.cut(y) == x:
                return y
        raise ValueError("edge is outside the hull")

    def at(self, n):
        return CodeHull(self.rows, n, self.columns)

    def reduce_class(self, potential, small):
        potential = integer_vector(potential, len(self.rows))
        self.class_of(potential)
        return self.at(small).class_of(reduction(potential, self.n, small))

    def inflate_class(self, potential, large):
        potential = integer_vector(potential, len(self.rows))
        self.class_of(potential)
        return self.at(large).class_of(scaled_inflation(potential, self.n, large))

    def reduce_edge(self, edge, small):
        edge = integer_vector(edge, self.columns)
        self.lift(edge)
        answer = reduction(edge, self.n, small)
        self.at(small).lift(answer)
        return answer

    def inflate_edge(self, edge, large):
        edge = integer_vector(edge, self.columns)
        self.lift(edge)
        answer = scaled_inflation(edge, self.n, large)
        self.at(large).lift(answer)
        return answer


@dataclass(frozen=True)
class HullIsometry:
    """A' = U A S^T, x' = Sx, [y'] = [U^{-T}y], at one modulus.

    Tower use requires coherent witnesses at every compared modulus.
    A fixed integral unimodular U and signed permutation S suffice.
    """

    source: CodeHull
    row_map: tuple
    edge_map: tuple

    def __post_init__(self):
        u, _ = rectangular_matrix(self.row_map, len(self.source.rows))
        s, _ = rectangular_matrix(self.edge_map, self.source.columns)
        if len(u) != len(self.source.rows) or len(s) != self.source.columns:
            raise ValueError("coordinate witness dimensions disagree")
        inverse_mod(u, self.source.n)
        if not orthogonal(s, self.source.n):
            raise ValueError("edge map does not preserve the standard pairing")
        object.__setattr__(self, "row_map", u)
        object.__setattr__(self, "edge_map", s)

    @cached_property
    def target(self):
        a, u, s = self.source.rows, self.row_map, self.edge_map
        rows = tuple(tuple(sum(u[i][k] * a[k][l] * s[j][l]
                               for k in range(len(a)) for l in range(self.source.columns))
                           for j in range(self.source.columns)) for i in range(len(a)))
        return CodeHull(rows, self.source.n, self.source.columns)

    def potential(self, y):
        y = integer_vector(y, len(self.source.rows))
        self.source.class_of(y)
        inv_t = transpose(inverse_mod(self.row_map, self.source.n), len(self.row_map))
        return matvec(inv_t, y, self.source.n)

    def quotient(self, y):
        return self.target.class_of(self.potential(y))

    def edge(self, x):
        x = integer_vector(x, self.source.columns)
        self.source.lift(x)
        answer = matvec(self.edge_map, x, self.source.n)
        self.target.lift(answer)
        return answer
