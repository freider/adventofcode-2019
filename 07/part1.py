import itertools

def read(prg, i, mode):
    if mode == "0":
        return prg[i]
    elif mode == "1":
        return i
    else:
        print(f"BAD MODE {mode}")


def sum(prg, modes,  i, inv, outv):
    a, b, c = list(zip(prg[i+1: i+4], modes))
    prg[c[0]] = read(prg, *a) + read(prg, *b)
    return i+4

def mult(prg, modes, i, inv, outv):
    a, b, c = list(zip(prg[i+1: i+4], modes))
    prg[c[0]] = read(prg, *a) * read(prg, *b)
    return i+4

def abrt(prg, modes, i, inv, outv):
    raise ExecutionEnded()

class ExecutionEnded(Exception):
    pass

def inp(prg, modes, i, inv, outv):
    a, = list(zip(prg[i+1:i+2], modes))
    prg[a[0]] = inv.pop(0)
    return i+2

def outp(prg, modes, i, inv, outv):
    a, = list(zip(prg[i+1:i+2], modes))
    o = read(prg, *a)
    outv.append(o)
    return i+2

def jumpiftrue(prg, modes,  i, inv, outv):
    a, b = list(zip(prg[i+1: i+3], modes))
    if read(prg, *a):
        return read(prg, *b)
    return i + 3

def jumpiffalse(prg, modes,  i, inv, outv):
    a, b = list(zip(prg[i+1: i+3], modes))
    if not read(prg, *a):
        return read(prg, *b)
    return i + 3

def lessthan(prg, modes, i, inv, outv):
    a, b, c = list(zip(prg[i+1: i+4], modes))
    prg[c[0]] = int(read(prg, *a) < read(prg, *b))
    return i+4

def equals(prg, modes, i, inv, outv):
    a, b, c = list(zip(prg[i+1: i+4], modes))
    prg[c[0]] = int(read(prg, *a) == read(prg, *b))
    return i+4

INSTR = {
    1: sum,
    2: mult,
    3: inp,
    4: outp,
    5: jumpiftrue,
    6: jumpiffalse,
    7: lessthan,
    8: equals,
    99: abrt
}


def exec(prg, inv):
    i = 0
    outv = []
    while 1:
        raw_op = prg[i]
        opcode = raw_op % 100
        op = INSTR[opcode]
        raw_mode = str(raw_op)[:-2]
        modes = ("0" * (3 - len(raw_mode)) + raw_mode)[::-1]
        try:
            i = op(prg, modes, i, inv, outv)
        except ExecutionEnded:
            break
    return outv


clean_prg = [int(n) for n in open("07/input.txt").read().split(",")]

best = 0
best_phases = None
for phases in itertools.permutations(range(5)):
    v = 0
    for p in phases:
        prg = [i for i in clean_prg]
        v = exec(prg, [p, v])[0]

    if v > best:
        best = v
        best_phases = phases

print(best, best_phases)
