import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse


clean_prg = [int(x) for x in open("13/input.txt").read().strip().split(",")]

def drawer(ins):
    while 1:
        try:
            x = next(ins)
            y = next(ins)
            t = next(ins)
            yield x, y, t
        except StopIteration:
            print("program stopped")
            return


m = Machine(clean_prg)
op = m.iter_output()

color = {}
for x, y, t in drawer(op):
    color[(x, y)] = t

tiles = {
    0: " ",
    1: "#",
    2: "x",
    3: "-",
    4: "o"
}
draw(sparse_to_array(color), charmap=tiles)
print(sum(1 for c in color.values() if c == 2))

