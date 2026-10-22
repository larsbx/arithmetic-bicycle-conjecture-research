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

theorem seven_a1_norm : (1 : ZMod 7) + 1 * 1 + (1 + 1) * (1 + 1) = 6 := by
  decide

theorem seven_a2_norm : (1 : ZMod 7) + 2 * 2 + (2 + 1) * (2 + 1) = 0 := by
  decide

theorem seven_a1_nonisotropic :
    (1 : ZMod 7) + 1 * 1 + (1 + 1) * (1 + 1) ≠ 0 := by
  decide

end ABC
