# Surjective representation uniqueness: source and scope audit

Source checked on 2026-10-15:

Roberto Pagaria and Giovanni Paolini, *Representations of torsion-free
arithmetic matroids*, [arXiv:1908.04137](https://arxiv.org/pdf/1908.04137),
version 1 dated 2019-08-12.

Section 2, Definitions 2.4–2.5, specifies representations in a finitely
generated abelian ambient group, multiplicity as quotient torsion
order, essentiality as equality of ambient and total ranks, and
equivalence by an ambient isomorphism preserving each labeled cyclic
subgroup. For a free ambient group, that equivalence permits individual
column signs. Torsion-free means m(empty)=1; surjective means m(E)=1.

Section 5.1 (printed pages 9–10) constructs the representation of a
torsion-free surjective arithmetic matroid up to equivalence.
The paragraph immediately after Lemma 5.2 identifies the candidate,
when representable, as the sole equivalence class. Its sign procedure
uses a bipartite support graph, spanning forest, and absolute
determinants of two-matching cycle submatrices. Lemma 5.2 uses Smith
form to recover coordinates in the generated lattice.

The local proof supplies its own labeled argument in the declared
ambient lattice. It allows any rational basis, uses equal normalized
minor magnitudes to prove the cycle sign condition, and uses
surjectivity explicitly to make the rational row equivalence integral.
It does not require a unit maximal minor or total unimodularity.
This is a local proof of an established uniqueness result, not a claim
that representation uniqueness was newly discovered here.

The source's uniqueness statement concerns representations up to
equivalence. It does not choose a unique comparison isomorphism.
The local modular tower and Gram-cokernel transport arguments are
proved in [the repository record](../proof/surjective-realization-invariance.md),
including every composite modulus and both modulus maps.

Section 5.2 treats the general nonsurjective case separately.
Neither its classification nor the surjective result repairs the
original conjecture on all torsion-free realizations. The repository
counterexample has m(E)=5 and stays outside this new theorem.
Changing the ambient lattice to the column lattice changes the
arithmetic data; that operation is not silently used as an equality.
