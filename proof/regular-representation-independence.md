# Regular-matroid representation independence of the bicycle tower

Claim: ABC-REGULAR-REPRESENTATION-INVARIANCE.

## Statement and label convention

Let A and A' be full-row-rank TU integer matrices of size r by e.
Suppose a specified bijection of their column labels identifies their
ordinary column matroids over $\mathbb Q$. After putting those columns
in the same order, there exist

$$
U\in\operatorname{GL}_r(\mathbb Z),\qquad
D=\operatorname{diag}(s_1,\ldots,s_e),\quad s_j\in\{1,-1\},
\qquad A'=UAD.
\tag{1}
$$

Including the specified relabeling gives $A'=UAS$, where S is a signed
permutation. The same U and S, independent of n, induce

$$
T_n:\operatorname{Bic}_n(A)\longrightarrow\operatorname{Bic}_n(A'),
\quad b\longmapsto S^\top b,
\qquad
F:K_A\longrightarrow K_{A'},\quad [d]\longmapsto[Ud].
\tag{2}
$$

Here $K_A=\mathbb Z^r/(AA^\top)\mathbb Z^r$. For all integers n at
least two, these are isomorphisms, they commute with the fixed-TU
isomorphisms, and T commutes with both reduction and inflation across
dividing moduli. Thus the compatible tower's **isomorphism class** is
independent of the TU representation of the regular matroid.

Naturality refers to specified equivalence witnesses. This theorem
does not assert that a comparison map is uniquely determined by the
unoriented matroid. Sections 1–3 prove the label-preserving equivalence;
Sections 4–6 establish the full tower transport.

## 1. Unit-basis normal forms preserve TU

Work first with aligned labels. A and A' represent the same matroid,
so choose one ordered common basis B. Its column submatrices C and C'
have determinant plus or minus one. Therefore their inverses are
integral. Put

$$
H=C^{-1}A,\qquad H'=(C')^{-1}A'.
$$

Both have identity columns at B. Every maximal minor of H is a maximal
minor of A divided by $\det C$, hence is zero or a unit.

Consider a nonzero k-by-k minor of H on row set I. Any identity column
$b_j$ in that minor must have $j\in I$, or its restriction is zero.
Append the identity columns at the complementary rows. They are distinct
from the chosen columns. Expanding the resulting maximal minor along
the appended identity columns gives the original minor up to sign.
It is therefore zero or a unit. This also proves the result for the
minors which were zero. Hence H is TU. The same reasoning proves H' TU.

In particular, their entries lie in $\{0,1,-1\}$. For $e\notin B$,
Cramer's rule gives

$$
H_{i,e}\ne0\quad\Longleftrightarrow\quad
B\setminus\{b_i\}\cup\{e\}\text{ is a basis}.
\tag{3}
$$

This is true for H' as well. The common labeled matroid thus determines
the same support in the nonbasis blocks of both normal forms.

An arbitrary unimodular row change need not preserve TU. This argument
uses the specific unit-basis normalization and its identity columns.

## 2. TU sign ratios have trivial cycle products

Make a bipartite graph with row vertices i and nonbasis-column vertices e.
Include edge (i,e) exactly where $H_{i,e}\ne0$, and give it ratio

$$
t_{i,e}=H'_{i,e}/H_{i,e}\in\{1,-1\}.
$$

On any chordless cycle of length 2k, its k row and k column vertices
select a square submatrix with exactly the cycle edges. There are
precisely two nonzero determinant terms, the two perfect matchings.
Each term is plus or minus one, so the determinant is in $\{-2,0,2\}$.
TU forces it to be zero, for both H and H'.

Let the matching products be p and q, with the same permutation signs
in the two matrices. Cancellation gives the same value of p/q for H
and H'. Taking ratios implies that the products of t on the two
matchings agree. Since each t is a sign, their joint product, namely
the product around the cycle, is one.

Every simple cycle with a chord splits into two shorter cycles.
Their products multiply to the product on the original cycle, because
the chord occurs twice and its square is one. Induction therefore
gives product one around every simple cycle. This argument is integral;
it does not extract signs from prime-field ranks.

Choose a sign at one vertex in every component and propagate signs
along a spanning tree. Trivial cycle products make the propagation
consistent on every remaining edge. Thus there are row signs alpha_i
and nonbasis-column signs beta_e such that

$$
t_{i,e}=\alpha_i\beta_e.
\tag{4}
$$

Isolated vertices impose no condition and can receive sign one.
This handles loops and isolated basis vertices, including coloops.

## 3. The labeled integral equivalence

Let $E_\alpha=\operatorname{diag}(\alpha_i)$. Define D on all columns
by $D_{b_i,b_i}=\alpha_i$ and $D_{e,e}=\beta_e$ off B. The identity
columns remain identity, since $\alpha_i^2=1$. Equations (3)–(4) give

$$
H'=E_\alpha HD,\qquad
A'=C'E_\alpha C^{-1}AD.
$$

Taking $U=C'E_\alpha C^{-1}$ proves (1). It is integral and unimodular
because every factor has that property.

For a prescribed matroid isomorphism, first reorder A's columns by
that bijection and then apply this labeled argument. The resulting
signed permutation has exactly that underlying permutation. For rank
zero, both matrices are zero; take the empty identity U and the
specified column permutation with positive signs. Empty ground sets
are included.

The known coordinate-equivalence theorem is also recorded as
Backman–Baker–Yuen, Section 2.1, Lemma 2.1.1 in the
[source audit](../sources/regular-representation-equivalence.md).
The proof above supplies the explicit labeled version used here.
No proof of arithmetic realization equivalence is imported from it.

## 4. Cuts, cycles, and Gram classes

Write $A'=UAS$. Since S is a signed permutation,
$SS^\top=I$, and U is invertible over every $\mathbb Z/n$.

For $b=A^\top y\bmod n$, take $y'=U^{-\top}y$. Then

$$
(A')^\top y'=S^\top A^\top y=S^\top b.
$$

So T takes cuts to cuts. Also $A'T(b)=UAb$, so it takes cycles to cycles.
Its inverse is the same formula for the inverse witness
$(U^{-1},S^\top)$. This proves each T_n is a module isomorphism.

Writing $Q=AA^\top$ and $Q'=A'(A')^\top$ gives

$$
Q'=UQU^\top,\qquad Q'\mathbb Z^r=UQ\mathbb Z^r.
$$

Consequently F in (2) is well defined and invertible. If b is a bicycle,
the already proved fixed-TU map satisfies

$$
\Phi'_n(T_n b)=[Q'y'/n]=[UQy/n]=F(\Phi_n b).
\tag{5}
$$

For the inverse square, $Qy=nd$ gives $Q'y'=nUd$, and the gradients
agree by the preceding calculation. Representative independence and
both inverse identities therefore persist under the equivalence.
These formulas work for all composite n without dividing in $\mathbb Z/n$.

## 5. One witness transports the whole tower

For $m=kn$, write reduction as $\rho_{m,n}$ and inflation as
$\iota_{n,m}(b)=kb\bmod m$. The integral matrix $S^\top$ commutes with
reduction and with multiplication by k:

$$
T_n\rho_{m,n}=\rho'_{m,n}T_m,\qquad
T_m\iota_{n,m}=\iota'_{n,m}T_n.
\tag{6}
$$

F likewise commutes with multiplication by k and with inclusions of
torsion subgroups. Thus (5) respects both tower maps and all their
divisibility chains. Choosing unrelated isomorphisms separately for
each modulus would not prove this result; the single integral witness
proves every compatibility at once.

For witnesses $(U_1,S_1)$ from A to A' and $(U_2,S_2)$ from A' to A'',
their composite is $(U_2U_1,S_1S_2)$. Its edge map is
$S_2^\top S_1^\top$ and its divisor map is $U_2U_1$.
Identity and inverse witnesses induce identity and inverse maps.
This states the precise naturality under specified equivalences.

## 6. What independence means, and the remaining arithmetic gate

For $A=[1,1,1]$ and $A'=[1,1,-1]$, the bicycles modulo 3 are respectively
$(y,y,y)$ and $(y,y,-y)$. Their embedded edge sets differ, but the
column sign map identifies them and commutes with every tower map.

Even for the same A, the witnesses $(1,I)$ and $(-1,-I)$ are both valid.
They act by identity and negation on the nonzero bicycles modulo 3.
Therefore a unique comparison map does not follow from the matroid
alone. Deterministic witness selection in finite code is a choice,
not additional mathematical canonicity.

The TU hypotheses are essential to this regular-matroid theorem's
scope. The integral matrices $[1,1]$ and $[1,2]$ have the same ordinary
matroid and are both split-surjective, but their bicycles modulo 2
have different orders, two and one. The second matrix is non-TU.
Their arithmetic multiplicities also differ, so this example does
not decide arithmetic realization invariance.

ABC-MAIN and ABC-REALIZATION-INVARIANCE remain open. The previously
withdrawn universal torsion-group model remains retracted. The next
research obligation is exact arithmetic-matroid equality and fixtures;
no general arithmetic claim is promoted by this regular result.

## 7. Exact evidence and authority

The candidate finds sign ratios in unit-basis normal forms and verifies
the final integral matrix equation and unit determinant. A separate
oracle enumerates column signs using a different unit basis, uses
Bareiss/Cramer calculations, and checks every subset's rational rank.

Regression fixtures include loops, coloops, disconnected components,
a chordless six-cycle in the support graph, changed row bases, graphic
and cographic representations, prescribed relabelings, and composite
moduli. Tests cover Gram classes, both modulus maps, witness composition,
invalid witnesses, and nonunique self-comparisons. The original graph
and fixed-TU proofs, receipts, and accepted claim records remain intact.

The integral proof supplies authority. Candidate Python, brute witness
search, and finite receipts supply implementation evidence. A separate
claim record identifies this regular representation-independence result.
