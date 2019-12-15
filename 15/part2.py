import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
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

curpos = np.array([0,0])

g = DiGraph()
g.add_edge((0,0), "untested")
map[(0,0)] = 0

oxygen = None

def explore(op):
    global curpos, oxygen
    trypos = None
    it = 0
    while 1:
        # find untested
        try:
            for p in shortest_path(g, tuple(curpos), "untested")[1:-1]:
                d = getdirnr(np.array(p) - curpos)
                curpos = p[:]
                yield d
                next(op)
        except:
            print("Fully explored")
            write_adjlist(g, "15/found.adjlist")
            with open("15/map.json", "w") as fp:
                fp.write(json.dumps(map))
            break
    
        # test directions
        for d, dir in enumerate(dirs, 1):
            trypos = curpos + dir
            trypos_t = tuple(trypos)
            if trypos_t not in map:
                break
        else:
            g.remove_edge(tuple(curpos), "untested")
            continue
        
        # untested direction trypos/d
        yield d
        i = next(op)
        curpos_t = tuple(curpos)
        if i == 0:
            # hit a wall
            map[trypos_t] = 1
        else:
            map[trypos_t] = 0
            g.add_edge(trypos_t, "untested")
            g.add_edge(curpos_t, trypos_t)
            g.add_edge(trypos_t, curpos_t)
            curpos = trypos[:]
            if i == 2:
                oxygen = trypos_t
                print("found home", trypos_t)
        

m = IterMachine(clean_prg, None)

it1, it2 = itertools.tee(m.iter_output())
m.inv = explore(it1)

tiles = {
    0: " ",
    1: "#",
}
try:
    for it, o in enumerate(it2):
        if it % 50000 == 0:
            draw(sparse_to_array(map), charmap=tiles)
except:
    pass

draw(sparse_to_array(map), charmap=tiles)

g.remove_node("untested")
longest = max(shortest_path_length(g, oxygen).values())
print(longest)

