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

Next blocking target: Phase 2. The graph theorem does not discharge the
fixed-TU or representation-independence obligations below.

## Phase 2 — fixed TU regular matroids

Generalize Phase 1 with \(A\) in place of graph incidence \(B\).

Promotion:
- `ABC-REGULAR-MODULAR-BICYCLE`: `working` -> `proved`.

## Phase 3 — regular representation independence

Pin down the exact theorem relating TU representations of the same regular matroid and prove the modular tower is representation-independent.

## Phase 4 — arithmetic-matroid equality and fixtures

Define fail-closed equality for representable arithmetic matroids using lattice-index multiplicities / module data.

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
