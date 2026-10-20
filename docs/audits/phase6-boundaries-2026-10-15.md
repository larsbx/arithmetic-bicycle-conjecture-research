# Phase 6 boundary and expanded census audit — 2026-10-15

Audited baseline: PR #6 at `40d23ee5e7edfa9252f0a44a31a2d6f37f5a6c01`,
following merged PR #5 at `dd81fc192302ea313acf6e9512243ca076482373`.
This follow-up reuses the existing surjective theorem, candidate code,
and independent algorithms. It is another assistant proof audit, not
independent human acceptance review.

## Claims and proof obligations

The separate candidate identifier already exists as
`ABC-SURJECTIVE-REALIZATION-INVARIANCE` in PR #6. Its proof settles the
surjective question generally; creating another overlapping conjecture
would duplicate that work. Its explicit hypotheses remain essentiality,
free declared ambient lattice, complete labeled arithmetic equality,
and m(E)=1. The original two unrestricted claims remain retracted.

The rational normalization argument was checked directly. Replacing
basis columns recovers all normalized minor magnitudes. A chordless
support cycle has two nonzero determinant terms of magnitudes a,b>0;
a+b differs from |a-b|. Thus sign-ratio products are one around every
cycle. Vertex signs give rational row/sign equivalence. Both column
lattices being the whole declared lattice forces the rational row map
and its inverse to be integral. No unit maximal minor is assumed.
A single signed coordinate map then transports cuts, cycles, and both
modulus maps. This proves invariance of the tower isomorphism class,
not uniqueness of a comparison map.

The fixed-surjection Gram proof was also checked: an integral right
inverse makes potentials unique modulo n, the cycle equation makes
Qy/n integral, and Qy=nd supplies the inverse on torsion divisor classes.
The proof now uses the finite integer Cauchy–Binet sum of squared
maximal minors to show det(Q)>0, including the empty-rank convention.
No real-vector or limiting argument is necessary.

The existing primary source was checked directly: Pagaria–Paolini,
[arXiv:1908.04137v1](https://arxiv.org/pdf/1908.04137v1), Definitions
2.4–2.5 and Section 5.1, especially the paragraph following Lemma 5.2.
It agrees with the existing source audit: representation uniqueness
up to labeled column signs in this domain is established literature.
No novelty claim is added.

The new [boundary record](../../proof/surjective-boundary-cases.md)
has two direct proofs, neither depending on representation uniqueness:

- `ABC-SURJECTIVE-SQUARE-TRIVIALITY`: an integral right inverse gives
  determinant +/-1. The integer inverse survives every modular
  reduction, so the entire cycle kernel, and hence bicycle, is zero.
- `ABC-RANK-ONE-REALIZATION-INVARIANCE`: singleton rank identifies loops;
  singleton multiplicity identifies the absolute value of every nonzero
  column. Column signs give a self-inverse cut/cycle transport commuting
  with both tower maps. Surjectivity is not needed.

These rule out the elementary shapes independently. They do not assert
that rank-one bicycles are trivial, nor that every surjection contains
a unit basis. Positive controls (2,3) and the rank-two matrix with
maximal minors 6,2,-3 explicitly refute those shortcuts.

## Finite search scope

`ABC-PHASE6-RANK-TWO-CENSUS` is recorded as **computed**.
The [script](../../experiments/surjective_rank_two.py) visits every
labeled matrix in two boxes, with no sign/permutation quotienting,
random sampling, early termination, or silent cap:

| Shape | Entries | All matrices | Surjections | Arithmetic buckets |
| --- | --- | ---: | ---: | ---: |
| 2 by 3 | -2 through 2 | 15,625 | 7,176 | 94 |
| 2 by 4 | -1 through 1 | 6,561 | 5,776 | 71 |

Every matrix, including excluded matrices, has its domain Smith factors
checked against independent gcds of Bareiss minors. Every admitted
matrix has all subset ranks/multiplicities checked by both routes.
Within each bucket, every matrix is compared to its lexicographically
first representative. Candidate support signs and independent exhaustive
sign search both find an integral unimodular witness. These witness
comparisons include the representative's identity case; the receipt
separately counts nonidentity comparisons.

Every admitted matrix also has its full Gram Smith factors checked by
both routes. Thus the finite abelian invariant factors, not merely
orders or determinants, agree within every bucket. All-matrix direct
potential enumeration and explicit witness transport are checked at
2,3,4,6 (51,808 cases). For one representative per bucket, the independent
edge/lattice oracle, literal cuts, and candidate potential sets agree
at 2,3,4,5,6,8,9,10 (1,320 cases). These include primes, prime powers,
and mixed composites. Annihilator counts for every divisor of each
modulus additionally check exponent information against the Smith
factors. The receipt does not describe representative-only oracle
calls as all-matrix calls.

All-matrix Gram profiles are compared at those eight moduli through
full Smith factors. The proof justifies their interpretation as bicycle
invariants in this domain; the representative oracle does not assume
that interpretation. Explicit integral witnesses establish comparisons
to the representative, so enumerating every ordered pair in a bucket
is unnecessary.

Controls preserve the original nonsurjective equal-data discrepancy
(orders one and five at 5 and 10), reject that pair from the new domain,
reject surjective pairs with matching singleton/full-index data but
unequal lower-subset multiplicities, and check the no-unit-basis C49
fixture at 7,14,49. Boundary tests independently exhaust 40 ternary
unimodular square matrices and 992 bounded rank-one sign comparisons.

The 2-by-3 box includes 1,440 surjections without a unit maximal
minor; the 2-by-4 ternary box has none. Thus the expanded search
exercises the Smith-derived splitting beyond a unit-basis shortcut.

No discrepancy occurs in either finite box. This is finite evidence,
not a universal proof by search. The separate integral theorem settles
the proposed restriction for all ranks and all moduli.

## Replay and governance

The receipt pins its script, boundary proof/tests, the general proof,
and all exact kernel/oracle dependencies. The prior surjective receipt
is intentionally regenerated only because the nonsingularity proof
was changed to the integer Cauchy–Binet argument; its mathematical
fixture results are unchanged. Four earlier receipts and their pinned
sources are preserved byte for byte.

Run the registry validator, the conformance unittest suite, all five
existing receipt replays, and:

```sh
python experiments/surjective_rank_two.py --check
```

The same commands are enforced in CI. The claims registry and current
roadmap distinguish the two proved elementary results, the proved
general restricted theorem, and the computed finite census. Python
acceptance authority remains false. This contribution does not advance
the nonsurjective structural-data question beyond naming it as the
next research target.

Local validation: all 83 tests pass; all six receipts replay exactly;
14 claim records and their locators validate; all local Markdown links
resolve; all eleven inherited claim records are unchanged. The first
four receipt files are byte-identical to the baseline, and the fifth
has only its intentionally changed proof hash. Remote CI is checked
separately on the published commit.
