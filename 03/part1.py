import numpy as np

origin = np.zeros(2, dtype=int)

def parse(raw):
    current = origin
    segments = []
    for instr in raw:
        i = instr[0]
        move = {
            'R': np.array([1, 0]),
            'L': np.array([-1, 0]),
            'D': np.array([0, -1]),
            'U': np.array([0, 1])
        }[i] * int(instr[1:])
        new = current + move
        segments.append((current, new))
        current = new
    return segments


wires = []
for line in open("03/input.txt"):
    raw = line.split(",")
    wire = parse(raw)
    wires.append(wire)

def is_horizontal(wire):
    return (wire[1] - wire[0])[1] == 0

def intersection(s1, s2):
    h1 = is_horizontal(s1)
    h2 = is_horizontal(s2)
    if h1 and h2:
        return None
    elif not h1 and not h2:
        return None
    elif h1:
        y = s1[0][1]
        x = s2[0][0]
        ybounds = sorted([s2[0][1], s2[1][1]])
        xbounds = sorted([s1[0][0], s1[1][0]])
        if ybounds[0] <= y <= ybounds[1] and  xbounds[0] <= x <= xbounds[1]:
            return np.array([x, y])
    elif h2:
        return intersection(s2, s1)


mindist = 1e10
for w in wires[0]:
    for v in wires[1]:
        cross = intersection(w, v)
        if cross is not None and (cross == origin).sum() != 2:
            mindist = min(abs(cross[0]) + abs(cross[1]), mindist)

print(mindist)
