from networkx import DiGraph, topological_sort


def tod(p):
    num, name = p
    return (name, int(num))

def read():
    for line in open("14/input.txt"):
        from_in, to_in = [p.strip() for p in line.split("=>")]
        sep = [s.strip() for s in from_in.split(", ")]
        ing_list = [tod(s.split()) for s in sep]
        yield ing_list, tod(to_in.split())

recipes = {  #e.g. {"AC": (5, ((A, 2), (C, 1))}
    prod[0]: (prod[1], ing)
    for ing, prod in read()
}

g = DiGraph()

for t, (n, f) in recipes.items():
    for i, m in f:
        g.add_edge(t, i)

from collections import defaultdict
need = defaultdict(int)
need["FUEL"] = 1
for f in topological_sort(g):
    if f == "ORE":
        assert len(need) == 1 and "ORE" in need
        break
    a = need[f]
    del need[f]
    p, ing = recipes[f]
    num_rep = (p + a - 1) // p
    for k, v in ing:
        need[k] += num_rep * v

print(need["ORE"])
