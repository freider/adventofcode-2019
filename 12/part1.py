import numpy as np
moons = np.array([
    [-9, 10, -1],
    [-14, -8, 14],
    [1, 5, 6],
    [-19, 7, 8]
])

velos = np.zeros(moons.shape, dtype=int)

for i in range(1000):
    for m in range(4):
        diff = moons - moons[m]
        vchange = diff//np.abs(diff)
        velos[m] += vchange.sum(axis=0)
    moons += velos

print(
    (np.abs(moons).sum(axis=1) * np.abs(velos).sum(axis=1)).sum()
)

