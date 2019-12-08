import numpy as np

img_data = open("08/input.txt").read().strip()

dim = (6, 25)

intbuf = [int(i) for i in img_data]
layers = np.array(intbuf).reshape(-1, dim[0]*dim[1])

bestl = layers[np.argmin((layers == 0).sum(axis=1))]

print((bestl == 1).sum() * (bestl == 2).sum())
