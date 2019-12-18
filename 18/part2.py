import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse

from collections import deque

map = [line.strip() for line in open("18/input2.txt")]

numkeys = 0
for y, r in enumerate(map):
    numkeys += sum(1 for c in r if c.islower())

print("numkeys", numkeys)

def findt(t):
    for y, r in enumerate(map):
        for x, c in enumerate(r):
            if c == t:
                yield (y, x)
            
for i, spos in enumerate(findt("@")):
    map[spos[0]] = map[spos[0]][:spos[1]] + str(i) + map[spos[0]][spos[1]+1:]

allkeys = set()
for y, r in enumerate(map):
    for x, c in enumerate(r):
        if c.islower():
            allkeys.add(c)


def addpos(p1, p2):
    return tuple(a + b for a, b in zip(p1, p2))


def get(pos):
    try:
        return map[pos[0]][pos[1]]
    except IndexError:
        return "#"

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

cache = {}

def findneighbours(start):
    q = deque()
    q.append((0, start))
    visited = {start}
    startt = get(start)
    ret = []
    while len(q) > 0:
        d, pos = q.popleft()
        t = get(pos)

        for dir in dirs:
            trypos = addpos(pos, dir)
            t = get(trypos)
            if trypos not in visited:
                if t == "#":
                    continue
                visited.add(trypos)
                if t in ".0123" or t.lower() == startt.lower():
                    q.append((d+1, trypos))
                else:
                    ret.append((d+1, t))

    return ret


def getedges():
    adj = {}
    for k in allkeys | {k.upper() for k in allkeys}:
        pos = list(findt(k))[0]
        if pos:
            adj[k] = findneighbours(pos)

    for c in "0123":
        adj[c] = findneighbours(list(findt(c))[0])
    return adj

import heapq

def findkeys():
    q = []
    edges = getedges()
    mindist = {}
    for boti in range(2, 3):
        heapq.heappush(q, (0, boti, "0123", frozenset()))
        mindist[(boti, "0123", frozenset())] = 0

    last = 0
    while len(q) > 0:
        d, boti, vs, found = heapq.heappop(q)
        #print(boti, vs, found)
        v = vs[boti]
        if d > mindist[(boti, vs, found)]:
            continue

        if len(found) > last:
            print("Found", len(found), d)
            last = len(found)

        if len(found) == numkeys:
            print("shortest path", d, found)
            break
        
        for d2, v2 in edges[v]:
            if v2.isupper() and v2.lower() not in found:
                continue

            newdist = d + d2
            tryset = found

            if v2.islower():
                tryset = found | {v2}
        
            vs2 = vs[:boti] + v2 + vs[boti+1:]
            if newdist < mindist.get((boti, vs2, tryset), 1e10):
                mindist[(boti, vs2, tryset)] = newdist
                heapq.heappush(q, (newdist, boti, vs2, tryset))
                if v2.islower() not in found:
                    # found something new, spread to other bots!
                    for j in range(4):
                        if j != boti and newdist < mindist.get((j, vs2, tryset), 1e10):
                            mindist[(j, vs2, tryset)] = newdist
                            heapq.heappush(q, (newdist, j, vs2, tryset))


findkeys()