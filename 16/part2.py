s = [int(c) for c in open("16/input.txt").read().strip()]
inputmult = 10000

s = "1234"
inputmult = 4


base = [0, 1, 0, -1]

cache = {}
m = len(s)

def charxitery(xy):
    if xy in cache:
        return cache[xy]
    x, y = xy
    if y == 0:
        ans = s[x % m]
    elif x > m * /2:
        ans = abs(charxitery((x-1, y)) - s[(x-1) % m]) % 10
    else:
        ss = 0
        p = 4 * (x + 1)
        for i in range(p):
            n = (i+1)//(x + 1)
            mult = base[n % 4]
            if mult != 0:
                ss += mult * charxitery((i, y-1))

        ans = abs(ss * ((m * inputmult) // p)) % 10
    cache[xy] = ans
    return ans


#range_start = int(''.join(str(c) for c in s[:7]))

range_start = 8
print(range_start)
print(''.join(str(charxitery((x, 100))) for x in range(range_start, range_start + 8)))

# 53541333 -> too low
