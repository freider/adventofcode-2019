import numpy as np

img_data = open("08/input.txt").read().strip()

dim = (6, 25)
layersize = dim[0] * dim[1]

intbuf = [int(i) for i in img_data]

layers = np.array(intbuf, dtype=int).reshape(-1, layersize)
img = layers[np.argmax(layers != 2, axis=0), range(len(layers[0]))]

paint = {
    2: "/",
    1: "█",
    0: " ",
}

for l in img.reshape(*dim):
    print(''.join(paint[x] for x in l))
