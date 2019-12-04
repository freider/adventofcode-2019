rng = [109165, 576723]

def valid(s):
    last = s[0]
    has_same = False
    for c in s[1:]:
        if c < last:
            return False
        elif c == last:
            has_same = True
        last = c
    return has_same


def run():
    a = 0
    for x in range(109165, 576723 + 1):
        v = str(x)
        if valid([int(c) for c in v]):
            a+=1
    print(a)


run()
