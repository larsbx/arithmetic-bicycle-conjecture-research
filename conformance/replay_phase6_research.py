"""Source-pinned, non-authoritative Phase 6 evidence for ABC-RD-01.

Checks inherited triangular-family bounded evidence and a genuinely
nonparallel three-edge rank-two negative control. The checked-in receipt
is canonical and pins git blob SHA-1 of the exact sources, proofs and
Lean proof-bank modules. It never promotes research claims.
"""
import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from experiments.triangular_family import run_checks
from experiments.three_edge_family import evidence

RECEIPT = ROOT / "conformance/receipts/phase6-realization-dependence-v2.json"
SOURCES = (
    "experiments/triangular_family.py",
    "experiments/three_edge_family.py",
    "proof/triangular-family-tower.md",
    "proof/nonparallel-three-edge.md",
    "lean/lean-toolchain",
    "lean/lakefile.toml",
    "lean/ABC.lean",
    "lean/ABC/Triangular.lean",
    "lean/ABC/ThreeEdge.lean",
    "conformance/replay_phase6_research.py",
    "conformance/test_phase6_research.py",
)

def git_blob(path):
    data=(ROOT/path).read_bytes()
    return sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

def canonical(report):
    return json.dumps(report,sort_keys=True,indent=2)+"\n"

def derive():
    baseline=run_checks()
    beyond=evidence()
    controls=[]
    for record in beyond["results"]:
        controls.append({
            "a":record["a"],"b":record["b"],
            "signature":record["signature"],
            "group_orders":[[g["n"],g["order"]] for g in record["groups"]],
            "group_vectors_sha256":[{
                "n":g["n"],
                "digest":sha256(canonical(g["elements"]).encode()).hexdigest(),
            } for g in record["groups"]],
            "map_image_orders":[[x["small"],x["large"],
                                 len(x["reduction_image"]),
                                 len(x["inflation_image"])]
                                for x in record["tower_maps"]],
        })
    assert controls[0]["signature"]==controls[1]["signature"]
    assert controls[0]["group_orders"]==[[2,1],[7,1],[14,1],[49,7]]
    assert controls[1]["group_orders"]==[[2,1],[7,7],[14,7],[49,7]]
    assert baseline["literal_formula_cases"]==1988
    assert baseline["equal_class_parameter_pairs"]==155
    assert baseline["tower_map_instances"]==6200
    return {
        "schema":2,
        "authority":"non_authoritative_experiment",
        "questions":["ABC-RD-01","ABC-MODULE-01"],
        "claim_promotions":[],
        "scope":"triangular bounded checks plus 2x3 nonparallel b=7 controls, b=3..13 sweep",
        "triangular_baseline":baseline,
        "three_edge_controls":controls,
        "nonparallel_bounded_census":beyond["bounded_census"],
        "source_git_blob_sha1":{path:git_blob(path) for path in SOURCES},
    }

def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check",action="store_true")
    mode.add_argument("--write",action="store_true")
    args=parser.parse_args()
    serialized=canonical(derive())
    if args.write:
        RECEIPT.write_text(serialized)
    elif RECEIPT.read_text()!=serialized:
        raise RuntimeError("Phase 6 receipt drift: investigate source/claim scope")
    print("PASS: source-pinned Phase 6 triangular and nonparallel evidence")

if __name__=="__main__":
    main()
