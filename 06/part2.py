orbits = {}
parents = set()

link = {}
for line in open("06/input.txt"):
    a, b = line.strip().split(")")
    orbits.setdefault(b, set()).add(a)
    parents.add(b)
    link.setdefault(b, set()).add(a)
    link.setdefault(a, set()).add(b)


start = list(orbits["YOU"])[0]
end = list(orbits["SAN"])[0]


q = [(start, 0)]
visited = set()

while q:
    n, d = q.pop(0)
    if n == end:
        print(d)
        break

    for c in link[n]:
        if c not in visited:
            q.append((c, d+1))

    visited.add(n)
