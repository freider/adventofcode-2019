from lib.machine import Machine
from collections import deque

import numpy as np

color = {}
clean_prg = [int(x) for x in open("11/input.txt").read().strip().split(",")]

def drawer(ins):
    current_pos = (0,0)
    dir = (-1, 0)
    try:
        while 1:
            yield color.get(current_pos, 0)
            col = next(ins)
            dirchange = next(ins)
            color[current_pos] = col
            if dirchange == 0:
                dir = (-dir[1], dir[0])
            elif dirchange == 1:
                dir = (dir[1], -dir[0])
            else:
                print("bad dir")
            current_pos = tuple(np.array(current_pos) + np.array(dir))

    except StopIteration:
        print("program stopped")


q = deque()
m = Machine(clean_prg, q)
for col in drawer(m.iter_output()):
    q.append(col)

print(len(color))
