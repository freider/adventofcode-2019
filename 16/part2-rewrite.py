import numpy as np
s = [int(c) for c in open("16/input.txt").read().strip()]
inputmult = 10000
#s = [int(c) for c in "1234"]

s = np.array(s * inputmult, dtype=int)
nxt = np.zeros(s.shape, dtype=int)
base = [0, 1, 0, -1]

def dist(s, nxt):
    print(f"iter {it}")
    nxt[:] = 0
    l = len(s)
    for i in range(l//2):
        if i % 1000 == 0:
            print(f"i {i}")
        c = s[i]
        if c != 0:
            # distribute over 
            for j in range(i+1):
                n = (i+1)//(j + 1)
                mult = base[n % 4]
                if mult != 0:
                    nxt[j] += mult * c

    for i in range(l//2, l):
        print(f"i {i}")
        c = s[i]
        if c != 0:
            for j in range(l//2):
                n = (i+1)//(j + 1)
                mult = base[n % 4]
                if mult != 0:
                    nxt[j] += mult * c

    nxt[l//2] += s[-1]
    for j in range(l//2, l):
        nxt[j] += nxt[j-1] - s[j-1]

    np.abs(nxt, out=nxt)
    nxt %= 10


for it in range(1):
    dist(s, nxt)
    s[:] = nxt[:]

print(''.join(str(c) for c in s[:8]))
