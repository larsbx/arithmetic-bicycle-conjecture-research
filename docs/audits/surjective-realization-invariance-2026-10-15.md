# Surjective arithmetic realization-invariance audit — 2026-10-15

Claim: **ABC-SURJECTIVE-REALIZATION-INVARIANCE**.
Base main: dd81fc192302ea313acf6e9512243ca076482373,
the merge of the principal counterexample contribution.

This is the contribution author's proof audit, not separate-person
acceptance review. Independent evidence means separate exact algorithms;
Python retains no acceptance authority.

## Hypotheses and source gate

The theorem requires essential integer realizations in their declared
free ambient lattices, with m(empty)=m(E)=1. In this domain m(E)=1
means the columns generate the ambient lattice. This is stronger than
the original conjecture's torsion-free hypothesis.

The [source audit](../../sources/surjective-representation-equivalence.md)
identifies Pagaria–Paolini, Section 5.1 and the paragraph following
Lemma 5.2, for established representation uniqueness in this domain.
Its equivalence is labeled and permits column signs. The local proof
does not claim a newly discovered uniqueness theorem or a unique
comparison map.

The local statement includes the prescribed label permutation and
handles rank zero and loops. It excludes nonsurjective realizations
instead of replacing their ambient lattice by their column lattice.

## Integral proof gate

| Obligation | Audited argument |
| --- | --- |
| Integral right inverse | Smith transforms P A V = [I,0] give T = V[:, :r] P, with A T = I. No unit maximal minor is assumed. |
| Composite-ring potential uniqueness | T transpose A transpose = I makes A transpose injective modulo every integer n. |
| Forward divisor | The cycle equation makes Qy/n integral; multiplying its class by n gives zero. |
| Lift and potential independence | Two representing potentials differ by nz, so divisors differ by Qz. Arbitrary edge lifts do not replace potentials. |
| Divisor independence | If Qy = nd, changing d by Qz changes y by nz. |
| Both inverse identities | Substitution in Qy = nd gives both identities; nonsingularity follows from Q = A A transpose and full row rank. |
| Modulus reduction | Reduction m to n corresponds to multiplication by m/n on Gram torsion. |
| Modulus inflation | Multiplying edges by m/n corresponds to torsion inclusion; both directions compose. |
| Rational representation comparison | A common rational basis gives equal entry magnitudes and equal absolute minors by identity-column completion. |
| Cycle sign condition | A chordless cycle has exactly two matching terms with positive magnitudes a,b. The distinct values a+b and absolute(a-b) force consistent relative signs. Chords reduce longer cycles. |
| Integral representation comparison | Surjectivity gives U Z^r = Z^r, or explicitly U = A' S inverse T. Rational equivalence alone is insufficient. |
| Whole-tower transport | A'=UAS and Q'=UQU transpose give edge action S transpose, potential action U inverse transpose, divisor action U, and both commuting Gram squares for every modulus. |
| Isomorphism-class scope | Witnesses invert and compose; valid self-witnesses can act differently. Only the tower's isomorphism class is intrinsic. |

The rational support argument is valid before imposing surjectivity;
the integral upgrade is exactly where m(E)=1 is used. This distinction
is visible in the principal counterexample's nonintegral row change.

## Independent exact evidence gate

The candidate checks the full rectangular Smith certificate before
admitting a surjection. Its right inverse is verified by the entire
integer matrix identity. The equivalence finder checks complete
arithmetic data, normalizes the first rational basis, solves a
support-graph sign system, then verifies integral unimodularity and
the complete witness equation.

The independent oracle imports no kernel code. It checks
surjectivity and subset arithmetic data via gcds of Bareiss minors,
uses a different rational basis and Cramer's rule, and searches
every column-sign assignment. It does not reuse Smith transformations
or the candidate sign solver.

For modular bicycles, the independent arithmetic oracle enumerates
edge vectors, filters by cycle congruences, and tests cut membership
by equality of integer lattice indices for [A transpose, n I]
and its augmentation by the edge vector. This remains exact for
every composite modulus. Literal cut enumeration supplies a third
finite check. Independently enumerated Gram quotient classes and
all-minor Smith factors verify torsion counts and element orders.

The new source-pinned packet has:

- ten positive pairs, 38 modulus cases, and 33 proper modulus pairs;
- three source matrices without a unit maximal minor, including
  (2,3), the rank-two matrix with minors 6,2,-3, and a disconnected
  extension with a coloop and loop;
- prime, prime-power, mixed-composite, noncyclic, zero-rank, loop,
  support-six-cycle, and nonorthogonal coordinate fixtures;
- two arithmetic negative pairs and three nonsurjective rejection
  fixtures, including both members of the principal counterexample.

The complete ternary 2-by-3 census examines all 729 matrices.
It admits 552 integral surjections, including 96 non-TU matrices,
in ten complete arithmetic buckets. Candidate and independent sign
search verify every comparison with a bucket representative and
2,208 modulus cases. All 90 ordered cross-bucket comparisons are
rejected.

Fifteen added tests verify the full packet, both inverse directions,
all representative changes, linearity, potential and Gram transport,
all six strict fixture modulus chains, witness composition and
inversion, large composite moduli without potential enumeration,
and nonunique comparisons. The new maps agree with all seven
inherited TU fixtures.

At modulus 49, the rank-two no-unit-basis fixture has elements of
order 49; its mod-7 module cannot expose that exponent. For (2,3),
reduction from 169 to 13 is zero although the target has thirteen
bicycles. Unscaled inflation and direct division of arbitrary edge
lifts fail. Negative witness tests check the complete matrix
equation, unit determinant, dimensions, labels, and integer domains,
including bool/float aliases after populating caches.

The six-cycle negative pair has the same entry magnitudes but
determinant magnitudes 25 and 23 on its nonbasis columns. Thus
support magnitude data alone cannot replace full arithmetic data.
The nonsurjective principal pair still has equal arithmetic data
and different bicycle orders; both are rejected by the new domain
gate.

## Validation and authority

All 80 tests pass on Python 3.12.14. The four inherited source-pinned
receipts replay without changes. The fifth receipt rebuilds the
surjective evidence and is checked byte for byte. Its source list
includes the new proof, source audit, fixtures, tests, replay, code,
and inherited exact dependencies.

Registry and required authority locators, preserved earlier claim
records and pinned source bundles, local documentation links, and
patch whitespace are checked before publication. The new scoped claim
is recorded as proved only after the integral proof and independent
evidence requirements pass.

ABC-MAIN, ABC-REALIZATION-INVARIANCE, and
ABC-UNIVERSAL-TORSION-MODEL remain retracted with their original
statements. The graph, fixed-TU, regular TU, exact signature, and
counterexample records retain their claims and bytes.
Historical status notes in earlier pinned bundles remain historical.

Remote CI and any subsequent separate-person review are independent
publication checks, not inferred from this author's audit.
