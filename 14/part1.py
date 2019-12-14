import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse
from collections import defaultdict

def tod(inglist):
    return {v: int(k) for k, v in inglist}

def read():
    for line in open("14/input.txt"):
        from_in, to_in = [p.strip() for p in line.split("=>")]
        sep = [s.strip() for s in from_in.split(", ")]
        ing_list = [s.split() for s in sep]
        to_n = to_in.split()
        yield tod(ing_list), tod([to_n])

recipes = list(read())

def build(ing, n, inventory):
    if ing == "ORE":
        return n, inventory
    
    new_inventory = inventory.copy()

    if ing in inventory:
        used_inv = min(new_inventory[ing], n)
        n -= used_inv
        new_inventory[ing] -= used_inv

    for requires, produces in recipes:
        if ing in produces:
            numproduced = produces[ing]
            required_processes = (n + numproduced -1) // numproduced

            extras_produced = required_processes * numproduced - n
            print(f"{n} {ing} requires {required_processes} * {requires} (extras:{extras_produced})")

            s = 0
            for k, v in requires.items():
                cost, new_inventory = build(k, v * required_processes, new_inventory)
                s += cost

            new_inventory[ing] += extras_produced

            return s, new_inventory

print(build("FUEL", 1, defaultdict(int)))
#print()
#start = defaultdict(int)
# start["A"] = 1
# start["B"] = 1
#print(build("AB", 1, start))
