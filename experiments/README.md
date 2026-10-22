# Experiments

Exploratory bounded searches and projective/Grassmannian diagnostics. Experimental results are never theorem authority.

- [Surjective rank-two census](surjective_rank_two.py): the two explicit
  entry boxes recorded by the Phase 6 computed claim and its existing receipt.
- [Triangular-family bounded validation](triangular_family.py): independent
  potential enumeration against an exact working formula, with 1,988
  modulus cases, 155 same-class primitive parameter pairs, and 6,200
  tower-map checks; the associated [working proof](../proof/triangular-family-tower.md)
  is not an accepted general nonsurjective classification.
- [Realization-dependence/code-hull seeds](realization_dependence.py): six
  explicit matrices, literal code orthogonality, independent bicycle
  comparisons, annihilator profiles, both modulus maps, and available
  Chinese-remainder comparisons. This is a starting packet, not a census.

```sh
python experiments/realization_dependence.py --check
```

Inputs are in the [versioned fixture](../conformance/fixtures/realization-dependence-v1.json);
results and source hashes are in the [receipt](../conformance/receipts/realization-dependence-v1.json).
Use `--write` only after investigating intentional changes. Every listed
matrix/modulus is exhausted without silent caps. The literal dual test
scans every edge vector against every codeword and is intended for small
fixtures. It assumes no nonsurjective Gram-torsion formula.

The [research brief](../docs/research/connections-and-open-questions.md)
and [queue](../docs/research/program.toml) specify how to extend this packet.
