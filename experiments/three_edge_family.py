"""Bounded nonparallel three-edge nonsurjective ABC family.

A(a,b)=[[1,a,a+1],[0,b,b]], b>=2, gcd(a,b)=gcd(a+1,b)=1.
Literal potential enumeration and a separate edge-congruence test; no
surjective Gram-torsion shortcut. This is finite exploratory evidence.
"""
from itertools import combinations, product
from math import gcd

def matrix(a, b):
    if type(a) is not int or type(b) is not int or b < 2 or gcd(a,b) != 1 or gcd(a+1,b) != 1:
        raise ValueError("primitive a,a+1 and integer b>=2 required")
    return ((1,a,a+1),(0,b,b))

def signature(a, b):
    rows=matrix(a,b)
    ans=[]
    for mask in range(8):
        js=[j for j in range(3) if mask & (1 << j)]
        g=0
        for j in js:
            g=gcd(g,rows[0][j],rows[1][j])
        d=0
        for i,j in combinations(js,2):
            d=gcd(d,rows[0][i]*rows[1][j]-rows[1][i]*rows[0][j])
        ans.append([2,d] if d else [1,g] if g else [0,1])
    return ans

def bicycles(a, b, n):
    if type(n) is not int or n < 2:
        raise ValueError("integer n>=2 required")
    matrix(a,b)
    out=set()
    for s,t in product(range(n),repeat=2):
        z=(s,(a*s+b*t)%n,((a+1)*s+b*t)%n)
        if (z[0]+a*z[1]+(a+1)*z[2])%n==0 and b*(z[1]+z[2])%n==0:
            out.add(z)
    return out

def independent_edges(a,b,n):
    """Enumerate all edge vectors; solve cut congruences using gcd."""
    matrix(a,b)
    g=gcd(b,n)
    out=set()
    for v in product(range(n),repeat=3):
        if (v[0]+a*v[1]+(a+1)*v[2])%n or b*(v[1]+v[2])%n:
            continue
        r1=(v[1]-a*v[0])%n
        r2=(v[2]-(a+1)*v[0])%n
        if r1==r2 and r1%g==0:
            out.add(v)
    return out

def transition(group,n,m,mode):
    assert m%n==0
    if mode=="reduce":
        return {tuple(v%n for v in x) for x in group}
    assert mode=="inflate"
    return {tuple((m//n)*v%m for v in x) for x in group}

def evidence():
    cases=[]
    for a,b in ((1,7),(2,7)):
        record={"a":a,"b":b,"matrix":matrix(a,b),"signature":signature(a,b),"groups":[],"tower_maps":[]}
        groups={}
        for n in (2,7,14,49):
            group=bicycles(a,b,n)
            if n<=14:
                assert group==independent_edges(a,b,n)
            if n==b:
                assert len(group)==gcd(b,2*(1+a+a*a))
            groups[n]=group
            record["groups"].append({"n":n,"order":len(group),"elements":[list(x) for x in sorted(group)]})
        for n,m in ((2,14),(7,14),(7,49)):
            red=transition(groups[m],n,m,"reduce")
            inf=transition(groups[n],n,m,"inflate")
            assert red<=groups[n] and inf<=groups[m]
            record["tower_maps"].append({"small":n,"large":m,"reduction_image":[list(x) for x in sorted(red)],"inflation_image":[list(x) for x in sorted(inf)]})
        cases.append(record)
    assert cases[0]["signature"]==cases[1]["signature"]
    assert set(map(tuple,cases[0]["signature"]))=={(0,1),(1,1),(2,7)}
    assert [[g["order"] for g in x["groups"]] for x in cases]==[[1,1,1,7],[1,7,7,7]]
    census=[]
    for b in range(3,14):
        admissible=[a for a in range(b) if gcd(a,b)==gcd(a+1,b)==1]
        if len(admissible)<2:
            continue
        profiles={a:len(bicycles(a,b,b)) for a in admissible}
        for a in admissible:
            assert profiles[a]==gcd(b,2*(1+a+a*a))
        census.append({"b":b,"admissible":admissible,"order_at_b":[[a,profiles[a]] for a in admissible],"distinct_orders":sorted(set(profiles.values()))})
    assert any(x["b"]==7 and x["distinct_orders"]==[1,7] for x in census)
    return {"schema":1,"authority":"non_authoritative_experiment",
            "scope":"labeled nonparallel rank-two three-edge family; fixed b sweep 3..13",
            "claim_promotions":[],"results":cases,"bounded_census":census}

if __name__=="__main__":
    import json
    print(json.dumps(evidence(),sort_keys=True,indent=2))
