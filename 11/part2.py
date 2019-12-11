import numpy as np
import collections
from lib.machine import Machine, IterMachine


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

inputq = collections.deque()
m = Machine(clean_prg, inputq)
color[(0, 0)] = 1
for current_color in drawer(m.iter_output()):
    inputq.append(current_color)

minx, maxx = (1e10, -1e10)
miny, maxy = (1e10, -1e10)
for coord, col in color.items():
    minx = min(minx, coord[1])
    miny = min(miny, coord[0])
    maxx = max(maxx, coord[1])
    maxy = max(maxy, coord[0])

for i in range(miny, maxy + 1): 
    row = ''.join([
        "#" if color.get((i, j)) else " " 
        for j in range(minx, maxx + 1)])
    print(row)
