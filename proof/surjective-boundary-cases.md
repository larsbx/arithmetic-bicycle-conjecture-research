# Direct boundary cases for Phase 6

Claims: **ABC-SURJECTIVE-SQUARE-TRIVIALITY** and
**ABC-RANK-ONE-REALIZATION-INVARIANCE**.

These elementary proofs do not use the general surjective representation
uniqueness theorem or any finite search. Align prescribed column labels
first. All ambient lattices are the declared free lattices.

## Square surjections

Let A be an r-by-r integer matrix whose columns generate Z^r.
Choose an integral preimage of each standard basis vector, forming T
with AT=I. Determinants give det(A)det(T)=1 in Z, hence det(A)=+/-1.
Conversely, the adjugate formula shows that det(A)=+/-1 gives an
integer inverse and therefore a surjection. Thus full-rank square
surjectivity, m(E)=1, and unimodularity are equivalent.

Reducing the integer inverse modulo any n >= 2 proves that A is
invertible over Z/n, including composite n. Its modular cycle kernel
is zero, so Bic_n(A)=0. Both reduction and inflation between these
zero modules are the unique zero maps. This also covers r=0 with the
empty determinant equal to one. No assertion about nonsurjective
square matrices is made: the original index-five counterexample is
square and has a nontrivial bicycle in its second realization.

## Rank-one labeled realizations

Let A=(a_e) and A'=(a'_e) be nonzero integer rows in the declared Z.
For a nonzero column, the singleton quotient Z/a_e Z has torsion
order |a_e|, so its arithmetic singleton multiplicity is |a_e|.
A zero column has rank zero and multiplicity one. Singleton ranks
therefore distinguish a zero entry from a unit entry; multiplicities
alone would not suffice.

Equal labeled arithmetic data imply a'_e=s_e a_e for signs
s_e in {+1,-1}; choose s_e=1 at zeros. Put D=diag(s_e). Then A'=AD,
D^2=I, and (A')^T=D A^T. Consequently b -> Db takes every cut of A
to a cut of A', and A'(Db)=A D^2 b=Ab takes cycles to cycles.
Its inverse is the same sign change. This proves a Z/n-module
isomorphism Bic_n(A) -> Bic_n(A') for every n >= 2. The same integral
D commutes with reduction and with multiplication by m/n for n|m,
so it identifies both directions of the entire tower.

Surjectivity is unnecessary for this rank-one conclusion. If required,
it is exactly gcd(a_e)=1, and is preserved by the signs. For a
surjective row, the separate general theorem additionally identifies
Bic_n(A) with the n-torsion of Z/(sum_e a_e^2)Z. That extra description
is not used in the direct proof above. In particular, rank-one
invariance does not imply rank-one bicycle triviality: (2,3) has
thirteen bicycles at modulus 13.

Rank-zero cuts are zero in every edge module. Together these direct
results exclude rank zero, rank one, and square surjections as sources
of a counterexample to the surjective candidate. The first remaining
search shape is rank two with at least three columns. The separate
[general proof](surjective-realization-invariance.md) now also settles
that shape and every higher rank; a finite census alone would not.

## Reproducible evidence

[Boundary tests](../conformance/test_phase6_boundaries.py) check literal
modular kernels of square matrices, all sign changes of bounded
rank-one rows (including loops and nonsurjections), and the nontrivial
(2,3) control. [The census](../experiments/surjective_rank_two.py)
uses complete arithmetic signatures, verified Smith forms, explicit
row/sign witnesses, and an independent edge/lattice oracle. Its
[receipt](../conformance/receipts/phase6-rank-two-v1.json) states exact
bounds and separates all-matrix checks from representative-only checks.
See the [audit](../docs/audits/phase6-boundaries-2026-10-15.md).
