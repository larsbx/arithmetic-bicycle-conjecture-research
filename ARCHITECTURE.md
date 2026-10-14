# Architecture

Status: proved graph/TU theory, exact arithmetic data, and a refuted principal conjecture within the candidate research program.

The repository follows an authority-first research layout. Conjecture, proof, computation, exploratory experiments, and publication surfaces are deliberately separated.

## Domain

Primary domain: integral cut/cycle lattices, modular bicycle modules, critical groups, regular matroids, and representable arithmetic matroids.

Original principal conjecture: realization invariance of the compatible modular bicycle tower, now refuted by an explicit essential torsion-free arithmetic pair. Corrected hypotheses are the next research target.

## Authority surfaces

### Proof plane: `proof/`

Claim states:
- `open`: principal unresolved statement;
- `working`: thread argument or draft proof not yet independently reproduced here;
- `computed`: reproduced by checked-in exact code/data/receipts;
- `proved`: repository proof record independent of exploratory scripts;
- `retracted`: retained for provenance but no longer asserted.

### Kernel plane: `kernel/`

Future canonical exact machinery for:
1. modular cut/cycle/bicycle modules over \(\mathbb Z/n\);
2. Smith normal form and finite abelian group comparison;
3. regular-matroid TU fixtures;
4. arithmetic-matroid realization comparison.

At bootstrap, no kernel has acceptance authority.
Candidate exact maps live in `kernel/graph_bicycle.py` and
`kernel/regular_bicycle.py`; Python acceptance authority remains false.
The separate graph and fixed-TU integral proof records are theorem
authority. Their independent small-fixture evidence lives in `oracles/`
and `conformance/`.

`kernel/regular_equivalence.py` adds verified witnesses for a prescribed
TU matroid label comparison. The separate integral proof transports the
whole modular tower and records independence of its isomorphism class.
Candidate witness choice does not define a unique canonical comparison.

The universal finite-group torsion-model strengthening is retracted by
`proof/arithmetic-torsion-model-obstruction.md`. It is recorded separately
from the original arithmetic realization-invariance statement, now
refuted separately by `proof/arithmetic-realization-counterexample.md`.
The exact arithmetic signature proof governs the new all-subset
comparison gate; equality of arithmetic data does not imply bicycle
invariance.

### Oracles plane: `oracles/`

Independent cross-check implementations. Never theorem authority.

### Experiments plane: `experiments/`

Bounded searches, counterexample hunting, projective/Grassmannian diagnostics. Experimental output cannot promote proof claims by itself.

### Conformance plane: `conformance/`

Versioned fixtures, canonical encodings, receipts, counterexamples, and replay tests.

### Sources plane: `sources/`

Literature provenance and imported theorem records.

### Paper plane: `paper/`

Consumes accepted claims only. It does not promote them.

## Integral truth layer vs projective shadow

```text
integral lattices / SNF / finite abelian groups
        ↓ reduce mod p
finite-field cut/cycle spaces
        ↓
Grassmannian / determinantal incidence shadow
```

Projective geometry is explanatory and diagnostic. Integral claims remain governed by lattice/exact-sequence/SNF evidence.

## Scope boundaries

- Do not reassert the withdrawn general ABC; its explicit refutation has its own proof record.
- Do not mark the graph modular-bicycle theorem proved until the arbitrary-\(n\) module isomorphism is written and audited.
- Keep the proved fixed-TU theorem separate from regular-matroid representation independence.
- Keep the regular TU representation theorem separate from arbitrary integer representations and arithmetic-matroid equality.
- Do not infer arithmetic-matroid realization invariance from regular/TU cases.
- Do not treat projective geometry as a substitute for integral multiplicity or torsion data.
