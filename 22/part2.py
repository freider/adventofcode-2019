import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse
from networkx import Graph, DiGraph, shortest_path_length
from collections import deque


def mod_inverse(a, m):
    if (m == 1): 
        return 0

    m0 = m
    y = 0
    x = 1
  
    while a > 1: 
        q = a // m
        t = m 
        m = a % m 
        a = t 
        t = y 
  
        y = x - q * y 
        x = t 
  
    return (x + m) % m0


dsize = 119315717514047
reps = 101741582076661
deck = None
infile = "22/input.txt"


instrs = [line.strip() for line in open(infile)]
debug = False

def it():
    global deck
    first = 0
    step = 1
    for instr in instrs:
        if instr.startswith("deal into new stack"):
            if deck:
                deck.reverse()
            first = (dsize + first - step) % dsize
            step = -step

        elif instr.startswith("deal with increment"):
            n = int(instr[len("deal with increment "):])
            newstep = mod_inverse(n, dsize)
            step = (step * newstep) % dsize

            if deck:
                j = 0
                q = deque(deck)
                while q:
                    deck[j % dsize] = q.popleft()
                    j += n

        elif instr.startswith("cut"):
            n = int(instr[4:])
            if n < 0:
                n = dsize + n
            
            first = (dsize + first + n * step) % dsize

            if deck:
                deck = deck[n:] + deck[:n]

        else:
            print("error", instr)
        if debug:
            print(instr)
            print(first, step)

    return (first, step)

print(it())

def do(r):
    if r == 1:
        return it()
    if r % 2 == 0:
        (a, b) = do(r//2)
        (c, d) = (a, b)
    else:
        (a, b) = do(r-1)
        (c, d) = do(1)

    #a + b(c + dn)
    #a + bc + bdn
    return ((a + b*c) % dsize, d*b % dsize)


print("Do ", reps)
a, b = do(reps)
print((a + b * 2020) % dsize)

