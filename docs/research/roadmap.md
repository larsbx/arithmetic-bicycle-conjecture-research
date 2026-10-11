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

Next blocking target: Phase 4. The ordinary-matroid comparison above
does not implement arithmetic-matroid equality or prove ABC.

## Phase 4 — arithmetic-matroid equality and fixtures

Define fail-closed equality for representable arithmetic matroids using lattice-index multiplicities / module data.

Retain realization invariance as the principal conjecture. The bootstrap's
unconditional finite-group strengthening is false: A=[2] is torsion-free
but has Bic_2=0 and Bic_4=Z/2. Its separate counterexample record retracts
that strengthening. Any torsion-group extension needs additional
hypotheses or a different representing object; Phase 4 must not assume
it is equivalent to realization invariance.

## Phase 5 — bounded counterexample search

Enumerate small non-TU integer matrices, bucket by arithmetic matroid, and compare bicycle modules for:
- primes,
- prime powers,
- mixed composite moduli.

A mismatch is a valid ABC counterexample/refinement signal.

## Phase 6 — structural attack

If bounded searches survive, seek an intrinsic construction of the bicycle tower from arithmetic-matroid data.

## Phase 7 — projective shadow

Formalize Grassmannian/determinantal interpretations only after the integral kernels are stable.
