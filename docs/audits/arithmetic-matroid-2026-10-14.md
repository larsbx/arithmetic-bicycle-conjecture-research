# Arithmetic equality and realization counterexample audit — 2026-10-14

Claims: ABC-ARITHMETIC-SIGNATURE and
ABC-ARITHMETIC-REALIZATION-COUNTEREXAMPLE.
Refuted statements: ABC-MAIN and ABC-REALIZATION-INVARIANCE.
Base main: 6f5a0c5447a02b1b862fa673b25f9549356259b6.

This is the contribution author's proof audit, not separate-person
acceptance review. The computation uses independent algorithms and a
third finite cross-check; the refutation itself is an elementary proof.

## Arithmetic definition gate

The source definition distinguishes torsion-free m(empty)=1 from
surjective m(E)=1. Essential means ambient rank equals total matroid
rank. Both counterexample matrices are full-rank integer lists in the
same free ambient lattice Z^2, with determinant 5.

All four labeled subsets are checked. The empty multiplicity is one;
both columns of either matrix are primitive; the full subgroup index
is five. Ranks are 0,1,1,2 and multiplicities are 1,1,1,5. The common
arithmetic matroid is within the original conjecture's declared domain.
Requiring surjectivity would be a different statement.

The Smith proof checks the ambient lattice and saturation explicitly.
For every subset, nonzero Smith factors give its rank and their product
gives the torsion/index multiplicity. Empty and dependent subsets are
included. Full-set data, a selected basis, or Gram Smith factors are
insufficient as arithmetic equality tests.

The executable interface requires essential realizations. It rejects
redundant ambient rows, nonintegers, invalid widths and subset masks,
and invalid label permutations. It does not silently change the
ambient lattice or treat an arbitrary serialized table as representable.

## Refutation gate

| Obligation | Audited argument |
| --- | --- |
| Same arithmetic object | The complete four-subset table agrees; full and singleton quotient isomorphism classes also agree. |
| Torsion-free and essential | Ambient Z^2 is free, empty torsion is trivial, and both total ranks are two. |
| Literal cut images | At modulus 5, the cut lines are (s,s) and (s,2s). |
| Literal cycle conditions | Their matrix images are (2s,0) and (5s,0) modulo 5. |
| Nonisomorphic modules | The first is zero; the second is cyclic of order five. |
| Composite witness | The direct modulus-10 equations force s=t even in the second case and s=0 in the first; modules again have orders five and one. |
| Tower failure | A tower isomorphism must be an isomorphism at each modulus; one order discrepancy already prevents it. |
| Orientation and basis changes | Integral unimodular rows and signed column permutations always preserve cuts/cycles up to coordinate isomorphism, so they cannot fix differing orders. |
| Minimal rank/elements | Essential rank-one data determine entry magnitudes and thus signs; rank zero is trivial. One element cannot have essential rank two. No minimal-index assertion is made. |

The proof does not use coker(AA transpose)[n] as a bicycle oracle:
neither counterexample matrix has an integral right inverse. Both Gram
determinants are 25, but the Gram Smith factors differ. Agreement in
bicycle order at modulus 25 does not undo the discrepancies at 5 and 10.

This is the principal realization-invariance refutation, not merely
the earlier universal torsion-model obstruction A=[2].

## Independent exact evidence

The candidate Euclidean Smith construction tracks both integer
unimodular transformations. Each certificate is checked for dimensions,
unit determinants, the full matrix equation, a dividing nonnegative
diagonal, and trailing zeros. The oracle imports no kernel code and
computes determinantal divisors with Bareiss minors instead.

Fourteen explicit realizations supply 91 complete subset records,
six labeled comparisons, and 20 bicycle cases. The receipt pins the
exact arithmetic encoding, subset factor lists and certificate hashes,
and complete modular edge sets. Multiplicities in canonical arithmetic
encodings use positive decimal strings, including indices beyond 2^80.

Thirteen new tests pass, including all 15,625 integer 2-by-3 matrices
with entries in {-2,-1,0,1,2}, rectangular/singular/empty certificates,
and large planted unimodular transforms. TU specialization checks the
original seven TU fixtures: all 648 subset multiplicities are one.
Tests also cover ambient row changes, signed relabeling, forged Smith
certificates, invalid domains and populated-cache bool/float aliases.

Candidate bicycle enumeration uses all potentials and deduplicates cuts.
The independent oracle enumerates edges and checks cut membership using
indices of [A transpose | n I] and its augmentation by the edge vector.
This tests lattice membership over composite rings without reusing the
candidate potential enumerator. The inherited literal-cut routine
provides a third route.

Direct expected generators (1,2) at modulus 5 and (2,4) at modulus 10
check both cardinality and cyclic order. Eight signed column/permutation
possibilities independently require a nonintegral row equivalence for
the counterexample pair.

Negative comparisons detect different lower-subset multiplicities even
when rank profiles, singleton data and the ground-set index agree.
Another control has identical full-set Smith factors but different
singleton indices. Saturation changes the ambient arithmetic data and
is explicitly rejected as an equality shortcut.

## Authority and status

ABC-MAIN and ABC-REALIZATION-INVARIANCE are retained as retracted claims
with this counterexample proof. The signature theorem and explicit
counterexample receive separate proved records. The earlier universal
torsion-model strengthening remains retracted.

The graph, fixed-TU, and regular TU representation-independence proofs
and claims are unchanged. Their original source-pinned receipts and
inputs remain unchanged. Dated earlier status notes describe the
state before the principal conjecture was refuted; current claim status
is governed by the registry.

The regular-representation v1 receipt's open-status annotation likewise
records its October 11 source bundle. Its replay verifies that historical
bundle without replacing the current registry's retracted status.

Python acceptance authority remains false. Mathematical proof and source
audits provide claim authority; finite checks support the implementations.
All 65 tests pass on Python 3.12.14. All four source-pinned replays,
registry/counterexample locators for ten claims, preserved-record
comparisons, and patch whitespace pass. Remote CI and review are separate
publication checks.
