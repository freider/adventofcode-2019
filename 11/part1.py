from lib.machine import IterMachine
from collections import defaultdict

import numpy as np

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
m.inv = drawer(m.iter_output())
m.exec()
print(len(color))