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

def findkeys(start):
    q = deque()
    q.append((0, start, frozenset()))
    visited = set((start, frozenset()))
    last = 0
    while len(q) > 0:
        d, pos, found = q.popleft()
        #visited.add((pos, found))
        t = get(pos)

        if t.islower():
            found = found | {t}
        if len(found) > last:
            print("Found", len(found))
            last = len(found)

        if len(found) == numkeys:
            print("shortest path", d)
            break

        for dir in dirs:
            trypos = addpos(pos, dir)
            t = get(pos)
            tryset = found

            if t.islower() and t not in found:
                tryset = tryset | {t}
            #print("1,15", get((1,15)), isopen((1, 15), found))
            if isopen(trypos, found) and not (trypos, tryset) in visited:
                visited.add((trypos, tryset))
                q.append((d+1, trypos, tryset))
                #print("adding", trypos, get(trypos), tryset)



print(findkeys(startpos))