inp = []
for line in open("input.txt"):
    n = int(line.strip())
    inp.append(n)

tot = 0
while inp:
    inp = [x for x in (p // 3 - 2 for p in inp) if x > 0]
    tot += sum(inp)

print(tot)
