import numpy as np

img_data = open("08/input.txt").read().strip()

dim = (25, 6)

intbuf = [int(i) for i in img_data]
layers = np.array(intbuf).reshape(-1, dim[0]*dim[1])

stacked = np.zeros(dim[0]*dim[1], dtype=int) + 2
for l in layers:    
    for i, v in enumerate(stacked):
        if v == 2:
            stacked[i] = l[i]

def paint(x):
    if x == 2:
        return "/"
    elif x == 1:
        return " "
    else:
        return "#"

for l in stacked.reshape(6, 25):
    print(''.join(paint(x) for x in l))
