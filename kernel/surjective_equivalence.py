"""Verified labeled integral equivalences for essential surjective realizations."""

from dataclasses import dataclass
from functools import cached_property
from itertools import combinations

from kernel.arithmetic_matroid import arithmetic_equal, comparison_permutation, multiply
from kernel.graph_bicycle import integer_vector, modulus
from kernel.regular_bicycle import integer_determinant, rational_inverse, rectangular_matrix
from kernel.surjective_bicycle import SurjectiveRepresentation


def compatible(source, target):
    if not isinstance(source, SurjectiveRepresentation) or not isinstance(target, SurjectiveRepresentation):
        raise ValueError("expected certified surjective representations")
    if source.rank != target.rank or source.columns != target.columns:
        raise ValueError("representations have different dimensions")


def integral(matrix):
    if any(x.denominator != 1 for row in matrix for x in row):
        raise ValueError("rational row change is not integral in the declared lattice")
    return tuple(tuple(int(x) for x in row) for row in matrix)


@dataclass(frozen=True)
class SurjectiveEquivalence:
    """Certify A'=U A S, with target j using signs[j] times source p[j]."""

    source: SurjectiveRepresentation
    target: SurjectiveRepresentation
    permutation: tuple
    signs: tuple
    row_change: tuple

    def __post_init__(self):
        compatible(self.source, self.target)
        p = comparison_permutation(self.permutation, self.source.columns)
        signs = integer_vector(self.signs, self.source.columns)
        if any(x not in (-1, 1) for x in signs):
            raise ValueError("column signs must be units +/-1")
        u, width = rectangular_matrix(self.row_change, self.source.rank)
        if len(u) != width or abs(integer_determinant(u)) != 1:
            raise ValueError("row change must be integral unimodular")
        changed = tuple(tuple(signs[j] * row[p[j]] for j in range(self.source.columns))
                        for row in self.source.rows)
        if multiply(u, changed, self.source.columns) != self.target.rows:
            raise ValueError("witness does not satisfy target = U source S")
        object.__setattr__(self, "permutation", p)
        object.__setattr__(self, "signs", signs)
        object.__setattr__(self, "row_change", u)

    def edge_action(self, edge_values):
        b = integer_vector(edge_values, self.source.columns)
        return tuple(self.signs[j] * b[self.permutation[j]] for j in range(self.source.columns))

    def divisor_action(self, divisor):
        d = integer_vector(divisor, self.source.rank)
        return tuple(sum(x * y for x, y in zip(row, d)) for row in self.row_change)

    @cached_property
    def row_inverse(self):
        return integral(rational_inverse(self.row_change))

    def potential_action(self, potential):
        y = integer_vector(potential, self.source.rank)
        return tuple(sum(self.row_inverse[j][i] * y[j] for j in range(self.source.rank))
                     for i in range(self.source.rank))

    def transport_bicycle(self, edge_values, n):
        modulus(n)
        b = integer_vector(edge_values, self.source.columns)
        self.source.bicycle_potential(b, n)
        answer = tuple(x % n for x in self.edge_action(b))
        self.target.bicycle_potential(answer, n)
        return answer

    def inverse(self):
        p = tuple(self.permutation.index(j) for j in range(self.source.columns))
        return SurjectiveEquivalence(self.target, self.source, p,
                                     tuple(self.signs[j] for j in p),
                                     self.row_inverse)

    def then(self, other):
        if not isinstance(other, SurjectiveEquivalence) or self.target != other.source:
            raise ValueError("equivalences have different intermediate representations")
        return SurjectiveEquivalence(
            self.source, other.target,
            tuple(self.permutation[j] for j in other.permutation),
            tuple(s * self.signs[j] for j, s in zip(other.permutation, other.signs)),
            multiply(other.row_change, self.row_change, self.source.rank),
        )


def find_surjective_equivalence(source, target, permutation=None):
    """Solve rational support signs, then verify integral unimodular equivalence.

    A common rational basis suffices; it need not be a unit minor.
    Arithmetic equality is checked on every labeled subset before searching.
    """
    compatible(source, target)
    rank, width = source.rank, source.columns
    p = comparison_permutation(permutation, width)
    if not arithmetic_equal(source.realization, target.realization, p):
        raise ValueError("label bijection does not preserve complete arithmetic data")
    if rank == 0:
        return SurjectiveEquivalence(source, target, p, (1,) * width, ())
    a = tuple(tuple(row[j] for j in p) for row in source.rows)
    basis = next(cc for cc in combinations(range(width), rank)
                 if integer_determinant(tuple(tuple(row[j] for j in cc) for row in a)))
    c = tuple(tuple(row[j] for j in basis) for row in a)
    cp = tuple(tuple(row[j] for j in basis) for row in target.rows)
    ci = rational_inverse(c)
    h = multiply(ci, a, width)
    hp = multiply(rational_inverse(cp), target.rows, width)
    if any(abs(h[i][j]) != abs(hp[i][j]) for i in range(rank) for j in range(width)):
        raise ValueError("normalized entry magnitudes disagree")
    adjacency = [[] for _ in range(rank + width)]
    for i in range(rank):
        for j in range(width):
            if j not in basis and h[i][j]:
                ratio = int(hp[i][j] / h[i][j])
                if ratio not in (-1, 1):
                    raise ArithmeticError("support ratio is not a sign")
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
                    raise ValueError("support ratios are inconsistent around a cycle")
    signs = [colors[rank + j] for j in range(width)]
    for i, j in enumerate(basis):
        signs[j] = colors[i]
    scaled = tuple(tuple(x * colors[k] for k, x in enumerate(row)) for row in cp)
    u = integral(multiply(scaled, ci, rank))
    return SurjectiveEquivalence(source, target, p, tuple(signs), u)
