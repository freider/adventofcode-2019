import numpy as np
raw = [int(c) for c in open("16/input.txt").read().strip()]
inputmult = 10000
offset = int(''.join(str(c) for c in raw[:7]))

s = np.array(raw * inputmult, dtype=int)
m = len(s)
m2 = m//2
nxt = np.zeros(s.shape, dtype=int)

for it in range(100):
    print(f"it {it}")
    nxt[m2] = np.sum(s[m2:])
    for i in range(m2 + 1, m):
        nxt[i] = nxt[i - 1] - s[i - 1]
    s[:] = np.abs(nxt) % 10


print(s[offset: offset + 8])