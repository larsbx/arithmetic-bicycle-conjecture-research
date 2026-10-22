# ABC Phase 6 Lean proof bank

This is a separate **mechanization workbench**, not theorem acceptance
authority for the repository's proof registry. Lean 4.35.0 and mathlib4
tag v4.35.0 are pinned; a dedicated CI workflow builds this Lake
library. The initial files have not been locally compiled in the
authoring environment, which lacks Lean. Treat them as **unverified
until the current-head CI build reports success**.

Build from the `lean/` directory:

    lake update
    lake exe cache get
    lake build

`ABC/Triangular.lean` gives algebraic cut/cycle normalization
over arbitrary commutative rings, without requiring field division.
`ABC/ThreeEdge.lean` records the nonparallel family's Gram scalar
polynomial and the b=7 finite-field arithmetic controls.

## Proof obligations not discharged by these modules

* **TRI-01:** encode `ZMod n` congruence solvability
  `b*t = c*z` iff `gcd(b,n)` divides a representative of `c*z`;
  supply exact explicit `k` normal forms, respecting `n>=2`.
* **TRI-02:** prove cyclic subgroup cardinality
  `gcd(g,(1+a²)*(n/g))` and fixed-b classification with controlled
  arithmetic parameters, not merely equal orders for sampled n.
* **TRI-03:** derive commuting reduction and scaled-inflation squares
  from the canonical witnesses; avoid treating reduction as surjective.
* **THREE-01:** formalize complete labeled subset signatures of
  `[[1,a,a+1],[0,b,b]]` for primitive `a,a+1`, including ambient
  index `b` and all pair minors.
* **THREE-02:** prove the modulus-b bicycle group has order
  `gcd(b,2*(1+a+a²))`, and formalize the a=1/2,b=7 comparison
  of *groups*, not just Gram scalar equalities.
* **RD-EXT:** classify nonsurjective towers beyond this three-edge
  example, prove maps and source-classified normal form completeness.
* **MODULE-01:** specify sufficient embedded-lattice/coordinate-pairing
  data and prove coherent transport over all moduli.

The absence of `sorry` in a *partial* bank must never be confused
with a formal proof of the outstanding obligations. There are no
new entries in `proof/claims.toml`, no changed statuses, and no
claim that Lean verified any general nonsurjective theorem.

The original claims `ABC-MAIN`, `ABC-REALIZATION-INVARIANCE`,
`ABC-UNIVERSAL-TORSION-MODEL` remain retracted.

`ABC/SurjectiveThreeEdge.lean` adds ring-level Gram determinant,
split-transpose injectivity and cycle normalization identities. These
new lemmas are uncompiled locally. The restricted cyclic theorem's
finite-field dimension, Smith and tower arguments are written in
`proof/surjective-three-edge-cyclic.md`, not fully formalized in Lean.
