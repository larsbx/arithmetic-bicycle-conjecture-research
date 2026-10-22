import Mathlib

/-! Partial, unverified proof bank. Not a formalization of the full theorem. -/
namespace ABC
variable {R : Type*} [CommRing R]

theorem gram_three_cauchy_binet (a b c d e f : R) :
    (a*a+b*b+c*c)*(d*d+e*e+f*f) - (a*d+b*e+c*f)^2 =
      (a*e-b*d)^2 + (a*f-c*d)^2 + (b*f-c*e)^2 := by
  ring

/-- Two coordinates of an integral right inverse yield injectivity
of the transpose over any commutative ring, hence also over ZMod n. -/
theorem split_transpose_injective (a b c d e f t u v w x z : R)
    (h1 : t*a+u*b+v*c=1) (h2 : t*d+u*e+v*f=0)
    (h3 : w*a+x*b+z*c=0) (h4 : w*d+x*e+z*f=1)
    (s q : R) (ha : a*s+d*q=0) (hb : b*s+e*q=0)
    (hc : c*s+f*q=0) : s=0 ∧ q=0 := by
  constructor
  · linear_combination t*ha + u*hb + v*hc - s*h1 - q*h2
  · linear_combination w*ha + x*hb + z*hc - s*h3 - q*h4

theorem gram_cycle_normalization (a b c d e f s t : R) :
    a*(a*s+d*t)+b*(b*s+e*t)+c*(c*s+f*t) =
      (a*a+b*b+c*c)*s+(a*d+b*e+c*f)*t := by
  ring
end ABC
