from lib.machine import Machine
from collections import deque

clean_prg = [int(x) for x in open("19/input.txt").read().strip().split(",")]

map = {}

target_width = 100
def getc(coord):
    m = Machine(clean_prg.copy(), deque([coord[1], coord[0]]))
    for o in m.iter_output():
        return o

startx = 0

for y in range(100000):
    for addx in range(4):
        tryx = startx + addx
        if getc((y, tryx)):
            startx = tryx
            map[(y, tryx)] = 1
            break
    else:
        print("no find")

    usey = y - (target_width - 1)
    usex = startx
    has_top_right = getc((usey, usex + (target_width - 1)))
    if has_top_right:
        print(usex * 10000 + usey)
        break
