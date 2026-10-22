# Exact nonparallel three-edge bicycle presentation

**Research status:** mathematical proof draft and independently checked finite controls.
This is an extension of the scoped ABC-RD-01 work, **not** a theorem
registration, full realization classification, or Lean-completed certificate.
Do not reinstate ABC-MAIN, ABC-REALIZATION-INVARIANCE or
ABC-UNIVERSAL-TORSION-MODEL (all **retracted**).

## Family and complete arithmetic signature

For \(b\ge2\) and \(\gcd(a,b)=\gcd(a+1,b)=1\), let

\[
A_{a,b}=\begin{pmatrix}1&a&a+1\\0&b&b\end{pmatrix}.
\]

Its columns are pairwise rationally nonparallel: the three labeled
\(2\times2\) determinants are \(b,b,-b\). Every singleton has gcd one.
Thus all admissible \(a\) at fixed \(b\) have the same complete subset
ranks and multiplicities: the empty set has \((0,1)\), every singleton
\((1,1)\), and every set of at least two elements \((2,b)\). The
ambient lattice is the declared \(\mathbb Z^2\) and \(m(E)=b>1\).

## Exact full-module presentation

Fix \(n\ge2\) and write \(g=\gcd(b,n)\). Define a subgroup of
\((\mathbb Z/n)^2\) by

\[
P_n(a,b)=\left\{(s,u):
 \begin{array}{ll}
 u-as=0 \pmod g,\\
 (a+2)s+(2a+1)u=0\pmod n,\\
 b(s+2u)=0\pmod n
 \end{array}\right\}.
\]

Here \(u-as=0\pmod g\) is a well-defined congruence because \(g\mid n\).
Then

\[
\boxed{\quad
P_n(a,b)\xrightarrow{\ \simeq\ }\operatorname{Bic}_n(A_{a,b}),
\qquad(s,u)\mapsto (s,u,s+u)\pmod n.\quad}
\]

**Proof.** Every cut is the transpose-image of a potential \((s,t)\)
and therefore has edge coordinates

\[
A^\mathsf T(s,t)=(s,as+bt,(a+1)s+bt).
\]

Setting \(u=as+bt\), the cut is \((s,u,s+u)\). Such a \(t\) exists
precisely when the standard linear congruence \(bt=u-as\pmod n\)
is solvable, i.e. \(g\mid (u-as)\). On this cut vector the two
cycle equations \(Ax=0\pmod n\) become exactly

\[
(a+2)s+(2a+1)u=0,\qquad b(s+2u)=0\pmod n.
\]

The map is additive and injective by its first two coordinates,
and the calculation shows its image is precisely the bicycle.
No division, field-rank argument, or nonsurjective Gram-torsion
identification is used.

**Coherent tower maps.** For \(n\mid m\), reduction is
\((s,u)_m\mapsto(s,u)\bmod n\), and scaled inflation is
\((s,u)_n\mapsto\frac mn(s,u)\bmod m\). Both preserve the displayed
congruences because the presentation comes from integral linear
cut/cycle maps, and the map \((s,u)\mapsto(s,u,s+u)\) commutes
coordinatewise. Thus this is an exact presentation of the **entire**
compatible tower for each member of the family. It is **not** a
classification of when two such towers are isomorphic.

## All-modulus group-order formula (not a group-structure assertion)

The Gram matrix is

\[
G=AA^\mathsf T=
\begin{pmatrix}
2(a^2+a+1)&b(2a+1)\\
b(2a+1)&2b^2
\end{pmatrix},
\qquad \det G=3b^2.
\]

Let
\[
d_1=\gcd(2(a^2+a+1),\,b(2a+1),\,2b^2),\quad
d_2=\frac{3b^2}{d_1}.
\]
Because \(G\) is a full-rank \(2\times2\) integer matrix,
the Smith factors are \(d_1\mid d_2\). In the general
[proved code-hull quotient](code-hull-tower.md), the bicycle module
is \(\ker(G\bmod n)/\ker(A^\mathsf T\bmod n)\).
The first coordinate of \(A^\mathsf T(s,t)\) is \(s\);
hence \(\ker(A^\mathsf T\bmod n)=\{(0,t):bt=0\bmod n\}\)
has size \(g=\gcd(b,n)\). By Smith diagonalization the Gram kernel
has size \(\gcd(n,d_1)\gcd(n,d_2)\). Consequently

\[
\boxed{\quad
|\operatorname{Bic}_n(A_{a,b})|
=\frac{\gcd(n,d_1)\gcd(n,d_2)}{\gcd(n,b)}.\quad}
\]

This identity counts the group correctly at all composite moduli,
but it **does not imply the group is cyclic**. The embedded
congruence presentation above retains the missing structure.
The formula at \(n=b\),
\(\gcd(b,2(1+a+a^2))\), has the independent scalar-line
proof in [the first three-edge note](nonparallel-three-edge.md).

## Necessary prime-power control: a noncyclic bicycle

For \(a=1,b=3,n=9\) take
\[
A=\begin{pmatrix}1&1&2\\0&3&3\end{pmatrix},\quad
G=\begin{pmatrix}6&9\\9&18\end{pmatrix}.
\]
Modulo nine, the Gram kernel consists of \(s\in\{0,3,6\}\)
with arbitrary second potential \(t\). The kernel of
\(A^\mathsf T\) consists of \(s=0\), \(t\in\{0,3,6\}\).
The bicycle is therefore
\[
\boxed{\operatorname{Bic}_9(A)\cong
(\mathbb Z/3)^2}
\]
with explicit independent order-three edge generators
\((3,3,6)\) and \((0,3,3)\). It has nine elements and exponent
three, whereas \(\operatorname{Bic}_3(A)\cong\mathbb Z/3\).
This is a negative control against treating the three-edge
family's full tower as universally cyclic.

## Reproduction and outstanding classification

The separate, non-authoritative
[experiment](../experiments/three_edge_structure.py)
enumerates literal potentials and separately enumerates the
\((s,u)\)-presentation; it also compares each group order to the
independently derived Gram/Smith expression. Fixed disclosed
bounds: \(3\le b\le13\), admissible \(0\le a<b\), and
\(n\in\{2,3,5,7,9,14,21,27\}\): **256 exact triples**.
Prime-power generators are explicitly checked.

    python experiments/three_edge_structure.py
    python -m unittest conformance.test_three_edge_structure

The calculation and paper derivation do not constitute a Lean
formalization or a source-classified normal-form completeness theorem.
Remaining obligations are to characterize tower-equivalence classes
across \(a\), prove sufficient embedded-lattice/pairing data for
ABC-MODULE-01, build independent proof review, and add a replayable
source-pinned v3 receipt for the new all-modulus packet.
