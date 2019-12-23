from lib.machine import Machine
from collections import deque

clean_prg = [int(c) for c in open("23/input.txt").read().strip().split(",")]


ms = [Machine(clean_prg.copy()) for i in range(50)]

for i in range(50):
    ms[i].inv.append(i)
    
ios = [m.io() for m in ms]

def f():
    nat = None
    lastnat = None
    while 1:
        idle = True
        for i, io in enumerate(ios):
            o = next(io)
            if o is None:
                ms[i].inv.append(-1)
                o = next(io)
            if o is None:
                continue
        
            idle = False

            if o == 255:
                nat = [next(io), next(io)]
                print("NAT", nat)
            else:
                c = o
                print("Sending to ", c)
                x = next(io)
                y = next(io)
                ms[c].inv.append(x)
                ms[c].inv.append(y)

        if idle:
            if not nat:
                print("idle with no nat values?!")
                exit()
            print("sending nat", nat)
            if lastnat and nat[1] == lastnat[1]:
                print("WE are done")
                return
            lastnat = nat
            ms[0].inv.append(nat[0])
            ms[0].inv.append(nat[1])


f()
