import numpy as np
from fractions import gcd
from itertools import count
from functools import reduce

moons = np.array([
    [-9, 10, -1],
    [-14, -8, 14],
    [1, 5, 6],
    [-19, 7, 8]
])

velos = np.zeros(moons.shape, dtype=int)
origpos = moons.copy()
axistimes = np.zeros(3, dtype=int)

for i in count(1):
    for m in range(4):
        diff = moons - moons[m]
        vchange = diff//np.abs(diff)
        velos[m] += vchange.sum(axis=0)
    moons += velos
    axis_is_orig = np.logical_and((moons == origpos).all(axis=0), (velos==0).all(axis=0))
    axistimes = np.where(axistimes==0, axis_is_orig * i, axistimes)
    if axistimes.all():
        break

def lcm(a, b):
    return a * b // gcd(a, b)

print(reduce(lcm, axistimes))  # axistimes = [161428, 231614, 108344]  # from above calc, took a while to run

