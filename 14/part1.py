import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse
from collections import defaultdict

def tod(inglist):
    return {v: int(k) for k, v in inglist}

def read():
    for line in open("14/input-test.txt"):
        from_in, to_in = [p.strip() for p in line.split("=>")]
        sep = [s.strip() for s in from_in.split(", ")]
        ing_list = [s.split() for s in sep]
        to_n = to_in.split()
        yield tod(ing_list), tod([to_n])

recipes = list(read())

def build(ing, n):
    if ing == "ORE":
        return n, {}

    for requires, produces in recipes:
        if ing in produces:
            numproduced = produces[ing]
            required_processes = (n + numproduced -1) // numproduced
            extras_produced = required_processes * numproduced - n
            print(f"{n} {ing} requires {required_processes} * {requires} (extras:{extras_produced})")

            s = 0
            all_fluff = defaultdict(int)
            
            for k, v in requires.items():
                cost, fluff = build(k, v * required_processes)
                for a, b in fluff.items():
                    all_fluff[a] += b

                s += cost

            if extras_produced:
                all_fluff[ing] = extras_produced

            return s, all_fluff

print(build("FUEL", 1))
