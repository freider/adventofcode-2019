import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse
from networkx import Graph, DiGraph, shortest_path_length

map = [[c for c in line.strip('\n')] for line in open("20/input.txt")]
h = len(map)
w = len(map[0])
g = Graph()

labels = {}

for y, line in enumerate(map):
    for x, c in enumerate(line):
        if len(c) == 1 and "A" <=c<= "Z":
            if x < w-1 and "A"<=map[y][x+1]<="Z":
                label = c + map[y][x+1]
                map[y][x+1] = map[y][x] = label
            elif y < h-1 and "A"<=map[y+1][x]<="Z":
                label = c + map[y+1][x]
                map[y+1][x] = map[y][x] = label
            labels.setdefault(label, []).append((y, x))
        if c == ".":
            if y > 0 and map[y-1][x] == ".":
                g.add_edge((y-1, x), (y, x))
            if x > 0 and map[y][x-1] == ".":
                g.add_edge((y, x-1), (y, x))


for l, poss in labels.items():
    ps = poss.copy()
    #print(poss)
    for (y, x) in poss:
        if map[y+1][x] == l:
            # vertical
            ps.append((y-1, x))
            ps.append((y+2, x))
        elif map[y][x+1] == l:
            ps.append((y, x-1))
            ps.append((y, x+2))
    print(poss)
    print(f"linking {l} {ps}")
    for p in ps:
        for p2 in ps:
            g.add_edge(p, p2)

print(labels)
for l in map:
    print(''.join(l))

start = labels["AA"][0]
end = labels["ZZ"][0]

#start = (start[0] + 2, start[1])
#end = (end[0]-1, end[1])

start = (start[0] - 1, start[1])
end = (end[0]+2, end[1])


print(shortest_path_length(g, start, end))
