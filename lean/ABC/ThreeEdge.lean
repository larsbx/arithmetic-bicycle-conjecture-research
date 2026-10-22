import Mathlib

/-!
Nonparallel three-column Phase 6 proof-bank lemmas.
The finite-field scalar identities are only the local b=7 obstruction.
The all-modulus tower and all-subset Smith assertions remain
separately listed proof obligations, not mechanically established here.
-/

namespace ABC

theorem threeEdge_norm {R : Type*} [CommRing R] (a : R) :
    1 + a * a + (a + 1) * (a + 1) =
      2 * (1 + a + a * a) := by
  ring

/-- The third edge coordinate is the sum of the first two cut coordinates. -/
theorem threeEdge_cut_coordinate {R : Type*} [CommRing R]
    (a b s t : R) :
    (a + 1) * s + b * t = (a * s + b * t) + s := by
  ring

/-- The first cycle equation in the (s,u) presentation. -/
theorem threeEdge_cycle_coordinate {R : Type*} [CommRing R]
    (a s u : R) :
    s + a * u + (a + 1) * (s + u) =
      (a + 2) * s + (2 * a + 1) * u := by
  ring

/-- The Gram determinant is independent of the primitive parameter a. -/
theorem threeEdge_gram_det {R : Type*} [CommRing R]
    (a b : R) :
    (2 * (a * a + a + 1)) * (2 * b * b) -
      (b * (2 * a + 1)) * (b * (2 * a + 1)) = 3 * b * b := by
  ring

theorem seven_a1_norm : (1 : ZMod 7) + 1 * 1 + (1 + 1) * (1 + 1) = 6 := by
  decide

theorem seven_a2_norm : (1 : ZMod 7) + 2 * 2 + (2 + 1) * (2 + 1) = 0 := by
  decide

theorem seven_a1_nonisotropic :
    (1 : ZMod 7) + 1 * 1 + (1 + 1) * (1 + 1) ≠ 0 := by
  decide

end ABC
