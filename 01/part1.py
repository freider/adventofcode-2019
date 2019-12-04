inp = []
for line in open("01/input.txt"):
    n = int(line.strip())
    inp.append(n)


print(sum([p // 3 - 2 for p in inp]))
