import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine, WaitingForInput
from lib.parse import ReParse
from collections import defaultdict
import itertools
import os
import json
from networkx import DiGraph, shortest_path, shortest_path_length, write_adjlist, read_adjlist, all_pairs_shortest_path_length

clean_prg = [int(x) for x in open("15/input.txt").read().strip().split(",")]

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

g = DiGraph()
g.add_edge(curpos, "untested")
map[curpos] = 0

oxygen = None

def addtup(a, b):
    return tuple(x + y for x, y in zip(a, b))

def explore(op):
    global curpos, oxygen, stop
    trypos = None
    while 1:
        # find untested
        try:
            for p in shortest_path(g, curpos, "untested")[1:-1]:
                d = getdirnr(np.array(p) - curpos)
                curpos = p[:]
                yield d
                next(op)
        except:
            # no unexplored path
            print("Fully explored")
            break
    
        # test directions
        for d, dir in enumerate(dirs, 1):
            trypos = addtup(curpos, dir)
            if trypos not in map:
                break
        else:
            g.remove_edge(curpos, "untested")
            continue
        
        # untested direction trypos/d
        yield d
        i = next(op)
        if i == 0:
            # hit a wall
            map[trypos] = 1
        else:
            map[trypos] = 0
            g.add_edge(trypos, "untested")
            g.add_edge(curpos, trypos)
            g.add_edge(trypos, curpos)
            curpos = trypos[:]
            if i == 2:
                oxygen = trypos
                print("found home", trypos)
        

m = IterMachine(clean_prg, None)

it1, it2 = itertools.tee(m.iter_output())
m.inv = explore(it1)

# run loop
try:
    for it, o in enumerate(it2):
        pass
except WaitingForInput:
    pass

draw(sparse_to_array(map))

g.remove_node("untested")
longest = max(shortest_path_length(g, oxygen).values())
print(longest)

