# Surjective rank-two three-edge cyclic classification

Status: established by the argument below; partial Lean formalization is
**unverified** until compiled. Executable conformance is bounded evidence,
not a proof. This specializes the existing surjective realization theorem;
it does not reinstate ABC-MAIN, ABC-REALIZATION-INVARIANCE, or
ABC-UNIVERSAL-TORSION-MODEL, all of which remain retracted.

Let A be an integer 2 by 3 matrix whose maximal minors have gcd one.
Let G=AAᵀ and Δ=det(G). For every integer n≥1,

    Bic_n(A) = im(Aᵀ mod n) ∩ ker(A mod n) ≅ Z/gcd(n,Δ)Z.

The n=1 assertion uses the trivial group; the repository executable API
uses n≥2. Loops and parallel columns are permitted. Three columns and
surjectivity are essential hypotheses of this cyclicity argument.

## Primitive Gram matrix, including characteristic two

For every prime p at least one maximal minor is nonzero modulo p, so
the two rows span a two-dimensional subspace W of F_p³. The standard
dot product is nondegenerate in every characteristic, including two.
If G vanished modulo p, W would be contained in W-perp. Nondegeneracy
implies dim(W-perp)=3-dim(W)=1, contradicting dim(W)=2.
Thus no prime divides all entries of G, and their integer gcd is one.
Cauchy–Binet gives Δ=d12²+d13²+d23²>0. The determinantal-divisor
characterization of integer Smith form now gives diag(1,Δ).
This argument does not assume that some maximal minor is ±1.

## Modular cut/cycle identification and group structure

An integral right inverse T exists because A is surjective over Z;
TᵀAᵀ=I remains true modulo every n, so Aᵀ is injective modulo n.
It restricts to an additive isomorphism ker(G mod n) → Bic_n(A).
Conversely any bicycle is Aᵀy, and its cycle equation is Gy=0;
the potential y is unique modulo n.
Choose integer unimodular matrices P,V with PGV=diag(1,Δ).
Writing y=Vz identifies that kernel with {(0,z2): Δz2=0 mod n}.
This is cyclic of order g=gcd(n,Δ), generated in z coordinates by
(0,n/g). This proves group structure, rather than only cardinality.

## Coherent maps across moduli

Fix P,V once over Z, independently of n. The cyclic kernel model is
H_n={z in Z/n: Δz=0}. Its maps for m=kn are z↦z mod n (reduction)
and z↦kz mod m (scaled inflation). They commute with y=V(0,z)
and the edge map Aᵀ. They compose along divisibility chains.

For a single fixed ambient cyclic group C_Δ=Z/Δ, the identification
H_n → C_Δ[n] is z↦[Δz/n], using an integer lift. The quotient is
integral and a lift change adds Δ. It is injective and surjective:
[Δz/n]=0 implies n divides z, and nd=Δz is precisely n[d]=0.
Reduction m→n becomes multiplication by k on C_Δ torsion;
scaled inflation becomes inclusion C_Δ[n]⊆C_Δ[m]. These are the
same maps as the existing Gram-cokernel identification [Gy/n].
In particular reduction need not be surjective: Δ=49, 343→7 has
zero reduction and a nontrivial target.

In the individually normalized abstract groups C_gn → C_gm,
where gn=gcd(n,Δ), gm=gcd(m,Δ), inflation is t↦(gm/gn)t.
Reduction in the reverse direction is t↦(k*gn/gm)t mod gn.
The coefficient is integral because gm divides k*gn. These formulas
follow by substituting z_n=(n/gn)t; reduction coefficients are not
generally one. The isomorphisms depend on the fixed Smith choice.

## Arithmetic invariance and boundaries

Labeled arithmetic-matroid data give |dij|=m({i,j}) for independent
pairs and zero for dependent pairs. Therefore they determine Δ and
the isomorphism class of this entire two-map tower. No canonical
comparison map between different realizations is asserted.
This proves the specialization without needing representation uniqueness.

The b=7 family A(a,b) is excluded since m(E)=7. Dropping surjectivity
can break injectivity of Aᵀ. Increasing to four columns breaks Gram
primitivity: rows (1,0,1,0),(0,1,0,1) are surjective but G=2I,
so Bic_2=C2⊕C2, not cyclic. Neither boundary is a counterexample
to the stated theorem.

## Mechanization boundary

ABC/SurjectiveThreeEdge.lean supplies ring-level Cauchy–Binet,
split-transpose injectivity and cut/cycle normalization lemmas.
The finite-field dimension argument, Smith existence, cyclic equivalence,
and coherent tower equivalences remain **not mechanized** here.
No proof-registry claim is promoted by these partial files.
