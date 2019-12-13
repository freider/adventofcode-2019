from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import IterMachine


prg = [int(x) for x in open("13/input.txt").read().strip().split(",")]
prg[0] = 2


tiles = {
    0: " ",
    1: "#",
    2: "x",
    3: "-",
    4: "o"
}

def pixel(ins):
    while 1:
        try:
            x = next(ins)
            y = next(ins)
            t = next(ins)
            yield x, y, t
        except StopIteration:
            break

def input_responder():
    while 1:
        #draw(sparse_to_array(color), charmap=tiles)
        #numleft = sum(1 for v in color.values() if v == 2)
        #print("numleft: ", numleft)
        #print("score: ", score)

        paddle = gett(3)
        ball = gett(4)
        
        if paddle is not None and ball is not None:
            if ball[1] > paddle[1]:
                yield 1
            elif ball[1] < paddle[1]:
                yield -1
            else:
                yield 0
        else:
            yield 0

m = IterMachine(prg, input_responder())
op = m.iter_output()

color = {}
score = 0

def gett(t):
    for p, v in color.items():
        if v == t:
            return V(list(p))

for x, y, t in pixel(op):
    if x == -1 and y == 0:
        score = t
        continue
    
    color[(y, x)] = t

print(score)