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

q = deque()

def explore(op):
    x, y = (0, 0)
    for inp in op:
        if inp < 256 and inp != 10:
            map[(y, x)] = inp
        
        if inp == 10:
            x = 0
            y += 1
        else:
            x += 1

    return
    yield


m = Machine(clean_prg.copy(), q)

for inp in explore(m.iter_output()):
    q.append(inp)


for k, v in map.items():
    if v == ord('^'):
        pos = k

dir = (-1, 0)

def addpos(p1, p2):
    return tuple(a + b for a, b in zip(p1, p2))


visited = set()
scaffoldsize = sum(1 for v in map.values() if v == ord('#'))

def visit_all():
    global dir, pos
    
    while len(visited) < scaffoldsize:
        left = (-dir[1], dir[0])
        right = (dir[1], -dir[0])
        for d, newdir in enumerate((left, right)):
            j = 0
            while 1:
                tpos = addpos(pos, newdir)
                if map.get(tpos) == ord('#'):
                    # we can walk in direction
                    pos = tpos
                    visited.add(pos)
                    j+=1
                else:
                    break
            if j:
                dir = newdir
                yield ['L', 'R'][d] + "," + str(j)
                break

ar = sparse_to_array(map)

charmap = {}
for i in range(256):
    charmap[i] = chr(i)
draw(ar, charmap)

for instr in visit_all():
    print(instr, len(visited), scaffoldsize)
