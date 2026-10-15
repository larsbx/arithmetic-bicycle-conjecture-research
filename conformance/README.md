# Conformance

Versioned fixtures, canonical encodings, receipts, and counterexamples for replayable exact checks.

## Graph modular-bicycle evidence v1

Run from the repository root with Python 3.11 or later. No external packages
are required:

```sh
python conformance/check_claims.py
python -m unittest discover -s conformance -p 'test_*.py' -v
python conformance/replay_graph_modular_bicycle.py --check
python conformance/replay_regular_modular_bicycle.py --check
python conformance/replay_regular_representation.py --check
python conformance/replay_arithmetic_matroid.py --check
python conformance/replay_surjective_representation.py --check
git diff --check
```

The original 17 conformance tests cover ten explicit multigraph fixtures at 53
moduli, and all 44 connected labeled simple graphs with at most four
vertices at moduli 2, 3, 4, and 6 (176 further graph/modulus cases).
The fixtures are constructions listed by their complete edge lists, not
an imported census. Loops have zero incidence columns and parallel edges
are separate coordinates.

The graph suite has 21 tests. Four additional
[independent review regressions](test_graph_modular_bicycle_audit.py) cover
all mixed edge orientations and vertex permutations on a doubled triangle,
single-vertex and loop-only graphs, large integral lift changes, and a
noncyclic `Z/2 + Z/6` tower through modulus 72. They check 37 further proper
tower pairs and 55 strict three-modulus chains. The original pinned receipt
retains its 53-case and 70-pair scope. See the
[October 9 independent audit](../docs/audits/graph-modular-bicycle-2026-10-09.md).

Two independent routes must agree:

| Candidate implementation | Independent oracle |
| --- | --- |
| Incidence-product Laplacian | Direct multiplicity Laplacian |
| Normalized-potential enumeration | Chord-valued cycles completed by tree leaf elimination |
| Rational Gauss-Jordan inverse | Exact Bareiss determinants and Cramer's rule |
| Explicit forward and inverse maps | Independently enumerated critical-group quotient |
| Bicycle element orders | Smith factors from gcds of all minors |

Both use integers and exact fractions. The oracle imports no kernel code;
it does not call the proposed theorem map to derive expected counts or
classes. A third literal edge/potential enumeration checks its tree method
on fixtures with at most four edges. Bareiss determinants are checked
against permutation expansion, and Smith factors against planted
unimodular transforms, including singular matrices.

Tests check both inverse identities, sampled integral representative
changes for every fixture bicycle, every computational root, linearity,
signed edge permutations, vertex relabeling, and both modulus maps and
their compositions. Negative tests reject non-cycles, non-cuts, incorrect
potentials, non-torsion divisors, invalid domains, and non-dividing tower
maps. They demonstrate why arbitrary edge lifts, unscaled inflation, and
assuming surjective reduction are invalid, and why mod-2 ranks miss
mod-4 exponents.

The checked-in JSON receipt records fixture results, element-order
profiles, bijection checks, tower checks, bicycle-set hashes, and hashes
of its source files and proof record. Replay compares canonical bytes and
fails on drift. After an intentional source change, inspect the cause and
regenerate with:

```sh
python conformance/replay_graph_modular_bicycle.py --write
```

Enumeration is exhaustive within the stated finite fixtures. There are no
silent caps or timeouts. Potential enumeration is exponential in V-1;
chord enumeration is exponential in E-V+1; the all-minors Smith oracle is
also for small matrices. These checks support the separate integral proof
and do not establish any arithmetic-matroid realization-invariance claim.

## Fixed-TU modular-bicycle evidence v1

The original 16 fixed-TU tests take the combined suite to 37. Seven explicit TU matrices
cover 36 modulus cases and 44 proper tower pairs in the new receipt.
They include rank zero with loop columns, identity coloops, parallel
elements, reduced graphic incidence matrices, and the cographic K3,3
fundamental-cycle matrix. Its Gram Smith factors (1,3,3,9) exercise both
noncyclic torsion and prime-power exponents at moduli 3,6,9.

| Candidate implementation | Independent oracle |
| --- | --- |
| Rational-elimination determinants for every TU minor | Bareiss determinants |
| First unit column basis and integral right inverse | Last unit column basis and Cramer inverse |
| Enumeration of normalized potentials | Nonbasis edge coordinates completed to cycles, then tested as cuts |
| Gauss–Jordan Gram coordinates and theorem maps | Cramer coordinates and quotient enumeration from generators |
| Bicycle orders | All-minor Smith factors and torsion order profiles |

The cycle oracle is also checked against literal edge/potential enumeration
on small fixtures. The tests classify every one of the 729 ternary 2-by-3
matrices: all 456 full-row-rank TU cases agree with the oracle and Smith
counts at moduli 2,3,4,6, giving 1,824 further matrix/modulus regressions.
Graph specialization agrees at every root of every original graph fixture.

Tests cover both inverse identities, integral potential and divisor
changes, large edge lifts, every bicycle pair's addition, integer scaling,
signed column permutations, a nonorthogonal unimodular row transformation,
and every fixture divisibility chain and both modulus-map composites.
Invalid representatives and domains are rejected.

Two separately labeled non-TU controls provide 12 further receipt cases.
A=[2] exhibits ambiguous potential images and contradicts the unconditional
finite-group torsion model; A=[1,2] has an integral right inverse and
satisfies the broader split-surjective lemma. Non-TU by itself is not a
failure signal. The [counterexample proof](../proof/arithmetic-torsion-model-obstruction.md)
withdraws the group strengthening and leaves realization invariance open.

The new replay pins the new proof records, candidate, independent oracle,
fixtures, tests, replay program, and inherited graph primitives by SHA-256.
The original graph receipt retains its scope and bytes. Regenerate only
after investigating an intentional change:

```sh
python conformance/replay_regular_modular_bicycle.py --write
```

All enumeration is exhaustive within its stated finite scope. TU
certification checks all square minors; potential enumeration costs n^r;
cycle enumeration costs n^(e-r). These are small-fixture algorithms with
no silent truncation. The integral proof supplies theorem authority;
Python and both oracles remain non-authoritative candidate/evidence code.

Four [independent acceptance-review tests](test_regular_modular_bicycle_audit.py)
take the combined suite to 41. They cover 48 signed column changes combined
with a row change that loses TU (288 coordinate/modulus cases), the
noncyclic K3,3 quotient at large composite moduli, 51 additional proper
tower pairs and 105 strict chains, and literal scalar-two edge membership
through modulus 128. The non-TU coordinate cases use literal enumeration
and Cramer equations while the TU candidate correctly rejects their
matrices. Both original source-pinned receipts retain their bytes and
scope; the added tests are tracked separately in the reviewed Git tree.
See the [acceptance audit](../docs/audits/regular-modular-bicycle-independent-2026-10-09.md).

## Regular representation-independence evidence v1

Eleven new tests take the combined suite to 52. The new receipt verifies
nine explicit TU matrix pairs at 46 moduli and 57 proper tower pairs.
Every pair has a prescribed column-label permutation. The candidate
solves sign ratios in unit-basis normal forms, then checks a unit integer
determinant and the complete matrix equation. A separate oracle imports
no kernel code; it checks every column subset's rational rank and searches
all signs using a different unit basis and Bareiss/Cramer arithmetic.

Fixtures cover rank zero, empty ground sets, loops, coloops, disconnected
components, a chordless support six-cycle, nonorthogonal basis changes,
and graphic/cographic examples. Independent Smith factors and quotient
enumeration check the Gram transport. Tests verify both inverse squares,
divisor representatives, both tower maps and all fixture chains, witness
composition, and very large composite moduli without potential enumeration.

The complete ternary 2-by-3 census has 456 full-row-rank TU matrices in
seven labeled matroid buckets. Both routes verify all 456 comparisons
with a bucket representative and 1,824 tower cases. All 42 ordered
cross-bucket comparisons are rejected. Equal Gram/Smith data for distinct
labeled matroids do not pass the comparison gate.

Negative tests reject invalid witnesses and domains. They also show that
embedded edge sets and comparison maps need not be equal, and that non-TU
representations of the same ordinary matroid are outside this theorem.
The result concerns the tower's isomorphism class under TU representations;
arithmetic realization invariance remains open.

The new receipt pins its proof, source audit, candidate, oracle, fixtures,
tests, replay, and inherited exact primitives. Both older receipts and
their inputs remain unchanged. Rebuild intentional changes with:

```sh
python conformance/replay_regular_representation.py --write
```

All ranks and witnesses use exact integer arithmetic. All-subset rank
comparison, all-minor TU certification, and the sign oracle are intended
for small fixtures. No search is silently truncated. Deterministic witness
selection is a computational choice, not a unique matroid comparison map.

## Arithmetic equality and principal counterexample evidence v1

Thirteen new tests take the combined suite to 65. Fourteen essential
integer realizations supply 91 complete subset records, six labeled
comparisons, and 20 bicycle cases in the new receipt.

| Candidate route | Independent route |
| --- | --- |
| Euclidean Smith reduction with both transforms | Gcds of all rectangular minors using Bareiss determinants |
| Verified Smith rank and torsion-order products | Independently computed rank/index pairs for every subset |
| All-potential bicycle enumeration with duplicate cuts removed | All-edge enumeration with modular cut membership tested by lattice indices |
| Complete arithmetic encodings and exact subset comparison | Independent complete rank/multiplicity signatures |

Certificates check dimensions, unit determinants, the full transformed
matrix equation, and a dividing positive diagonal followed by zeros.
The complete Smith regression covers all 15,625 integer 2-by-3 matrices
with entries in {-2,-1,0,1,2}. Empty, rectangular, singular, planted,
and large-integer cases are included. The original seven TU fixtures
have unit multiplicities at all 648 subsets.

The principal counterexample matrices `((1,1),(0,5))` and
`((1,2),(0,5))` have identical subset ranks 0,1,1,2 and multiplicities
1,1,1,5. Yet their bicycle orders are one and five at moduli 5 and 10.
The receipt contains their full modular edge sets and order profiles,
checked by both independent routes and inherited literal cut enumeration.
The [elementary counterexample proof](../proof/arithmetic-realization-counterexample.md)
supplies refutation authority independently of bounded computation.

Negative controls reject invalid certificates, domains, masks, and label
permutations. They detect different lower-subset multiplicities even
when rank profiles, singleton data, and the ground-set index agree;
identical full-set Smith factors do not certify arithmetic equality.
Saturation is not an allowed shortcut for changing the declared ambient
lattice. Complete data equality still does not certify realization or
bicycle equivalence, as the counterexample demonstrates.

The modular cut oracle compares indices of `[A^T | n I]` and its
augmentation by an edge vector. Equal indices mean that vector is in
the same integer lattice. This criterion works over every composite
modulus and assumes no Gram-group torsion formula for nonsurjective
realizations.

The new receipt pins the arithmetic proofs, source audit, code, fixtures,
tests, replay, and inherited exact primitives. All three older receipts
and their mathematical inputs are unchanged. Intentional source changes
must be investigated before regenerating:

```sh
python conformance/replay_arithmetic_matroid.py --write
```

Canonical multiplicities are positive decimal strings, including indices
exceeding 2^80. Equality compares complete data, not hashes. The interface
is essential and uses declared free ambient lattices; it does not admit
arbitrary serialized tables as representability certificates. All finite
enumerations are exhaustive within their stated fixture scopes, with no
silent truncation. This packet is not a census of all realizations.

Current principal claim states are retracted; earlier open-status notes
in pinned proofs and dated audits describe the pre-counterexample state.
See the [October 14 audit](../docs/audits/arithmetic-matroid-2026-10-14.md).

The regular-representation v1 receipt's `arithmetic_realization_invariance:
open` annotation records its October 11 source bundle. Replaying that
bundle preserves its evidence and bytes; current claim status is retracted
in the registry and supported by the new counterexample packet.

## Surjective arithmetic realization-invariance evidence v1

Fifteen new tests take the combined suite to 80. The separately scoped
claim is ABC-SURJECTIVE-REALIZATION-INVARIANCE, for essential free-lattice
representations with m(E)=1. All retracted unrestricted claims remain
retracted.

Ten positive pairs supply 38 modulus cases and 33 proper tower pairs
in the new receipt. Tests also verify all six strict three-modulus
chains in those fixtures. Three source fixtures have no unit maximal
minor: (2,3), the rank-two matrix with minors 6,2,-3, and a disconnected
extension with a coloop and loop. Their Smith-derived splittings are
verified by the complete integer right-inverse equation.

| Candidate route | Independent route |
| --- | --- |
| Smith transformations certify an integral surjection | Gcds of Bareiss maximal minors |
| Rational basis and support-graph signs | A different rational basis, Cramer inverse, and exhaustive column-sign search |
| Normalized-potential bicycle enumeration | Edge enumeration with lattice-index cut membership |
| Gram maps and rational class coordinates | All-minor Smith factors and quotient enumeration from generators |

Literal cuts provide a third finite check. The fixtures cover C13 at
moduli 13,26,52,169, C49 at 7,14,49, noncyclic C3+C3, zero rank,
loops, a support six-cycle, and row changes that lose literal TU.
The new maps also agree with all seven inherited TU fixtures.
Independent algorithms do not imply separate-person acceptance review.

The complete ternary 2-by-3 census contains 552 integral surjections
in ten arithmetic buckets, including 96 non-TU matrices. Every matrix
is compared with its bucket representative, with 2,208 transport cases
at moduli 2,3,4,6. All 90 ordered comparisons between distinct bucket
representatives are rejected by both witness routes.

Tests verify both inverse identities, representative independence,
linearity, both Gram squares, potential transport, both tower directions
and their compositions, witness inversion/composition, and nonunique
comparison maps. Large composite moduli are checked without enumerating
potential spaces. At modulus 49 the rank-two fixture has elements of
order 49, invisible at modulus 7. Reduction from 169 to 13 for (2,3)
is zero even though the target has thirteen bicycles.

Two negative arithmetic pairs include an equal-magnitude support
six-cycle with conflicting signs: its two relevant determinant
magnitudes are 25 and 23. Three nonsurjective rejection fixtures include
both members of the principal counterexample. Their equal arithmetic
data and differing bicycle orders remain independently tested.
Invalid representatives, forged witnesses, nondividing modulus maps,
and populated-cache bool/float aliases are rejected.

The fifth receipt pins its proof, source audit, fixtures, tests, replay,
candidate, independent oracle, and all inherited exact dependencies.
All four earlier receipts and their source files retain their bytes.
After investigating an intentional change, rebuild with:

```sh
python conformance/replay_surjective_representation.py --write
```

All enumeration is exhaustive within the stated finite scope, without
silent truncation. These are small-fixture algorithms, not a scalable
arithmetic classification. The integral proof is theorem authority;
Python acceptance authority remains false.
