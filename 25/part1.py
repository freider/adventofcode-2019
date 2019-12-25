import sys
import numpy as np
from numpy import array as V
from lib.npdraw import draw, sparse_to_array
from lib.machine import Machine, IterMachine
from lib.parse import ReParse

clean_prg = [int(c) for c in open("25/input.txt").read().split(",")]

m = Machine(clean_prg)
io = m.io()

def send(cmd):
    for c in cmd:
        m.inv.append(ord(c))
    m.inv.append(10)


mv = None

cur = (0, 0)
map = {cur: 0}

def addpos(p1, p2):
    return tuple(a + b for a, b in zip(p1, p2))


mv_map = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1),
}

forbidden = [
    "giant electromagnet",
    "escape pod",
    "photons",
    "infinite loop",
    "molten lava"
]

shortcuts = {
    "w": "north",
    "s": "south",
    "a": "west",
    "d": "east"
}

def read(io):
    buf = ""
    o = ""
    try:
        while 1:
            o = next(io)
            if o is None:
                break
            buf += chr(o)
    except StopIteration:
        print(buf)
        raise
    return buf

def try_all_inv(io):
    send("inv")
    print("Direction?")
    try_cmd = input().strip()

    all_items = []
    for line in read(io).split("\n"):
        if line.startswith("- "):
            item = line[2:]
            all_items.append(item)

    bits = len(all_items)
    current_items = set(all_items)
    for selection in range(1 << bits):
        picked = [bool(selection & (1 << i)) for i in range(bits)]
        trycomb = list(zip(all_items, picked))
        for it, should_use in trycomb:
            if should_use and it not in current_items:
                send("take " + it)
                current_items.add(it)
                buf = read(io)
            elif not should_use and it in current_items:
                send("drop " + it)
                current_items.remove(it)
                buf = read(io)
        send(try_cmd)
        buf = read(io)
        if "ejected back to the checkpoint" not in buf:
            print("Found the perfect items", [a for a, b in trycomb if b])
            return
        else:
            print("Failed using", [a for a, b in trycomb if b])

while 1:
    buf = read(io)

    if mv in mv_map:  # last move
        tp = addpos(cur, mv_map[mv])
        if "You can't go that way." in buf or "ejected back to the checkpoint" in buf:
            tp = addpos(cur, tp)
            map[tp] = 1
        else:
            map[tp] = 0
            cur = tp

    if "Doors here lead" in buf:
        for dname, dir in mv_map.items():
            dp = addpos(cur, dir)
            if "- " + dname in buf:
                if map.get(dp) != 0:
                    map[dp] = 2
            else:
                map[dp] = 1
    else:
        print(repr(buf))

    if "Items here:" in buf:
        lines = buf.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("Items here:"):
                break
        for line in lines[i+1:]:
            if line.startswith("- "):
                it = line[2:]
                if it not in forbidden:
                    # take
                    send("take " + it)
                    read(io)
            else:
                break

    map[cur] = 3
    draw(sparse_to_array(map))
    map[cur] = 0
    
    print(buf)

    mv = input().strip()
    if mv in shortcuts:
        mv = shortcuts[mv]
    
    if mv == "clear":
        cur = (0,0)
        map = {cur: 0}
        continue

    if mv == "try":
        try_all_inv(io)
        continue

    send(mv)
