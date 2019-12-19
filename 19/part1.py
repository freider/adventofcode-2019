import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine, WaitingForInput
from lib.parse import ReParse
from collections import defaultdict, deque
import itertools
import os
import json
from networkx import Graph, DiGraph, shortest_path, shortest_path_length, write_adjlist, read_adjlist, all_pairs_shortest_path_length

clean_prg = [int(x) for x in open("19/input.txt").read().strip().split(",")]

map = {}


inputs = []
coords = []
for x in range(50):
    for y in range(50):
        inputs += [x, y]
        coords.append((y, x))

def getc(coord):
    m = Machine(clean_prg.copy(), deque([coord[1], coord[0]]))
    for o in m.iter_output():
        return o

c = 0
for coord in coords:
    o = getc(coord)
    if o > 0:
        c+=1
    map[coord] = o

print(c)
ar = sparse_to_array(map)
draw(ar)
