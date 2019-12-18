import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse

from collections import deque

map = [line.strip() for line in open("18/input.txt")]

numkeys = 0
for y, r in enumerate(map):
    numkeys += sum(1 for c in r if c.islower())

print("numkeys", numkeys)

def findt(t):
    for y, r in enumerate(map):
        for x, c in enumerate(r):
            if c == t:
                return (y, x)
            
startpos = findt("@")

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

def isopen(pos, found):
    try:
        g = get(pos)
        return g in (".", "@") or g.lower() in found or g.islower()
    except IndexError:
        return False

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
                if t in ".@" or t.lower() == startt.lower():
                    q.append((d+1, trypos))
                else:
                    ret.append((d+1, t))

    return ret


def getedges():
    adj = {}
    for k in allkeys | {k.upper() for k in allkeys}:
        pos = findt(k)
        if pos:
            adj[k] = findneighbours(pos)

    adj['@'] = findneighbours(findt('@'))
    return adj

import heapq

def findkeys():
    q = []
    edges = getedges()
    heapq.heappush(q, (0, '@', frozenset()))
    mindist = {('@', frozenset()): 0}
    last = 0
    while len(q) > 0:
        d, v, found = heapq.heappop(q)
        if d > mindist[(v, found)]:
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
            tryset = found
            if v2.islower():
                tryset = found | {v2}
            
            newdist = d + d2
            if newdist < mindist.get((v2, tryset), 1e10):
                mindist[(v2, tryset)] = newdist
                heapq.heappush(q, (newdist, v2, tryset))
        #print("adding", trypos, get(trypos), tryset)



findkeys()