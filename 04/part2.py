rng = [109165, 576723]

def valid(s):
    last = s[0]
    has_same = False
    for i, c in enumerate(s[1:]):
        j = i+1
        if c < last:
            return False
        elif c == last:
            if (j-2 < 0 or s[j-2] != c) and (j+1 >= len(s) or s[j+1] != c):
                has_same = True
        last = c
    return has_same


def run():
    a = 0
    for x in range(109165, 576723 + 1):
        v = str(x)
        vi = [int(c) for c in v]
        if valid(vi):
            a+=1
    print(a)

run()
