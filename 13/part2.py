import numpy as np
from numpy import array as V
from collections import deque
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine, WaitingForInput
from lib.parse import ReParse


prg = [int(x) for x in open("13/input.txt").read().strip().split(",")]
prg[0] = 2
q = deque([])


tiles = {
    0: " ",
    1: "#",
    2: "x",
    3: "-",
    4: "o"
}

def drawer(ins):
    while 1:
        try:
            x = next(ins)
            y = next(ins)
            t = next(ins)
            yield x, y, t
        except StopIteration:
            break
        except WaitingForInput:
            paddle = gett(3)
            ball = gett(4)
            if paddle is not None and ball is not None:
                #draw(sparse_to_array(color), charmap=tiles)
                #print("action")
                if ball[1] > paddle[1]:
                    #print("right")
                    q.append(1)
                elif ball[1] < paddle[1]:
                    #print("left")
                    q.append(-1)
                else:
                    #print("still")
                    q.append(0)
            m._started = False
            ins = m.iter_output()  # restart ?

m = Machine(prg, q)
op = m.iter_output()

color = {}
score = 0

def gett(t):
    for p, v in color.items():
        if v == t:
            return V(list(p))

oldy = None
started = False
prevnumleft = None
prevscore = None
for x, y, t in drawer(op):
    if x == -1 and y == 0:
        score = t
        if prevscore != score:
            print("score: ", score)
        prevscore = score
        continue
    
    color[(y, x)] = t
    ball = gett(4)
    paddle = gett(3)
    if paddle is not None:
        started = True
        
    if started:
        numleft = sum(1 for v in color.values() if v == 2)
        if numleft == 0:
            print("DONE!")
        if prevnumleft != numleft:
            print("numleft: ", numleft)
        prevnumleft = numleft

    if ball is not None and ball[0] != oldy:
        #print("-------------------FRAME-------------------")
        #draw(sparse_to_array(color), charmap=tiles)
        oldy = ball[0]

draw(sparse_to_array(color), charmap=tiles)
print(score)