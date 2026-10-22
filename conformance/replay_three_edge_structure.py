"""Source-pinned exact three-edge full-tower structure receipt (v3).

The finite receipt checks two independent enumerations and a separate
Smith order calculation. It does not certify the general proof or Lean.
"""
import argparse
import json
from hashlib import sha1
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from experiments.three_edge_structure import (
    audit, literal_potentials, presented_edges, gram_order, group_exponent,
)

RECEIPT=ROOT / "conformance/receipts/three-edge-structure-v1.json"
SOURCES=(
    "experiments/three_edge_structure.py",
    "conformance/test_three_edge_structure.py",
    "conformance/replay_three_edge_structure.py",
    "proof/three-edge-full-tower-presentation.md",
)

def git_blob(path):
    data=(ROOT/path).read_bytes()
    return sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def canonical(x):
    return json.dumps(x,sort_keys=True,indent=2)+"\n"

def report():
    checks=audit()
    samples=[]
    for a,b,n in ((1,3,3),(1,3,9),(1,7,7),(2,7,7),
                  (1,7,14),(2,7,14),(1,7,49),(2,7,49)):
        hull=literal_potentials(a,b,n)
        assert hull == presented_edges(a,b,n)
        assert len(hull)==gram_order(a,b,n)
        samples.append({"a":a,"b":b,"n":n,"order":len(hull),
                        "exponent":group_exponent(hull,n),
                        "vectors":[list(x) for x in sorted(hull)]})
    assert samples[1]["order"]==9 and samples[1]["exponent"]==3
    return {"schema":1,"authority":"non_authoritative_experiment",
            "questions":["ABC-RD-01","ABC-MODULE-01"],
            "claim_promotions":[],
            "scope":"256 bounded 3-edge triples: b=3..13, a primitive 0..b-1, n in [2,3,5,7,9,14,21,27]",
            "three_route_exact_comparisons":checks,
            "noncyclic_prime_power_control":{"a":1,"b":3,"n":9,"group":"(Z/3)^2"},
            "samples":samples,
            "source_git_blob_sha1":{p:git_blob(p) for p in SOURCES}}

def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check",action="store_true")
    mode.add_argument("--write",action="store_true")
    args=parser.parse_args()
    serial=canonical(report())
    if args.write:
        RECEIPT.write_text(serial)
    elif RECEIPT.read_text()!=serial:
        raise RuntimeError("three-edge structure v1 receipt drift")
    print("PASS: three-edge full-module / Smith / noncyclic evidence")

if __name__=="__main__":
    main()
