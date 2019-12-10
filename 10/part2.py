import math
map = [line.strip() for line in open("10/input.txt")]
w = len(map[0])
h = len(map)

c = {}
def gcd(a, b):
    if (a, b) in c:
        return c[(a, b)]
    if b == 0:
        r = a
    else:
        r = gcd(b, a%b)
    c[(a, b)] = r
    return r

def get_dirs(y, x):
    for j in range(h):
        for i in range(w):
            if j == y and i == x:
                continue
            g = gcd(abs(j-y), abs(i-x))
            dy, dx = (j-y)//g, (i-x)//g
            yield dy, dx


def laser(y, x, n=200):
    dirs = set(get_dirs(y, x))
    dirs = sorted(dirs, key=lambda d: -(math.atan2(d[1], d[0]) + 2 * math.pi))

    removed = set()
    while 1:
        for dy, dx in dirs:
            d = 1
            while 1:
                cy = y + d*dy
                cx = x + d*dx
                if cy < 0 or cy >= h or cx < 0 or cx >= w:
                    break
                m = map[cy][cx]
                
                if m == "#" and (cy, cx) not in removed:
                    if len(removed) == n - 1:
                        return (cy, cx)
                    removed.add((cy, cx))
                    break
                d += 1

ty, tx = laser(14, 19, 200)

print(tx * 100 + ty)
