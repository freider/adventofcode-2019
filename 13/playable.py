from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import IterMachine
from curses import wrapper

prg = [int(x) for x in open("13/input.txt").read().strip().split(",")]
prg[0] = 2


tiles = {
    0: " ",
    1: "#",
    2: "x",
    3: "-",
    4: "o"
}

def pixel(ins):
    while 1:
        try:
            x = next(ins)
            y = next(ins)
            t = next(ins)
            yield x, y, t
        except StopIteration:
            break

color = {}

def gett(t):
    for p, v in color.items():
        if v == t:
            return V(list(p))


def run(scr):
    def input_responder():
        while 1:
            yield {"KEY_LEFT": -1, "KEY_RIGHT": 1}.get(scr.getkey(), 0)

    m = IterMachine(prg, input_responder())
    score = 0
    op = m.iter_output()
    scr.clear()
    for x, y, t in pixel(op):
        if x == -1 and y == 0:
            score = t
            continue
        
        color[(y, x)] = t
        scr.addstr(y, x, tiles[t])
        scr.addstr(20, 0, f"Score: {score}")
        scr.refresh()

wrapper(run)
