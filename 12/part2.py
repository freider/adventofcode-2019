import numpy as np
from fractions import gcd

moons = np.array([
    [-9, 10, -1],
    [-14, -8, 14],
    [1, 5, 6],
    [-19, 7, 8]
])

def calc(orig):
    pos = orig.copy()
    velos = np.zeros(pos.shape, dtype=int)
    origstate = (tuple(pos), tuple(velos))
    i = 0
    while 1:
        for m in range(4):
            diff = pos - pos[m]
            vchange = diff//np.abs(diff)
            velos[m] += vchange.sum(axis=0)
        pos += velos
        i += 1
        state = (tuple(pos), tuple(velos))
        if state == origstate:
            return i

a = calc(moons[:, 0])
c = calc(moons[:, 1])
e = calc(moons[:, 2])

# a, c, e = [161428, 231614, 108344]  # from above calc, took a while to run

print(a, c, e)

def lcm(a, b):
    return a * b // gcd(a, b)

print(lcm(lcm(a, c), e))

