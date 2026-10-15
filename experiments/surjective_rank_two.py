"""Exhaust two finite rank-two boxes; do not infer a theorem from the census."""

import argparse
from collections import defaultdict
from itertools import combinations, product
import hashlib
import json
from math import gcd, prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel.arithmetic_matroid import IntegralRealization, smith_certificate
from kernel.surjective_bicycle import SurjectiveRepresentation
from kernel.surjective_equivalence import find_surjective_equivalence
from oracles.arithmetic_matroid import arithmetic_signature, lattice_bicycles, rectangular_factors
from oracles.regular_snf import determinant, literal_bicycles
from oracles.surjective_equivalence import brute_surjective_equivalence

RECEIPT = ROOT / 'conformance/receipts/phase6-rank-two-v1.json'
MODULI = (2, 3, 4, 5, 6, 8, 9, 10)
DIRECT_MODULI = (2, 3, 4, 6)
SOURCES = (
    'experiments/surjective_rank_two.py', 'conformance/test_phase6_boundaries.py',
    'proof/surjective-boundary-cases.md', 'proof/surjective-realization-invariance.md',
    'kernel/arithmetic_matroid.py', 'kernel/surjective_bicycle.py',
    'kernel/surjective_equivalence.py', 'kernel/regular_bicycle.py', 'kernel/graph_bicycle.py',
    'oracles/arithmetic_matroid.py', 'oracles/surjective_equivalence.py',
    'oracles/regular_snf.py', 'oracles/graph_snf.py',
)


def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2) + '\n'


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def scan(width, bound):
    buckets = defaultdict(list)
    excluded = defaultdict(int)
    for v in product(range(-bound, bound + 1), repeat=2*width):
        rows = (v[:width], v[width:])
        independent = rectangular_factors(rows)
        require(smith_certificate(rows).factors == independent, 'domain Smith disagreement')
        if len(independent) != 2:
            excluded['rank_deficient'] += 1
        elif independent != (1, 1):
            excluded['nonsurjective_full_rank'] += 1
        else:
            buckets[arithmetic_signature(rows)].append(rows)
    print(f'{width} columns, bound {bound}: {sum(map(len, buckets.values()))} surjections, '
          f'{len(buckets)} buckets; checking witnesses and modular sets', flush=True)
    witnesses, profiles = [], []
    no_unit_basis = 0
    for signature, group in sorted(buckets.items()):
        a = SurjectiveRepresentation(group[0])
        smith = rectangular_factors(a.gram)
        require(smith_certificate(a.gram).factors == smith, 'representative Gram SNF disagreement')
        edges = {}
        for n in MODULI:
            b = lattice_bicycles(a.rows, n)
            require(b == literal_bicycles(a.rows, n) == set(a.bicycles(n)),
                    'independent representative edge sets disagree')
            factors = tuple(gcd(n, d) for d in smith)
            require(len(b) == prod(factors), 'Smith group size disagrees with edge oracle')
            # Verify exponent information, not just total order.
            for d in (k for k in range(1, n + 1) if n % k == 0):
                require(sum(all(d*x % n == 0 for x in v) for v in b) ==
                        prod(gcd(d, f) for f in factors), 'annihilator profile disagrees')
            profiles.append({'representative': a.rows, 'modulus': n,
                             'cyclic_factors_including_units': factors,
                             'edge_set_sha256': digest(sorted(b))})
            edges[n] = b
        for rows in group:
            ap = SurjectiveRepresentation(rows)
            require(ap.realization.signature == signature, 'complete arithmetic data disagree')
            w = find_surjective_equivalence(a, ap)
            require(brute_surjective_equivalence(a.rows, rows) is not None,
                    'independent sign search fails')
            require(smith_certificate(ap.gram).factors == rectangular_factors(ap.gram) == smith,
                    'same arithmetic data, different Gram groups')
            no_unit_basis += all(abs(determinant([[row[j] for j in cc] for row in rows])) != 1
                                 for cc in combinations(range(width), 2))
            for n in DIRECT_MODULI:
                actual = set(ap.bicycles(n))
                transported = {w.transport_bicycle(b, n) for b in edges[n]}
                require(actual == transported, 'same arithmetic data, different bicycle sets under witness')
            witnesses.append({'matrix': rows, 'signature': signature,
                              'row_change': w.row_change, 'signs': w.signs})
    size = sum(map(len, buckets.values()))
    return {
        'rows': 2, 'columns': width, 'entry_interval': [-bound, bound],
        'all_matrices': (2*bound + 1)**(2*width), 'excluded': dict(excluded),
        'surjective_matrices': size, 'arithmetic_buckets': len(buckets),
        'without_unit_maximal_minor': no_unit_basis,
        'all_matrix_witness_comparisons_including_representatives': size,
        'nonidentity_comparisons_to_bucket_representative': size-len(buckets),
        'all_matrix_direct_potential_and_transport_moduli': DIRECT_MODULI,
        'all_matrix_direct_modulus_cases': size*len(DIRECT_MODULI),
        'all_matrix_gram_snf_profile_moduli': MODULI,
        'independent_edge_oracle_scope': 'one lexicographically first matrix per complete arithmetic bucket',
        'independent_edge_oracle_moduli': MODULI,
        'independent_edge_oracle_cases': len(profiles),
        'unequal_gram_groups': 0, 'failed_witnesses': 0, 'bicycle_discrepancies': 0,
        'witness_records_sha256': digest(witnesses), 'representative_profiles': profiles,
    }


def controls():
    a, ap = ((1, 1), (0, 5)), ((1, 2), (0, 5))
    require(arithmetic_signature(a) == arithmetic_signature(ap), 'lost equal-data negative control')
    orders = []
    for n in (5, 10):
        sizes = [len(lattice_bicycles(rows, n)) for rows in (a, ap)]
        require(sizes == [1, 5], 'lost nonsurjective discrepancy')
        orders.append({'modulus': n, 'orders': sizes})
    for rows in (a, ap):
        try:
            SurjectiveRepresentation(rows)
        except ValueError:
            pass
        else:
            raise RuntimeError('admitted index-five control')
    # Same rank, singleton data and full index; different labeled pair data.
    c, cp = ((1, 0, 1), (0, 1, 1)), ((1, 0, 1), (0, 1, 2))
    sig, sigp = arithmetic_signature(c), arithmetic_signature(cp)
    require(all(sig[k] == sigp[k] for k in (0, 1, 2, 4, 7)) and sig != sigp,
            'lower-subset negative control is ineffective')
    require(brute_surjective_equivalence(c, cp) is None, 'oracle accepted unequal data')
    try:
        find_surjective_equivalence(SurjectiveRepresentation(c), SurjectiveRepresentation(cp))
    except ValueError:
        pass
    else:
        raise RuntimeError('candidate accepted unequal data')
    # Outside both entry boxes: surjective but no single maximal minor is a unit.
    p = ((2, 0, 1), (0, 3, 1))
    require(rectangular_factors(p) == (1, 1), 'positive control not surjective')
    require(rectangular_factors(SurjectiveRepresentation(p).gram) == (1, 49), 'lost C49 control')
    positive = []
    for n in (7, 14, 49):
        b = lattice_bicycles(p, n)
        require(b == set(SurjectiveRepresentation(p).bicycles(n)), 'positive edge disagreement')
        require(len(b) == gcd(n, 49), 'lost nontrivial positive control')
        positive.append({'modulus': n, 'order': len(b)})
    return {'nonsurjective_equal_data': orders, 'unequal_lower_subset_data_rejected': True,
            'no_unit_basis_positive': positive}


def evidence():
    return {
        'schema': 1, 'claim': 'ABC-PHASE6-RANK-TWO-CENSUS', 'status': 'computed',
        'scope': 'exhaustive finite boxes; general theorem authority is the separate integral proof',
        'boxes': [scan(3, 2), scan(4, 1)], 'controls': controls(),
        'sources_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
        'original_claims': 'ABC-MAIN and ABC-REALIZATION-INVARIANCE remain retracted',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = canonical(evidence())
    if args.write:
        RECEIPT.write_text(result)
    else:
        require(RECEIPT.read_text() == result, 'receipt drift; investigate before regeneration')
    print('PASS: both complete rank-two boxes and all controls', flush=True)


if __name__ == '__main__':
    main()
