from lib.machine import Machine
from collections import deque

clean_prg = [int(c) for c in open("23/input.txt").read().strip().split(",")]


ms = [Machine(clean_prg.copy()) for i in range(50)]

for i in range(50):
    ms[i].inv.append(i)
    
ios = [m.io() for m in ms]

def f():
    while 1:
        for i, io in enumerate(ios):
            o = next(io)
            if o is None:
                ms[i].inv.append(-1)
            elif o == 255:
                print("End", next(io), next(io))
                return
            else:
                c = o
                print("Sending to ", c)
                x = next(io)
                y = next(io)
                ms[c].inv.append(x)
                ms[c].inv.append(y)

f()
