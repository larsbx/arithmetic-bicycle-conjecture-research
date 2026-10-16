# Code-hull tower proof and interface audit — 2026-10-16

Baseline: `7b041ce1288256564f3ff104c238fc519f7a7476` (merged PR #7).
This is an assistant-authored proof review and executable cross-check,
not an independent human review or a proof-assistant certificate.

## Mathematical closure

Research task ABC-HULL-01 is closed by the separately registered
**ABC-CODE-HULL-TOWER**, with the [ring proof](../../proof/code-hull-tower.md)
as authority. Its hypotheses are any rectangular integer matrix and
n>=2; no essentiality, surjectivity, or field structure is used.

| Obligation | Proof check |
| --- | --- |
| Literal dual | Coordinate unit potentials force Ax=0; the converse is direct. |
| Hull quotient | Restrict A^T to ker(AA^T); the kernel is exactly ker(A^T), and every hull element has a Gram-kernel potential. |
| Reduction | Integer matrices commute with reduction; the denominator maps into the smaller denominator. |
| Scaled inflation | Multiplication by m/n kills the larger congruences, preserves the denominator, and is independent of integer lifts. |
| Quotient injectivity | (m/n)A^T y=0 mod m implies A^T y=0 mod n. |
| Naturality | The hull/quotient squares are the same integer matrix identities on representatives. |
| Composition and round trips | Ratios multiply across n|m|l; both round trips multiply by m/n, rather than being inverse maps. |
| Fixed-ring pairing preservation | Testing coordinate unit pairs gives exactly S^T S=I. |
| Integral coordinate classification | Integer columns of norm one have one +/-1 entry; orthogonality forces distinct positions. |
| Coordinate quotient transport | A'=UAS^T, y'=U^{-T}y and x'=Sx give G'=UGU^T and A'^T y'=S A^T y. |
| Tower witnesses | Reduction-compatible witness matrices and their inverses commute with scaled inflation; unrelated modular witnesses need not. |

The quotient denominator cannot be dropped: A=(2), n=4 has Gram
kernel order four, cut kernel order two, and quotient/hull order two.
Reduction need not be onto: the nonzero hull element for A=(1,1)
modulo two is not the reduction of a hull element modulo four.
No claim that a modular kernel commutes with tensor base change appears.

The pairing classification concerns the ambient standard bilinear form.
It is not a classification of all maps preserving a particular hull or
even all maps preserving orthogonality: unit similitudes illustrate the
difference. General invertible edge changes transport the pairing to
S^{-T}S^{-1}, changing the dual from ker A' to ker(A' S^{-T}S^{-1}).
This does not identify the transformed standard bicycle.

## Finite evidence and its limits

The [packet](../../conformance/replay_code_hull.py) checks 11 explicitly
listed matrices at 49 modulus cases, with 43 proper dividing-modulus
pairs and six three-level chains. Six matrices and 36 cases reuse the
unchanged PR #7 fixture; five further matrices cover redundant rows,
zero rows, zero columns, the empty matrix, and nonsurjective reduction.
There is no random sampling, silent cap, or general parameter census.

For every case, full cosets are compared with the fibers of A^T on the
Gram kernel. The isomorphism's two inverse identities, addition and scalar
action are checked. Every Gram-kernel representative participates in the
transition checks; integral shifts test lift independence. Both quotient
maps, their additivity, injection of inflation, both commuting squares,
round trips, identity maps, and three-level compositions are checked.
The receipt records actual quotient-to-hull and transition tables.

Independent literal codeword orthogonality and lattice-index edge
membership check all hulls, and the existing essential potential route
also checks every original seed. Four explicit coordinate scenarios
exercise signed integral maps, redundant rows, finite-ring isometries
not integral isometries, and modular row units that are not unimodular
over Z. Pairing equality is evaluated on all pairs of edge vectors at
those levels. Transport is compared against the literal target hull.
Inverse maps and both coordinate/tower squares are also checked.

Negative controls retain the standard-pairing shear discrepancy of
orders one and five, unscaled edge and potential inflation at 13 to 26,
the nontrivial quotient denominator, and nonsurjective reduction.
An additional test exhibits incompatible independently chosen isometries.
The old seed receipt continues to cover all eight CRT comparisons and
the original realization-dependent and prime-power module controls.

The new [receipt](../../conformance/receipts/code-hull-tower-v1.json)
pins its proof, fixture, implementation, tests, replay, and imported
algorithm files. It remains `non_authoritative_experiment` with empty
`claim_promotions`. All seven historical receipts and their pinned files
remain unchanged. Python acceptance authority remains false.

## Queue and boundaries

The research checker now permits a completed task only with a distinct
proved claim, matching proof locator, and a linked non-authoritative
receipt. The queue names ABC-RD-01 as next: classify nonsurjective
triangular-family tower variation with explicit bounds and equivalences.
No such classification is claimed by the present interface.

ABC-MAIN, ABC-REALIZATION-INVARIANCE, and ABC-UNIVERSAL-TORSION-MODEL
remain retracted. The surjective refinement retains its explicit domain.
No new imported literature theorem or novelty claim is needed for this
elementary ring proof; the existing hull terminology source is unchanged.

## Reproduced validation

On 2026-10-16, all 94 tests passed under
`python -m unittest discover -s conformance -p 'test_*.py' -q`.
Both registry/program checkers passed. All eight receipt replays passed:
the five graph/TU/representation/arithmetic/surjective conformance packets,
the expanded rank-two census, the original realization-dependence seeds,
and the new code-hull quotient packet. Patch whitespace also passed.
These checks validate the executable evidence and repository consistency;
they do not replace the general proof or independent mathematical review.
