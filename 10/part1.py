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


def numdet(y, x):
    seen = set()
    for j in range(h):
        for i in range(w):
            if j == y and i == x:
                continue
            g = gcd(abs(j-y), abs(i-x))
            dy, dx = (j-y)//g, (i-x)//g

            for dir in (-1, 1):
                d = dir
                while 1:
                    cy = y + d*dy
                    cx = x + d*dx
                    if cy < 0 or cy >= h or cx < 0 or cx >= w:
                        break
                    m = map[cy][cx]
                    
                    if m == "#":
                        # if (cy, cx) not in seen:
                        #     print(f"sees {cx, cy} via {x, y} + {d}*{dx, dy} ({i, j})")
                        seen.add((cy, cx))
                        break
                    d += dir

    return len(seen)

def gen():
    for y, row in enumerate(map):
        for x, p in enumerate(row):
            if p == "#":
                d = numdet(y, x)
                yield d, (y, x)

print(max(gen()))