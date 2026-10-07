# Arithmetic Bicycle Conjecture Research Program

Research workspace for the **Arithmetic Bicycle Conjecture (ABC)**: whether the full modular bicycle tower attached to an integral realization of a torsion-free representable arithmetic matroid is determined by the arithmetic matroid itself.

## Principal conjecture

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

> **Arithmetic Bicycle Conjecture.** The compatible tower
> \[
> \{\operatorname{Bic}_n(A)\}_{n\ge2}
> \]
> depends only on \(\mathcal M\), not on the chosen integral realization \(A\).
> Equivalently, there should exist a canonical finite abelian group
> \[
> K_{\mathrm{arith}}(\mathcal M)
> \]
> such that
> \[
> K_{\mathrm{arith}}(\mathcal M)[n]\cong \operatorname{Bic}_n(A)
> \]
> naturally for all \(n\ge2\).

## Baseline theorem ladder

The program is deliberately staged:

```text
G0  graphs: K(G)[n] ≅ Bic_n(G)
 ↓
R0  fixed TU representation of a regular matroid
 ↓
R1  regular-matroid representation independence
 ↓
A0  arithmetic-matroid realization equivalence
 ↓
A1  bounded counterexample search
 ↓
ABC realization-invariance theorem or minimal counterexample/refinement
```

Thread-derived arguments begin as `working` until they are reproduced by repository proof records or executable evidence.

## Authority planes

- `proof/` — theorem statements, proof records, claim states.
- `kernel/` — future canonical exact algorithms.
- `oracles/` — independent, non-authoritative cross-checks.
- `experiments/` — exploratory searches only.
- `conformance/` — replayable fixtures and receipts.
- `sources/` — literature/source provenance.
- `docs/` — research status, audits, roadmaps.
- `paper/` — publication surface consuming accepted claims.

Projective / Grassmannian geometry is a **derived field-valued shadow** of the integral theory, not acceptance authority for lattice/SNF/torsion claims.

## Current status

Bootstrap only. ABC is open. No graph, regular-matroid, or arithmetic-matroid theorem has yet been promoted to `proved` in this repository.

Start with:
1. `docs/research/status-2026-10-07.md`
2. `docs/research/roadmap.md`
3. `docs/audits/thread-audit-2026-10-07.md`
4. `proof/claims.toml`
