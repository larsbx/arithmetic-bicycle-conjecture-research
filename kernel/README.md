# Kernel

`graph_bicycle.py` implements candidate exact graph maps, normalized-potential
enumeration, and critical-group coordinates using integer arithmetic and
`fractions.Fraction`. Its graph inputs are finite connected undirected
multigraphs; its modulus inputs are arbitrary integers at least two.

The integral theorem in `proof/graph-modular-bicycle.md` supplies proof
authority. Python remains a candidate language without acceptance authority
under `ESTATE.toml`; executable results are checked against the independent
oracle and source-pinned conformance receipts.

`regular_bicycle.py` implements candidate maps for a fixed full-row-rank
TU matrix. It verifies every square minor, constructs an integral right
inverse from a unit column basis, and uses exact rational Gram coordinates.
It handles rank zero, loops, and arbitrary composite moduli. The separate
integral proof in `proof/regular-modular-bicycle.md` supplies authority.
TU recognition and enumeration are intended for small fixtures.

`regular_equivalence.py` finds and verifies an integral unimodular row
change and signed column map for a prescribed label bijection between
certified TU matrices. Its witnesses transport bicycles and Gram divisor
classes, compose, and invert. It verifies the entire integer matrix
equation before returning a witness. Its deterministic sign choice does
not assert mathematical canonicity.

`arithmetic_matroid.py` computes verified rectangular Smith certificates
and complete rank/index signatures for essential integral realizations
in a declared ambient lattice. It compares every labeled subset and
enumerates literal bicycle modules with duplicate cuts removed. It does
not apply the fixed-TU Gram map to nonsurjective realizations.

Arithmetic data equality and realization equivalence are separate
questions. The rank-two counterexample has equal signatures and different
bicycle orders. Scalable module algorithms remain future work.

`surjective_bicycle.py` certifies m(E)=1 for an essential integer
realization in its declared ambient lattice. Its integral right inverse
comes from both Smith transformations, so a unit maximal minor is not
required. Exact Gram maps, class coordinates, and both modulus maps work
for every integer modulus at least two.

`surjective_equivalence.py` compares complete labeled arithmetic data,
normalizes a rational basis, solves support sign ratios, and certifies
an integral unimodular row/sign equivalence. Witnesses act on edges,
potentials, and divisors and support inversion and composition. They
transport the whole tower; their deterministic selection does not make
the comparison map canonical. The principal counterexample is outside
the surjective domain, and the unrestricted claims remain retracted.
