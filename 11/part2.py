import numpy as np
import collections
from lib.machine import Machine, IterMachine
from lib.npdraw import draw, sparse_to_array


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

pic = sparse_to_array(color)
draw(pic)
