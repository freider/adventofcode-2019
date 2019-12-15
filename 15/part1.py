import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse
from collections import defaultdict
import itertools
from networkx import DiGraph, shortest_path, shortest_path_length, write_adjlist

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
#print(g.adj[(0,0)])
map[(0,0)] = 0

def explore(op):
    global curpos
    trypos = None
    it = 0
    while 1:
        #print("loop")
        # backtrack
        for p in shortest_path(g, tuple(curpos), (0, 0))[1:]:
            d = getdirnr(np.array(p) - curpos)
            curpos = p[:]
            yield d
            next(op)
        
        # find untested
        for p in shortest_path(g, tuple(curpos), "untested")[1:-1]:
            d = getdirnr(np.array(p) - curpos)
            curpos = p[:]
            yield d
            next(op)
        
        # test directions
        for d, dir in enumerate(dirs, 1):
            trypos = curpos + dir
            trypos_t = tuple(trypos)
            if trypos_t not in map:
                break
        else:
            #print(f"{curpos} fully tested")
            g.remove_edge(tuple(curpos), "untested")
            continue
        
        # untested direction trypos/d
        #print("testing", d, trypos_t)
        yield d
        i = next(op)
        curpos_t = tuple(curpos)
        if i == 0:
            # hit a wall
            #print(f"hit wall at {trypos_t}")
            map[trypos_t] = 1
        elif i == 1:
            map[trypos_t] = 0
            g.add_edge(trypos_t, "untested")
            g.add_edge(curpos_t, trypos_t)
            g.add_edge(trypos_t, curpos_t)
            curpos = trypos[:]
        else:
            assert i == 2
            print("found home", trypos_t)
            print(shortest_path_length(g, (0,0), curpos_t) + 1)
            write_adjlist(g, "15/found.adjlist")
            break

        

m = IterMachine(clean_prg, None)

it1, it2 = itertools.tee(m.iter_output())
m.inv = explore(it1)


tiles = {
    0: " ",
    1: "#",
    2: "x",
    3: "-",
    4: "o"
}


for it, o in enumerate(it2):
    if it % 10000 == 0:
        draw(sparse_to_array(map), charmap=tiles)

draw(sparse_to_array(map), charmap=tiles)


