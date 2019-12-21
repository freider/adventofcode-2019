import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine, WaitingForInput
from lib.parse import ReParse
from collections import defaultdict, deque
import itertools
import os
import json
from networkx import Graph, DiGraph, shortest_path, shortest_path_length, write_adjlist, read_adjlist, all_pairs_shortest_path_length

clean_prg = [int(x) for x in open("21/input.txt").read().strip().split(",")]

map = {}

q = deque([])
def sendword(s):
    for c in s:
        q.append(ord(c))
    q.append(10)
m = Machine(clean_prg.copy(), q)


#a and ((not a) or (not b) or (not c))

def main():
    out = []
    instr = [
        "NOT A T",   
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J"
    ]
    for i in instr:
        sendword(i)
    sendword("WALK")
    for o in m.iter_output():
        if o > 128:
            print("We are done", o)
            return
        out.append(chr(o))

    print(''.join(out))


main()