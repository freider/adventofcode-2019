import numpy as np
from lib.machine import IterMachine


color = {}
clean_prg = [int(x) for x in open("11/input.txt").read().strip().split(",")]

def drawer(ins):
    current_pos = np.array([0,0])
    dir = np.array([-1, 0])
    try:
        while 1:
            yield color.get(tuple(current_pos), 0)
            col = next(ins)
            dirchange = next(ins)
            color[tuple(current_pos)] = col
            if dirchange == 0:
                dir = np.array([-dir[1], dir[0]])
            elif dirchange == 1:
                dir = np.array([dir[1], -dir[0]])
            else:
                print("bad dir")
            current_pos += dir

    except StopIteration:
        print("program stopped")

m = IterMachine(clean_prg, None)
color[(0, 0)] = 1
m.inv = drawer(m.iter_output())
m.exec()

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
