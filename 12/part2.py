import numpy as np
from fractions import gcd

moons = np.array([
    [-9, 10, -1],
    [-14, -8, 14],
    [1, 5, 6],
    [-19, 7, 8]
])

def calc(orig):
    mem = set()
    pos = orig.copy()
    velos = np.zeros(pos.shape, dtype=int)
    i = 0
    a = None
    b = None
    origall = (tuple(pos), tuple(velos))
    mem = {origall}
    while 1:
        for m in range(4):
            diff = pos - pos[m]
            vchange = diff//np.abs(diff)
            velos[m] += vchange.sum(axis=0)
        pos += velos

        i += 1
        tup = (tuple(pos), tuple(velos))
        if tup in mem and a is None:
            a = i
        if tup == origall:
            b = i
            return a, b
        mem.add(tup)

a, b = calc(moons[:, 0])
c, d = calc(moons[:, 1])
e, f = calc(moons[:, 2])

# a, c, e = [161428, 231614, 108344]  # from above calc, took a while to run

print(a, c, e)

def lcm(a, b):
    return a * b // gcd(a, b)

print(lcm(lcm(a, c), e))

