# Conformance

Versioned fixtures, canonical encodings, receipts, and counterexamples for replayable exact checks.

## Graph modular-bicycle evidence v1

Run from the repository root with Python 3.11 or later. No external packages
are required:

```sh
python conformance/check_claims.py
python -m unittest discover -s conformance -p 'test_*.py' -v
python conformance/replay_graph_modular_bicycle.py --check
git diff --check
```

The original 17 conformance tests cover ten explicit multigraph fixtures at 53
moduli, and all 44 connected labeled simple graphs with at most four
vertices at moduli 2, 3, 4, and 6 (176 further graph/modulus cases).
The fixtures are constructions listed by their complete edge lists, not
an imported census. Loops have zero incidence columns and parallel edges
are separate coordinates.

The current suite has 21 tests. Four additional
[independent review regressions](test_graph_modular_bicycle_audit.py) cover
all mixed edge orientations and vertex permutations on a doubled triangle,
single-vertex and loop-only graphs, large integral lift changes, and a
noncyclic `Z/2 + Z/6` tower through modulus 72. They check 37 further proper
tower pairs and 55 strict three-modulus chains. The original pinned receipt
retains its 53-case and 70-pair scope. See the
[October 9 independent audit](../docs/audits/graph-modular-bicycle-2026-10-09.md).

Two independent routes must agree:

| Candidate implementation | Independent oracle |
| --- | --- |
| Incidence-product Laplacian | Direct multiplicity Laplacian |
| Normalized-potential enumeration | Chord-valued cycles completed by tree leaf elimination |
| Rational Gauss-Jordan inverse | Exact Bareiss determinants and Cramer's rule |
| Explicit forward and inverse maps | Independently enumerated critical-group quotient |
| Bicycle element orders | Smith factors from gcds of all minors |

Both use integers and exact fractions. The oracle imports no kernel code;
it does not call the proposed theorem map to derive expected counts or
classes. A third literal edge/potential enumeration checks its tree method
on fixtures with at most four edges. Bareiss determinants are checked
against permutation expansion, and Smith factors against planted
unimodular transforms, including singular matrices.

Tests check both inverse identities, sampled integral representative
changes for every fixture bicycle, every computational root, linearity,
signed edge permutations, vertex relabeling, and both modulus maps and
their compositions. Negative tests reject non-cycles, non-cuts, incorrect
potentials, non-torsion divisors, invalid domains, and non-dividing tower
maps. They demonstrate why arbitrary edge lifts, unscaled inflation, and
assuming surjective reduction are invalid, and why mod-2 ranks miss
mod-4 exponents.

The checked-in JSON receipt records fixture results, element-order
profiles, bijection checks, tower checks, bicycle-set hashes, and hashes
of its source files and proof record. Replay compares canonical bytes and
fails on drift. After an intentional source change, inspect the cause and
regenerate with:

```sh
python conformance/replay_graph_modular_bicycle.py --write
```

Enumeration is exhaustive within the stated finite fixtures. There are no
silent caps or timeouts. Potential enumeration is exponential in V-1;
chord enumeration is exponential in E-V+1; the all-minors Smith oracle is
also for small matrices. These checks support the separate integral proof
and do not establish any arithmetic-matroid realization-invariance claim.
