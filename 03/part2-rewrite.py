import numpy as np

origin = np.zeros(2, dtype=int)

def parse(raw):
    current = origin
    points = {}
    d = 0
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
            d += 1
            points[tuple(current)] = min(points.get(tuple(current), 1e10), d)

    return points


wires = []
for line in open("03/input.txt"):
    raw = line.split(",")
    wire = parse(raw)
    wires.append(wire)


def intersection(w1, w2):
    ps = set(w1.keys()) & set(w2.keys())
    return min(w1[p] + w2[p] for p in ps)

print(intersection(*wires))
