import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse

s = [int(c) for c in open("16/input.txt").read().strip()]

#s = [int(c) for c in "03036732577212944063491565474664"]

base = [0, 1, 0, -1]

cache = {}
def cfilt(l, n):
    if (l, n) in cache:
        return cache[(l, n)]
    
    a = np.array(list(filt(l, n))) 
    cache[(l, n)] = a
    return a

def filt(l, n):
    skip = True
    m = 0
    for i in range(l + 1):
        for j in range(n):
            if not skip:
                yield base[i%len(base)]
            else:
                skip = False 
            m += 1
            if m > l:
                return

def trans(s):
    for d in range(len(s)):
        filter = cfilt(len(s), d + 1)
        mult = np.array(s) * np.array(filter)
        c = abs(np.sum(mult)) % 10
        yield c


t = s.copy()

for i in range(100):
    t = list(trans(t))

print(''.join(str(c) for c in t[:8]))
