import re

def valid(s):
    return tuple(s) == tuple(sorted(s)) and re.match(r'[0-9]*?(^|([0-9])(?!\2))([0-9])\3(?!\3)', s)

print(sum(1 for x in range(109165, 576723 + 1) if valid(str(x))))
