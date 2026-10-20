# Regular representation-independence proof audit — 2026-10-11

Claim: ABC-REGULAR-REPRESENTATION-INVARIANCE.
Base: merged main 23053222c2acdf9b6ff74f0f2499b44af9c3684a.
The graph and fixed-TU contributions, including their independent
acceptance audits, are already merged. This is the new contribution
author's proof audit; it does not claim a separate-person review.

## Mathematical gate

The source lemma's full-row-rank TU setting and permitted column
permutations were checked. The local proof derives the stronger labeled
statement directly after aligning a specified matroid isomorphism.

| Obligation | Audited argument |
| --- | --- |
| Common integral coordinates | A common basis gives two unit column matrices and integral inverses. |
| Normalization preserves TU | A nonzero square minor extends using complementary identity columns to a maximal minor, whose determinant is zero or a unit. Arbitrary row changes are not assumed to preserve TU. |
| Labeled support equality | A normal-form entry is nonzero exactly when replacing its basis element by the corresponding nonbasis element gives a basis. |
| Sign-ratio consistency | A chordless bipartite cycle has exactly two determinant terms. TU forces cancellation in both normal forms, so its ratio product is one. Chord splitting proves this for every cycle. |
| Integral equivalence | Spanning-tree sign propagation gives row and column signs; combining them with the unit basis changes gives U integral unimodular and A'=UAS. |
| Cut and cycle transport | S transpose sends gradients to gradients using y'=U inverse transpose y; A'S transpose b=UAb. |
| Gram quotient transport | Q'=UQU transpose gives Q'Z^r=UQZ^r; divisor classes move by U. |
| Forward and inverse squares | Q'y'/n=UQy/n and Qy=nd implies Q'y'=nUd. |
| Full tower compatibility | One integral S works for every modulus and commutes with reduction and scaled inflation. |
| Naturality | Composition uses U2U1 and S1S2; identity and inverse witnesses give the corresponding maps. |
| Degenerate cases | Rank zero, empty ground sets, loop columns, isolated support vertices, and disconnected components are included. |

No field-rank argument is used to prove equivalence or arbitrary-modulus
compatibility. Gram invertibility over a residue ring is never assumed.
The proof closes the TU representation gate for the tower's isomorphism
class; it does not assert a unique comparison map from the matroid alone.

For the same one-row matrix [1,1,1], identity and simultaneous global
row/column negation are both valid witnesses and act differently on
nonzero bicycles modulo 3. This supplies a concrete canonicity boundary.
The matrices [1,1,1] and [1,1,-1] also have unequal embedded bicycle
sets; a signed coordinate isomorphism is the proved relationship.

## Executable evidence

The candidate uses the first source unit basis, integral normal forms,
and bipartite sign propagation. Its witness constructor independently
checks strict integer domains, a genuine label permutation, unit signs,
a unit row determinant, and the entire integer matrix equation.
Its forward maps validate the source and target bicycle domains.
Inverse and composition create new verified witnesses.

The separate oracle imports no kernel code. It checks every column
subset's rational rank with Bareiss determinants, chooses a different
unit basis, uses Cramer inverses, and enumerates all column signs.
It therefore does not reuse the candidate support-graph solver or
infer matroid equality from Gram Smith data.

Eleven new regressions pass. The source-pinned receipt covers nine
explicit matrix pairs, 46 modulus cases, and 57 proper tower pairs.
Fixtures include a chordless support six-cycle, loops, coloops,
disconnected components, prescribed relabelings, changed Gram coordinates,
and graphic and cographic representations. Independent Smith factors
and quotient enumeration check the Gram transport, including the
noncyclic cographic K3,3 group.

The complete ternary 2-by-3 census contains 456 full-row-rank TU matrices
in seven labeled matroid buckets. All 456 comparisons with their bucket
representative are verified by both routes, and their towers are checked
at four moduli, for 1,824 transport cases. All 42 ordered comparisons
between different bucket representatives are rejected.

Tests additionally cover both inverse identities, both Gram squares,
large integral representative changes, nontrivial witness composition,
all fixture modulus chains, and a composite modulus exceeding 2^80,
using quotient classes rather than modulus-sized enumeration.

Negative controls reject invalid signs, permutations, row matrices,
bicycle inputs, divisor dimensions, modulus domains, and mismatched
composition endpoints. Equal Gram matrices and equal Smith factors for
[1,1,0] and [1,0,1] do not certify labeled matroid equality; the witness
finder rejects identity labels and accepts the correct prescribed
relabeling. A single inconsistent sign on a chordless support cycle is
rejected as non-TU.

The ordinary matroid of [1,1] and [1,2] is the same, but their bicycles
modulo 2 have orders two and one. Both matrices are split-surjective;
only the first is TU. This is a negative scope control, not an ABC
counterexample: their arithmetic multiplicities differ.

## Authority and preserved claims

The integral proof is theorem authority. Python remains candidate code
with acceptance authority false. The seven existing claim records are
preserved verbatim; the new regular representation-independence claim
is separate. ABC-MAIN and ABC-REALIZATION-INVARIANCE remain open,
and the universal torsion-model strengthening remains retracted.

The original graph and fixed-TU proof records, candidate modules,
oracles, fixtures, tests, replays, receipts, and dated audits remain
unchanged. The new receipt pins its own proof, source audit, witnesses,
oracle, fixtures, tests, replay, and inherited exact primitives.

All 52 conformance tests pass on Python 3.12.14. All three source-pinned
receipts replay without drift, eight claims pass the registry gate, and
preserved-record comparisons and patch whitespace checks pass.
Validation commands are recorded in
[conformance/README.md](../../conformance/README.md).
Remote review and CI remain separate publication-time checks.
