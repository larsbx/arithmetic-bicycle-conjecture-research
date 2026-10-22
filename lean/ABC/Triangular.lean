import Mathlib

/-!
Phase 6 proof bank, triangle subfamily.
These are ring-level normalization lemmas, not a formal proof of the
global gcd-order or coherent tower classification. No `sorry`, `admit`
or new axioms are used here. The repository's claims.toml is unchanged.
-/

namespace ABC
section RingLemmas

variable {R : Type*} [CommRing R]

/-- Cut membership for the two-column triangular family. -/
def TriCut (a b x z : R) : Prop :=
  ∃ s t : R, x = s ∧ z = a * s + b * t

/-- Cycle membership for the two-column triangular family. -/
def TriCycle (a b x z : R) : Prop :=
  x + a * z = 0 ∧ b * z = 0

theorem triCut_iff (a b x z : R) :
    TriCut a b x z ↔ ∃ t : R, z = a * x + b * t := by
  constructor
  · rintro ⟨s, t, rfl, hz⟩
    exact ⟨t, hz⟩
  · rintro ⟨t, hz⟩
    exact ⟨x, t, rfl, hz⟩

theorem triCycle_normal (a b z : R) :
    TriCycle a b (-a * z) z ↔ b * z = 0 := by
  simp [TriCycle]
  ring

/-- Elementary cut congruence before the gcd criterion over ZMod. -/
theorem triCut_normal_form (a b z t : R) :
    (z = a * (-a * z) + b * t) ↔ (b * t = (1 + a * a) * z) := by
  constructor
  · intro h
    linear_combination -h
  · intro h
    linear_combination -h

theorem triBicycle_normal_form (a b z : R) :
    (TriCut a b (-a * z) z ∧ TriCycle a b (-a * z) z) ↔
      ((∃ t : R, b * t = (1 + a * a) * z) ∧ b * z = 0) := by
  constructor
  · rintro ⟨hc, hy⟩
    obtain ⟨t, ht⟩ := (triCut_iff a b (-a * z) z).mp hc
    exact ⟨⟨t, (triCut_normal_form a b z t).mp ht⟩,
      (triCycle_normal a b z).mp hy⟩
  · rintro ⟨⟨t, ht⟩, hb⟩
    exact ⟨(triCut_iff a b (-a * z) z).mpr
        ⟨t, (triCut_normal_form a b z t).mpr ht⟩,
      (triCycle_normal a b z).mpr hb⟩

end RingLemmas
end ABC
