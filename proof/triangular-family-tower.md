# Nonsurjective triangular-family bicycle towers

Task: **ABC-RD-01**, triangular-family subproblem.
**Status: working mathematical proof draft**; not a registered proved claim.
This does not close ABC-RD-01 for general nonsurjective realizations.
The original **ABC-MAIN**, **ABC-REALIZATION-INVARIANCE**, and
**ABC-UNIVERSAL-TORSION-MODEL** remain retracted.

## Domain and arithmetic data

Fix integers \(b\ge2\) and \(a\) with \(\gcd(a,b)=1\), and set

\[
A_{a,b}=\begin{pmatrix}1&a\\0&b\end{pmatrix}.
\]

Work in the declared ambient lattice \(\mathbb Z^2\), with labeled
columns and the standard coordinate pairing. All primitive \(a\)
at fixed \(b\) have identical complete labeled arithmetic data:
subset ranks \(0,1,1,2\), multiplicities \(1,1,1,b\).
Each singleton column is primitive, and the determinant has absolute
value \(b\). In particular \(m(E)=b>1\), so these realizations are
nonsurjective. Let

\[
H_n(a,b)=\operatorname{im}(A_{a,b}^{T}\bmod n)
          \cap\ker(A_{a,b}\bmod n)\subseteq(\mathbb Z/n)^2.
\]

The transition maps, for \(n\mid m\), are reduction modulo \(n\)
and scaled inflation by \(m/n\) modulo \(m\).

## Subgroup at every modulus

Set \(g=\gcd(b,n)\), \(q=n/g\), and \(c=1+a^2\).
A vector \((x,z)\) is a cycle if and only if

\[
x+az=0\pmod n,\qquad bz=0\pmod n.
\]

It is also a cut precisely when there exist potentials \(s,t\) with
\((x,z)=(s,as+bt)\pmod n\). Taking \(s=x=-az\) leaves the congruence
\(bt=cz\pmod n\), solvable exactly when \(g\mid cz\).
The cycle condition \(bz=0\pmod n\) holds precisely when
\(z=qk\pmod n\) for a unique \(k\in\mathbb Z/g\).
Therefore there is an explicit additive bijection

\[
\boxed{
\ker(cq:\mathbb Z/g\to\mathbb Z/g)
 \stackrel{\sim}{\longrightarrow}H_n(a,b),\
 k\longmapsto(-aqk,qk)\bmod n.
}
\]

In particular the bicycle group is cyclic of order

\[
\boxed{
h_n(a,b)=\gcd(g,cq)
=\gcd\left(\gcd(b,n),(1+a^2)\frac{n}{\gcd(b,n)}\right).
}
\]

More strongly, its possible second coordinates form the unique subgroup
of \(\{z\bmod n:bz=0\}\cong\mathbb Z/g\) having order \(h_n\).

## Classification at fixed b and coherent transport

For two primitive parameters \(a,a'\) at the same fixed \(b\), put
\(c=1+a^2\), \(c'=1+(a')^2\). Their full additive bicycle towers
(including both transition maps) are isomorphic if and only if

\[
\boxed{\gcd(b,c)=\gcd(b,c').}
\]

**Necessity.** Taking \(n=b\) gives \(g=b,q=1\) and
\(|H_b(a,b)|=\gcd(b,c)\); different values imply different groups.

**Sufficiency.** For each prime dividing \(b\), equality of
\(\gcd(b,c)\) and \(\gcd(b,c')\) gives equality of truncated
valuations \(\min(v_p(b),v_p(c))=\min(v_p(b),v_p(c'))\).
Since \(g\mid b\), for every \(n\) we have
\(\gcd(g,cq)=\gcd(g,c'q)\). By uniqueness of subgroups in a cyclic group,
the allowed sets of second coordinates are literally identical for
the two parameters, at every modulus. Thus

\[
F_n:H_n(a,b)\longrightarrow H_n(a',b),
\quad(-az,z)\longmapsto(-a'z,z)
\]

is an additive bijection. Because it uses fixed integral coefficients
on the second coordinate, it commutes with reduction and scaled
inflation \(z\mapsto (m/n)z\), and hence their compositions.
This proves coherence, not merely levelwise equality of orders.

In the \(k\)-coordinates, for \(n\mid m\), write \(g_j=\gcd(b,j)\)
and \(q_j=j/g_j\). Then \(q_n\mid q_m\) and \(g_n\mid g_m\).
Reduction sends \(k_m\mapsto(q_m/q_n)k_m\bmod g_n\);
inflation sends \(k_n\mapsto(g_m/g_n)k_n\bmod g_m\).
The maps are generally not inverses.

**Scope limit.** These are additive bicycle subgroup isomorphisms.
They need not extend to integral row/sign equivalences or to
orthogonal transformations of the full edge space. The formula
classifies only this triangular normal form at fixed \(b\), not
arbitrary nonsurjective arithmetic realizations. It makes no claim
of unique canonical comparison from arithmetic-matroid data.

## Explicit positive and negative controls

* At \(b=5\), \(a=1\) gives \(c=2\) and bicycle orders \(1,1,5\)
  at moduli \(5,10,25\), while \(a=2\) gives \(c=5\) and orders
  \(5,5,5\). Equal arithmetic data do not imply equal towers.
  Agreement at modulus 25 cannot erase mismatches at 5 or 10.
* At \(b=13\), \(a=1\) and \(a=2\) have \(\gcd(13,2)=\gcd(13,5)=1\).
  Their bicycle towers agree, with orders \(1,1,13\) at
  moduli \(13,26,169\), using the explicit maps \(F_n\).
* For every divisor \(d\mid n\), the annihilator profile of this
  cyclic group is \(|H_n[d]|=\gcd(d,h_n)\).
  No invalid nonsurjective Gram-cokernel torsion formula is assumed.

## Bounded independent verification

Execute the independent experiment with Python 3:

    python experiments/triangular_family.py
    python -m unittest conformance.test_triangular_family

The experiment enumerates literal potentials (not a Gram-torsion
shortcut) for primitive \(0\le a<b<16\) and \(2\le n<30\),
checks 1,988 cases, checks 155 equal-class labeled parameter pairs,
and 6,200 commuting reduction/inflation instances. It also directly
checks the index-five and index-thirteen controls.

These fixed bounds are finite corroboration, not a census of all
representations. This mathematical draft has not received independent
mathematical review or a source-pinned conformance receipt; no claim
registry promotion is proposed here.

Next steps: independent mathematical audit and pinned evidence, followed
by systematic classification of nonsurjective realizations beyond the
triangular family and the embedded-lattice/map/pairing obligations of
ABC-MODULE-01.
