"""Candidate exact Gram/tower maps for integral surjections.

Surjectivity is certified in the declared lattice, not inferred from a
unit column basis or a rank calculation over one finite field.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from functools import cached_property, lru_cache
from itertools import product
from math import lcm

from kernel.arithmetic_matroid import IntegralRealization
from kernel.graph_bicycle import integer_vector, modulus
from kernel.regular_bicycle import rational_inverse


@dataclass(frozen=True)
class SurjectiveRepresentation:
    rows: tuple
    columns: int | None = None
    realization: IntegralRealization = field(init=False, repr=False)

    def __post_init__(self):
        a = IntegralRealization(self.rows, self.columns)
        if a.full_smith.factors != (1,) * len(a.rows):
            raise ValueError("columns must generate the declared ambient lattice: m(E)=1")
        object.__setattr__(self, "rows", a.rows)
        object.__setattr__(self, "columns", a.columns)
        object.__setattr__(self, "realization", a)

    @property
    def rank(self):
        return len(self.rows)

    @cached_property
    def right_inverse(self):
        # P A V = [I | 0], so T = V[:, :r] P and A T = I.
        certificate = self.realization.full_smith
        answer = tuple(tuple(sum(certificate.right[j][k] * certificate.left[k][i]
                                 for k in range(self.rank)) for i in range(self.rank))
                       for j in range(self.columns))
        if any(sum(self.rows[i][j] * answer[j][k] for j in range(self.columns)) != int(i == k)
               for i in range(self.rank) for k in range(self.rank)):
            raise ArithmeticError("Smith-derived right inverse does not split A")
        return answer

    @cached_property
    def gram(self):
        return tuple(tuple(sum(x * y for x, y in zip(row, other)) for other in self.rows)
                     for row in self.rows)

    def gradient(self, potential):
        y = integer_vector(potential, self.rank)
        return tuple(sum(self.rows[i][j] * y[i] for i in range(self.rank))
                     for j in range(self.columns))

    def divergence(self, edge_values):
        b = integer_vector(edge_values, self.columns)
        return tuple(sum(x * y for x, y in zip(row, b)) for row in self.rows)

    def gram_action(self, potential):
        return self.divergence(self.gradient(potential))

    def bicycle_potential(self, edge_values, n):
        modulus(n)
        b = tuple(x % n for x in integer_vector(edge_values, self.columns))
        if any(x % n for x in self.divergence(b)):
            raise ValueError("edge vector is not a modular cycle")
        y = tuple(sum(self.right_inverse[j][i] * b[j] for j in range(self.columns)) % n
                  for i in range(self.rank))
        if tuple(x % n for x in self.gradient(y)) != b:
            raise ValueError("edge vector is not a modular cut")
        return y

    def bicycle_to_divisor(self, edge_values, n, potential=None):
        b = integer_vector(edge_values, self.columns)
        y = self.bicycle_potential(b, n)
        if potential is not None:
            y = integer_vector(potential, self.rank)
        if tuple(x % n for x in self.gradient(y)) != tuple(x % n for x in b):
            raise ValueError("potential does not represent this bicycle")
        qy = self.gram_action(y)
        if any(x % n for x in qy):
            raise ArithmeticError("Gram image of a bicycle potential is not divisible by n")
        return tuple(x // n for x in qy)

    @cached_property
    def gram_inverse(self):
        return rational_inverse(self.gram)

    def rational_potential(self, divisor):
        d = integer_vector(divisor, self.rank)
        return tuple(sum((x * y for x, y in zip(row, d)), Fraction(0))
                     for row in self.gram_inverse)

    def class_key(self, divisor):
        return tuple(x % 1 for x in self.rational_potential(divisor))

    def class_order(self, divisor):
        return lcm(*(x.denominator for x in self.class_key(divisor)))

    def divisor_to_bicycle(self, divisor, n):
        modulus(n)
        d = integer_vector(divisor, self.rank)
        y = self.rational_potential(tuple(n * x for x in d))
        if any(x.denominator != 1 for x in y):
            raise ValueError("divisor class is not annihilated by modulus")
        y = tuple(int(x) for x in y)
        if self.gram_action(y) != tuple(n * x for x in d):
            raise ArithmeticError("inverse failed the full Gram equation")
        return tuple(x % n for x in self.gradient(y))

    def bicycles(self, n):
        modulus(n)
        return dict(self._bicycles(n))

    @lru_cache(maxsize=None)
    def _bicycles(self, n):
        return tuple((tuple(x % n for x in self.gradient(y)), y)
                     for y in product(range(n), repeat=self.rank)
                     if all(x % n == 0 for x in self.gram_action(y)))

    def reduce_bicycle(self, edge_values, m, n):
        modulus(m)
        modulus(n)
        if m % n:
            raise ValueError("target modulus must divide source modulus")
        b = integer_vector(edge_values, self.columns)
        self.bicycle_potential(b, m)
        return tuple(x % n for x in b)

    def inflate_bicycle(self, edge_values, n, m):
        modulus(n)
        modulus(m)
        if m % n:
            raise ValueError("source modulus must divide target modulus")
        b = integer_vector(edge_values, self.columns)
        self.bicycle_potential(b, n)
        return tuple((m // n) * x % m for x in b)
