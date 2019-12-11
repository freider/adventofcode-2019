# rewrite of part1 using my lib.machine cleanup

from lib.machine import Machine
from collections import deque

clean_prg = [int(n) for n in open("09/input.txt").read().split(",")]

m = Machine(clean_prg.copy(), deque([2]))

for o in m.iter_output():
    print(o)
