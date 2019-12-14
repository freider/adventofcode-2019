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

            s = 0
            for k, v in requires.items():
                cost, new_inventory = build(k, v * required_processes, new_inventory)
                s += cost

            new_inventory[ing] += extras_produced

            return s, new_inventory


target_ore = 1000000000000
low = 1
high = 1
while 1:
    needed_ore, _ = build("FUEL", high, defaultdict(int))
    if needed_ore < target_ore:
        low = high
        high *= 2
    else:
        break

cur = low + (high - low) // 2
while 1:
    needed_ore, _ = build("FUEL", cur, defaultdict(int))
    if needed_ore < target_ore:
        newcur = cur + (high - cur) //2
        low = cur
    else:
        newcur = cur - (cur - low) //2
        high = cur
    
    if newcur == cur:
        break
    cur = newcur


print(
    cur-1, build("FUEL", cur-1, defaultdict(int))[0]
)

print(
    cur, build("FUEL", cur, defaultdict(int))[0]
)

print(
    cur+1, build("FUEL", cur + 1, defaultdict(int))[0]
)

print(cur)
