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
num_layers = 100
for y, line in enumerate(map):
    for x, c in enumerate(line):
        # if (y, x) == (35, 15):
        #     print("hej", c)

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
                for layer in range(num_layers):
                    g.add_edge((layer, y-1, x), (layer, y, x))
            if x > 0 and map[y][x-1] == ".":
                for layer in range(num_layers):
                    g.add_edge((layer, y, x-1), (layer, y, x))

label_links = {}
for label, poss in labels.items():
    outsins = [[], []]
    for (y, x) in poss:
        if y in (0, h-2) or x in (0, w-2):
            i = 0
        else:
            i = 1
        if map[y+1][x] == label:
            # vertical
            if y-1 >= 0 and map[y-1][x] == ".":
                outsins[i].append((y-1, x))
            if y+2 < h and map[y+2][x] == ".":
                outsins[i].append((y+2, x))
        elif map[y][x+1] == label:
            if x-1 >= 0 and map[y][x-1] == ".":
                outsins[i].append((y, x-1))
            if x + 2 < w and map[y][x+2] == ".":
                outsins[i].append((y, x+2))
    
    label_links[label] = outsins
    outer, inner = outsins
    for o in outer:
        for i in inner:
            for layer in range(num_layers):
                g.add_edge((layer,) + i, (layer+1,) + o)


start = label_links["AA"][0][0]
end = label_links["ZZ"][0][0]


print(start, end)

# not 4226
print(shortest_path_length(g, (0,) + start, (0,) + end))
