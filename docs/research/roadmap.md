# Roadmap

## Phase 0 — governed bootstrap

- [x] Declare ABC precisely.
- [x] Add authority planes and conservative claim registry.
- [x] Preserve thread state as non-authoritative audit provenance.
- [x] Add CI after the first executable conformance fixture exists.

## Phase 1 — graph modular bicycle theorem

Goal:
\[
K(G)[n]\cong \operatorname{Bic}_n(G)
\]
for every connected graph and \(n\ge2\).

Completed in the 2026-10-08 graph contribution:

- [x] Exact statement with graph naturality, reduction, and inflation maps.
- [x] Integral proof record, including representative independence and both inverse identities.
- [x] Examples for prime, prime-power, and composite moduli.
- [x] Independent exact SNF and critical-group oracle checks.
- [x] Negative tests for incorrect representative/lift constructions.

Promotion:

- `ABC-GRAPH-MODULAR-BICYCLE`: `working` -> `proved`, supported by
  `proof/graph-modular-bicycle.md`, the dated proof audit, and source-pinned
  conformance receipts.

The graph theorem and its independent audit remain separate from the
fixed-TU and representation-independence obligations below.

## Phase 2 — fixed TU regular matroids

Completed in this contribution: replace graph connectedness with an
integral right inverse of a full-row-rank TU matrix A. The proof covers
every integer modulus, both representatives and inverse identities,
specified coordinate equivariance, and compatible modulus maps.
Independent evidence includes graphic and cographic fixtures, all-minor
Smith factors, separate cycle completion and quotient enumeration, and
non-TU controls that distinguish loss of splitting from loss of TU.

Promotion:
- `ABC-REGULAR-MODULAR-BICYCLE`: `working` -> `proved`, supported by
  `proof/regular-modular-bicycle.md`, its dated proof audit, and the TU
  source-pinned receipt.

Specified coordinate equivariance in Phase 2 remains distinct from the
theorem relating arbitrary TU realizations of one matroid in Phase 3.

## Phase 3 — regular representation independence

Completed in the October 11 contribution:

- [x] Audit the full-row-rank TU hypotheses and label conventions of the equivalence source.
- [x] Derive the prescribed labeled equivalence from unit-basis normal forms and integral support-cycle signs.
- [x] Apply one integral witness to every modulus and both tower maps.
- [x] Check Gram-cokernel transport, both inverse squares, witness composition, and nonunique comparison maps.
- [x] Verify explicit witnesses against a separate signed-search oracle and all-subset rational rank data.

`ABC-REGULAR-REPRESENTATION-INVARIANCE` is recorded as `proved` with its
own integral proof, dated audit, and source-pinned witness evidence.
The source audit identifies Backman–Baker–Yuen, Section 2.1, Lemma 2.1.1;
the local proof gives the labeled statement explicitly. Independence is
of the tower's isomorphism class under TU representations; a unique
comparison map from an unoriented matroid is not asserted.

The ordinary-matroid comparison above is separate from the exact
arithmetic equality gate and counterexample in Phases 4–5.

## Phase 4 — arithmetic-matroid equality and fixtures

Completed in the October 14 contribution for essential integer
realizations in their declared free ambient lattice:

- [x] Verified rectangular Smith certificates with both unimodular transforms.
- [x] Rank and saturation-index multiplicity for every labeled subset.
- [x] Exact comparison under a prescribed label bijection and versioned complete encodings.
- [x] Independent all-minors rank/index oracle and modular cut-membership criterion.
- [x] Empty, dependent, nonprimitive, nonsurjective, large-integer, and invalid-domain controls.

`ABC-ARITHMETIC-SIGNATURE` is `proved`. The executable interface does
not silently alter the ambient lattice or conflate arithmetic equality
with equivalence of realizations.

## Phase 5 — explicit realization counterexample

Completed by a concrete witness, without asserting an exhaustive
realization search:

`A=((1,1),(0,5))` and `A'=((1,2),(0,5))` have the same complete
arithmetic data, with ranks 0,1,1,2 and multiplicities 1,1,1,5.
Their bicycle orders are one and five at both moduli 5 and 10.
The [elementary proof](../../proof/arithmetic-realization-counterexample.md)
and independent exact receipt establish the discrepancy.

`ABC-ARITHMETIC-REALIZATION-COUNTEREXAMPLE` is `proved`.
`ABC-MAIN` and `ABC-REALIZATION-INVARIANCE` are `retracted` on their
original torsion-free domain. They are not silently replaced by a
surjective-domain statement. The earlier universal torsion-group
strengthening remains a separate retraction.

The graph, fixed-TU, and regular TU theorems remain proved. Agreement
of the counterexample's bicycle orders at modulus 25 does not undo
the order discrepancies at 5 and 10.

## Phase 6 — corrected statement and structural data

Next blocking target: source and proof audit of a separately stated
surjective essential arithmetic realization-invariance refinement.
Surjectivity is m(E)=1, an additional hypothesis beyond m(empty)=1.

An intrinsic construction from ordinary arithmetic-matroid data cannot
recover the original bicycle tower on the full withdrawn domain.
The explicit pair even has isomorphic quotient groups at every subset.
Any alternative using finer realization data must name the added
structure and prove its transport properties.

Preserve the original statements and dated provenance; new restricted
claims receive separate identifiers and proof records.

## Phase 7 — projective shadow

Formalize Grassmannian/determinantal interpretations only after the integral kernels are stable.
