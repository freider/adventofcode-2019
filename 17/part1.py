import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine, WaitingForInput
from lib.parse import ReParse
from collections import defaultdict
import itertools
import os
import json
from networkx import Graph, DiGraph, shortest_path, shortest_path_length, write_adjlist, read_adjlist, all_pairs_shortest_path_length

clean_prg = [int(x) for x in open("17/input.txt").read().strip().split(",")]

map = {}

dirs = np.array(list([
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1]
]))

def getdirnr(dir):
    for d, foo in enumerate(dirs, 1):
        if (foo == dir).all():
            return d

curpos = (0, 0)

g = Graph()

def explore(op):
    x, y = (0, 0)
    for inp in op:
        if inp == 35:
            t = 1
            map[(y, x)] = t
            if y > 0 and map.get(y-1, x) == t:
                g.add_edge((y-1, x), (y, x))
            if x > 0 and map.get(y, x-1) == t:
                g.add_edge((y-1, x), (y, x))

        elif inp == 46:
            t = 0
        
        if inp == 10:
            x = 0
            y += 1
        else:
            x += 1
    yield


m = IterMachine(clean_prg, None)

for a in explore(m.iter_output()):
    pass

# it1, it2 = itertools.tee(m.iter_output())
# m.inv = explore(it1)

# # run loop
# try:
#     for it, o in enumerate(it2):
#         pass
# except WaitingForInput:
#     pass


# ar = sparse_to_array(map)

# for y, row in iterate(arr):
#     for x, c in 

s = 0
for x, y in map.keys():
    if map.get((x-1, y)) and map.get((x+1, y)) and map.get((x, y-1)) and map.get((x, y+1)):
        s += x * y
        
print(s)
