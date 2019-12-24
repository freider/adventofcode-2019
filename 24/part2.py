import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse

map = [[c for c in line.strip()] for line in open("24/input.txt")]


def do(prev, cur, nxt):
    cp = [[c for c in line] for line in cur]

    for y, line in enumerate(cur):
        for x, c in enumerate(line):
            full = 0

            for dy, dx in [(0, 1), (-1, 0), (1, 0), (0, -1)]:
                if 0 <= y + dy < 5 and 0<= x + dx <5:
                    ty = y + dy
                    tx = x + dx
                    if (ty, tx) != (2, 2):
                        t = cur[ty][tx]
                        if t == "#":
                            full += 1
                        elif t != ".":
                            print("ERROR")
                    elif nxt:
                        #print(y, x, "using nxt")
                        # use nxt
                        if y == 1:
                            # first row
                            full += sum(1 for d in nxt[0] if d == "#")
                        elif y == 3:
                            # last row
                            full += sum(1 for d in nxt[-1] if d == "#")
                        elif x == 1:
                            # first column
                            full += sum(1 for d in nxt if d[0] == "#")
                        elif x == 3:
                            # last column
                            #print("YAY", y, x, sum(1 for d in nxt if d[-1] == "#"))
                            full += sum(1 for d in nxt if d[-1] == "#")
            
            # handle outer rim using prev
            if prev:
                if y == 0:
                    full += 1 if prev[1][2] == "#" else 0
                elif y == 4:
                    full += 1 if prev[3][2] == "#" else 0
                if x == 0:
                    full += 1 if prev[2][1] == "#" else 0
                elif x == 4:
                    full += 1 if prev[2][3] == "#" else 0

            #print(y, x, c, full)
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


layers = [map]

def getlayer(j):
    if 0<=j<len(layers):
        return layers[j]
    else:
        return None

for i in range(200):
    newfirst = [['.' for j in range(5)] for k in range(5)]
    newlast = [['.' for j in range(5)] for k in range(5)]
    layers = [
        do(None, newfirst, layers[0])
    ] + [do(getlayer(j-1), getlayer(j), getlayer(j+1)) for j in range(len(layers))] + [
        do(layers[-1], newlast, None)
    ]

s = 0
for layer in layers:
    for y, line in enumerate(layer):
        for x, c in enumerate(line):
            if (y,x) != (2,2) and c == "#":
                s += 1

# too high: 5211
print(s)


# for l in layers:
#     for line in l:
#         print(''.join(line))
#     print()
