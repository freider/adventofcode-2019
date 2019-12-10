# rewrite of part1 using my lib.machine cleanup

from lib.machine import IterMachine

clean_prg = [int(n) for n in open("09/input.txt").read().split(",")]

m = IterMachine(clean_prg.copy(), iter([2]))
for o in m.iter_output():
    print(o)
