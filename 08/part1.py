import numpy as np

img_data = open("08/input.txt").read().strip()

dim = (25, 6)
#dim = (4, 2)

intbuf = [int(i) for i in img_data]
layers = np.array(intbuf).reshape(-1, dim[0]*dim[1])

#print(layers)
best = 1e10
bestl = None

for l in layers:
    s = (l == 0).sum()
    if s < best:
        best = s
        bestl = l


print((bestl == 1).sum() * (bestl == 2).sum())
