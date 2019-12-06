orbits = {}
parents = set()
for line in open("06/input.txt"):
    a, b = line.strip().split(")")
    orbits.setdefault(b, set()).add(a)
    parents.add(b)


mem = {}

def rec(a):
    if a in mem:
        return mem[a]
    elif a not in orbits:
        return 0
    else:
        ret = len(orbits[a]) + sum(rec(o) for o in orbits[a])
        mem[a] = ret
        return ret

for a in parents:
    r = rec(a)
    # print(f"{a}: {r}")

print(sum(mem.values()))
