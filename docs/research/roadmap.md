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

Completed in the October 15 contribution: a separately stated
surjective essential arithmetic realization-invariance theorem.
Surjectivity is m(E)=1, an additional hypothesis beyond m(empty)=1.

- [x] Independently prove and register square-unimodular triviality and rank-one sign invariance.
- [x] Exhaust the 2-by-3 entry box [-2,2] and 2-by-4 box [-1,1], with explicit finite scope and controls.
- [x] Source audit of surjective representation uniqueness and a self-contained labeled proof.
- [x] Rational support-cycle argument and explicit upgrade to integral equivalence using surjectivity.
- [x] Smith-derived right inverse and arbitrary-modulus Gram isomorphism without a unit basis.
- [x] Both representative changes, both inverse directions, both modulus maps, and witness transport.
- [x] Independent all-minor, lattice-membership, quotient, and exhaustive signed-search evidence.
- [x] Non-TU and no-unit-basis fixtures, composite exponents, and rejection of the nonsurjective counterexample.

`ABC-SURJECTIVE-REALIZATION-INVARIANCE` is `proved` with its own
[proof record](../../proof/surjective-realization-invariance.md), source
audit, dated contribution audit, and fifth source-pinned receipt.
It concerns the tower's isomorphism class; witness-dependent comparison
maps are not unique.

The [direct boundary proof](../../proof/surjective-boundary-cases.md)
registers `ABC-SURJECTIVE-SQUARE-TRIVIALITY` and
`ABC-RANK-ONE-REALIZATION-INVARIANCE` separately. The latter does not
require surjectivity and includes zero columns via singleton rank data.
The [expanded census](../../experiments/surjective_rank_two.py) is
`ABC-PHASE6-RANK-TWO-CENSUS`, with status `computed`, not proof authority.
Its complete boxes contain 7,176 and 5,776 surjections in 94 and 71
arithmetic buckets, respectively. No counterexample was found.
The general theorem, rather than extrapolation from those boxes,
settles the surjective candidate in all ranks.

Next target: state and prove a structural description for nonsurjective
realizations that explicitly includes their additional lattice data.
No unrestricted realization-invariance claim is reinstated.

An intrinsic construction from ordinary arithmetic-matroid data cannot
recover the original bicycle tower on the full withdrawn domain.
The explicit pair even has isomorphic quotient groups at every subset.
Any alternative using finer realization data must name the added
structure and prove its transport properties.

Preserve the original statements and dated provenance; new restricted
claims receive separate identifiers and proof records.

### Research scaffold after the surjective theorem

The [connections brief](connections-and-open-questions.md) and
[machine-readable queue](program.toml) make the next work concrete.
Question IDs describe research work, not additional accepted proof claims.
Dependencies can reference proved baselines or retracted statements that
must remain negative controls; they do not assume a retracted statement.

- [x] Preserve the sourced connections document with current claim boundaries.
- [x] Register six tasks, dependencies, first actions, and acceptance/falsification criteria.
- [x] Add a source-pinned starting experiment for code hulls and nonsurjective variation.
- [x] ABC-HULL-01: prove the code-hull and Gram-kernel quotient identities, both modulus maps, and pairing-preserving coordinate transport.
- [ ] ABC-RD-01: classify tower variation in the triangular family, then source-classified representations.
- [ ] ABC-MODULE-01: state sufficient added lattice/map/pairing data and prove transport.
- [ ] ABC-TORIC-01: audit the current status of published reconstruction questions before extracting topology fixtures.
- [ ] ABC-JAC-01: audit restricted realization problems and specify exact pairing transport.
- [ ] ABC-CELL-01: derive a torsion-corrected modular statement from cellular cut/flow exact sequences.

The [code-hull proof](../../proof/code-hull-tower.md) closes ABC-HULL-01
as `ABC-CODE-HULL-TOWER`, with [quotient-sensitive evidence](../../conformance/receipts/code-hull-tower-v1.json)
and an explicit distinction between fixed-ring orthogonal maps and integral
signed permutations. Reduction need not be onto; scaled inflation is
injective and both maps commute with the quotient presentation.

A further [exact all-modulus three-edge presentation](../../proof/three-edge-full-tower-presentation.md) gives (s,u)-coordinate congruences, coherent maps, and a Smith-based order formula for each family member. An explicit modulus-nine control is noncyclic: (Z/3)^2. Its [versioned receipt](../../conformance/receipts/three-edge-structure-v1.json) records 256 bounded comparisons and is CI-replayed. This is not a classification of parameter choices with isomorphic complete towers; ABC-RD-01 remains active.

Phase 6 follow-up (October 22): a separate
[source-pinned v2 evidence packet](../../conformance/receipts/phase6-realization-dependence-v2.json)
records the triangular computations and a nonparallel 2-by-3
rank-two family, with independent edge-congruence checks and
counterexample values at moduli 7, 14 and 49.
The [three-edge proof note](../../proof/nonparallel-three-edge.md)
derives the exact modulus-b obstruction
`gcd(b, 2*(1+a+a²))`; it does **not** classify whole towers.
A [partial Lean 4 proof bank](../../lean/README.md) now records
algebraic normalizations and a set of explicit formalization gates.
Lean compilation is unverified until current-head CI passes;
no new proof registry status is promoted.

ABC-RD-01 remains the active next task. A [working triangular-family proof](../../proof/triangular-family-tower.md)
now gives a candidate exact subgroup formula and additive tower classification
at fixed b, with [bounded independent checks](../../experiments/triangular_family.py).
It has not received an independent proof audit or a source-pinned receipt;
no claim is promoted and the full task remains open. Next classify
source-classified nonsurjective representations beyond the triangular family.
Prioritize ABC-RD-01 and ABC-MODULE-01. The topology, graph-pairing, and cellular
tracks are follow-ups and do not block that work. All future theorem
promotions require their own proof records and exact evidence; the seed
packet alone is not a census or a classification theorem.

## Phase 7 — projective shadow

Formalize Grassmannian/determinantal interpretations only after the integral kernels are stable.
