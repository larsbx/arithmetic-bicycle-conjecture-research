"""Replay bounded conformance and verify exact source pins; no claim authority."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from conformance.test_surjective_three_edge import SurjectiveThreeEdgeTests
RECEIPT=ROOT/'conformance/receipts/surjective-three-edge-v1.json'
SOURCES=('proof/surjective-three-edge-cyclic.md',
         'conformance/test_surjective_three_edge.py',
         'conformance/replay_surjective_three_edge.py',
         'lean/ABC/SurjectiveThreeEdge.lean',
         'kernel/arithmetic_matroid.py','kernel/surjective_bicycle.py',
         'kernel/regular_bicycle.py','kernel/graph_bicycle.py',
         'oracles/arithmetic_matroid.py','oracles/regular_snf.py','oracles/graph_snf.py')
def derive():
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(SurjectiveThreeEdgeTests)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError('restricted cyclic conformance failed')
    return {'authority':'non_authoritative_experiment','claim_promotions':[],
            'box_entries':[-2,2],'surjective_matrices':7176,
            'ternary_signature_representatives':10,'extra_no_unit_minor_realizations':2,
            'tests_run':result.testsRun,'lean_status':'unverified_partial_formalization',
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}}
def main():
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--write',action='store_true')
    g.add_argument('--check',action='store_true')
    args=p.parse_args()
    data=json.dumps(derive(),sort_keys=True,indent=2)+'\n'
    if args.write:
        RECEIPT.write_text(data)
    elif RECEIPT.read_text()!=data:
        raise RuntimeError('restricted cyclic receipt drift')
    print('PASS: surjective three-edge source-pinned conformance')
if __name__=='__main__':
    main()
