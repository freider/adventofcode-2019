s = [int(c) for c in open("16/input.txt").read().strip()]
inputmult = 3
#s = [int(c) for c in "12345678"]

base = [0, 1, 0, -1]

cache = {}
m = len(s)

def charxitery(xy):
    if xy in cache:
        return cache[xy]
    x, y = xy
    if y == 0:
        ans = s[x % m]
    else:
        ss = 0
        for i in range(m * inputmult):
            n = (i+1)//(x + 1)
            mult = base[n % 4]
            if mult != 0:
                ss += mult * charxitery((i % m, y-1))

        ans = abs(ss) % 10
    cache[xy] = ans
    return ans

# too low -> 37590968
print(''.join(str(charxitery((x % m, 100))) for x in range(83687711-1, 83687711+7)))
