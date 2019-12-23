import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse
from networkx import Graph, DiGraph, shortest_path_length
from collections import deque
dsize = 10007
deck = list(range(dsize))


for line in open("22/input.txt"):
    line = line.strip()
    if line.startswith("deal into new stack"):
        deck.reverse()

    elif line.startswith("deal with increment"):
        n = int(line[len("deal with increment "):])
        d2 = range(dsize)
        
        j = 0
        q = deque(deck)
        while q:
            deck[j % dsize] = q.popleft()
            j += n

    elif line.startswith("cut"):
        n = int(line[4:])
        if n < 0:
            n = dsize + n

        deck = deck[n:] + deck[:n]

    else:
        print("error", line)

print(deck.index(2019))

#print(deck)