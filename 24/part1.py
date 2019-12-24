import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse

map = [[c for c in line.strip()] for line in open("24/input.txt")]


def do(map):
    cp = [[c for c in line] for line in map]

    for y, line in enumerate(map):
        for x, c in enumerate(line):
            full = 0
            empty = 0

            for dy, dx in [(0, 1), (-1, 0), (1, 0), (0, -1)]:
                if 0 <= y + dy < 5 and 0<= x + dx <5:
                    t = map[y+dy][x+dx]
                    if t == ".":
                        empty += 1
                    elif t == "#":
                        full += 1
                    else:
                        print("ERROR")

            if c == "#":
                if full != 1:
                    n = "."
                else:
                    n = "#"
            elif c == ".":
                if 1 <= full <= 2:
                    n = "#"
                else:
                    n = "."
            cp[y][x] = n

    return cp

import itertools

seen = set()
nxt = [[c for c in line] for line in map]

for i in itertools.count():
    score = 0

    st = '\n'.join(''.join(line) for line in nxt)
    j = 0
    for line in nxt:
        for c in line:
            if c == "#":
                score += 1 << j
            j+=1

    if st in seen:
        print(i, score)
        break
    seen.add(st)
    nxt = do(nxt)
