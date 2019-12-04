import numpy as np

origin = np.zeros(2, dtype=int)

def parse(raw):
    current = origin
    points = []
    for instr in raw:
        i = instr[0]
        move = {
            'R': np.array([1, 0]),
            'L': np.array([-1, 0]),
            'D': np.array([0, -1]),
            'U': np.array([0, 1])
        }[i]
        for j in range(int(instr[1:])):
            current = current + move
            points.append(tuple(current))

    return points


wires = []
for line in open("03/input.txt"):
    raw = line.split(",")
    wire = parse(raw)
    wires.append(wire)

def dist(p1, p2):
    return np.abs(p2 - p1).sum()


def intersection(w1, w2):
    ps = set(w1) & set(w2)
    return min(dist(np.array(p), origin) for p in ps)


print(intersection(*wires))
