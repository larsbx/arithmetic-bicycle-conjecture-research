# Arithmetic Bicycle Conjecture Research Program

Research workspace for integral modular bicycle theory, exact arithmetic-matroid data, and corrected realization-invariance questions. The original **Arithmetic Bicycle Conjecture (ABC)** is refuted by a [rank-two counterexample](proof/arithmetic-realization-counterexample.md).

## Original conjecture — refuted

Let \(\mathcal M=(M,m)\) be a torsion-free representable arithmetic matroid with integral realization
\[
A\in\mathbb Z^{r\times E}.
\]
For \(n\ge2\), define
\[
C_n(A)=\operatorname{im}(A^\top\bmod n),\qquad
Z_n(A)=\ker(A\bmod n),
\]
and
\[
\operatorname{Bic}_n(A):=C_n(A)\cap Z_n(A)\subseteq (\mathbb Z/n)^E.
\]

> **Withdrawn Arithmetic Bicycle Conjecture (refuted 2026-10-14).** The compatible tower
> \[
> \{\operatorname{Bic}_n(A)\}_{n\ge2}
> \]
> depends only on \(\mathcal M\), not on the chosen integral realization \(A\).

The bootstrap's asserted equivalent finite-group formulation is withdrawn.
For the torsion-free arithmetic matroid realized by A=[2] in Z,
Bic_2(A)=0 and Bic_4(A)=Z/2. Every abelian group with zero 2-torsion
also has zero 4-torsion, so no single group represents that tower.
See the [counterexample proof](proof/arithmetic-torsion-model-obstruction.md).
The original realization-invariance statement is now also refuted.
In the same ambient lattice, the two realizations

$$
A=\begin{pmatrix}1&1\\0&5\end{pmatrix},\qquad
A'=\begin{pmatrix}1&2\\0&5\end{pmatrix}
$$

have identical complete arithmetic data: subset ranks 0,1,1,2 and
multiplicities 1,1,1,5. Yet their bicycle orders are one and five at
both moduli 5 and 10. See the
[counterexample proof](proof/arithmetic-realization-counterexample.md).
The finite-group model remains proved for graph and fixed full-row-rank
TU representations.

## Baseline theorem ladder

The program is deliberately staged:

| Stage | Obligation | State |
| --- | --- | --- |
| G0 | Graph modular-bicycle isomorphism for arbitrary moduli | Proved |
| R0 | Fixed full-row-rank TU representation | Proved |
| R1 | Regular TU representation independence of the full tower | Proved |
| A0 | Exact essential arithmetic-matroid equality and fixtures | Proved and implemented |
| A1 | Explicit arithmetic realization counterexample | Proved |
| ABC | Original torsion-free realization-invariance statement | Refuted; refinement next |

Thread-derived arguments begin as `working` until they are reproduced by repository proof records or executable evidence.

## Authority planes

- `proof/` — theorem statements, proof records, claim states.
- `kernel/` — candidate exact graph and fixed-TU maps; future canonical module algorithms.
- `oracles/` — independent, non-authoritative cross-checks.
- `experiments/` — exploratory searches only.
- `conformance/` — replayable fixtures and receipts.
- `sources/` — literature/source provenance.
- `docs/` — research status, audits, roadmaps.
- `paper/` — publication surface consuming accepted claims.

Projective / Grassmannian geometry is a **derived field-valued shadow** of the integral theory, not acceptance authority for lattice/SNF/torsion claims.

## Current status

The graph modular-bicycle theorem is `proved` for every integer modulus
at least two. Its integral proof supplies representative independence,
both inverse directions, graph naturality, and compatible reduction and
inflation maps. Independent exact Smith-factor and critical-group checks
support it with composite-modulus fixtures and source-pinned receipts.

The fixed-TU regular-matroid theorem is also `proved` for every modulus.
Its integral right inverse makes the representative arguments work over
composite rings. Independent Smith factors, cycle completion, and quotient
enumeration support it, including a cographic K3,3 fixture and labeled
non-TU controls.

The regular TU representation-independence theorem is now `proved`.
A specified matroid label isomorphism gives an integral row equivalence
and signed column map that transports the entire tower. The proof covers
the tower's isomorphism class; comparison maps depend on the chosen
witness. Independent all-subset rank and signed-search checks support it.

The exact essential arithmetic signature theorem is `proved`, with
verified rectangular Smith certificates and a separate all-minors oracle.
The original ABC and arithmetic realization-invariance statements are
`retracted` by the new counterexample. The earlier unconditional
finite-group strengthening remains a separate `retracted` claim.

The next target is an explicitly stated refinement, beginning with
surjective essential arithmetic representations. The declared
torsion-free domain of the original conjecture is preserved in its
withdrawn statement.

Start with:

1. [Graph proof](proof/graph-modular-bicycle.md)
2. [Fixed-TU proof](proof/regular-modular-bicycle.md)
3. [Regular representation-independence proof](proof/regular-representation-independence.md)
4. [Current status](docs/research/status-2026-10-14.md)
5. [Roadmap](docs/research/roadmap.md)
6. [Claim registry](proof/claims.toml)
7. [Exact replay commands](conformance/README.md)
8. [Independent graph audit](docs/audits/graph-modular-bicycle-2026-10-09.md)
9. [Fixed-TU contribution audit](docs/audits/regular-modular-bicycle-2026-10-09.md)
10. [Independent fixed-TU acceptance audit](docs/audits/regular-modular-bicycle-independent-2026-10-09.md)
11. [Regular representation proof audit](docs/audits/regular-representation-independence-2026-10-11.md)
12. [Arithmetic equality proof](proof/arithmetic-matroid-signature.md)
13. [Principal counterexample](proof/arithmetic-realization-counterexample.md)
14. [Arithmetic proof audit](docs/audits/arithmetic-matroid-2026-10-14.md)
