# Oracles

Independent non-authoritative implementations for cross-checking canonical kernels.

`graph_snf.py` contains an exact small-matrix Smith-factor oracle based on
determinantal divisors, a separate tree-cycle bicycle enumerator, and
Cramer-based critical-group class coordinates. It imports no kernel code.
It is evidence for finite fixtures, not theorem authority.

`regular_snf.py` supplies a separate fixed-TU oracle. It uses the Bareiss
and all-minors Smith primitives, takes a different unit column basis from
the candidate, completes cycles with Cramer's rule, and tests their cut
condition. Quotient classes are enumerated from standard generators
independently of the theorem map. Literal potential enumeration handles
labeled non-TU controls. This module also imports no kernel code.

`regular_equivalence.py` checks the rational rank of every column subset
and enumerates all column signs to find an integral equivalence using
Bareiss/Cramer calculations and a different unit basis. It imports no
kernel code and does not reuse the candidate support-graph sign solver.
Its ordinary-matroid rank signature is not an arithmetic-matroid encoding.

`arithmetic_matroid.py` independently computes rectangular Smith factors
and all-subset multiplicities by Bareiss minor gcds. For modular bicycles,
it enumerates edges and tests cut membership by comparing the full-lattice
indices of `[A^T | n I]` and its augmentation by the edge vector. This
works over composite rings and imports no kernel code or candidate Smith
reduction. The inherited literal potential routine supplies a third check.

`surjective_equivalence.py` checks surjectivity by independent rectangular
determinantal divisors and compares complete arithmetic signatures.
It searches all column signs using the last nonzero rational basis and
Bareiss/Cramer inverse coordinates. It requires no unit basis and imports
no kernel code or candidate support-sign solver. The arithmetic lattice
oracle above checks its modular edge transports independently, including
prime powers and mixed composite moduli.
