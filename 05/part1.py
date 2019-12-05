clean_prg = [int(n) for n in open("05/input.txt").read().split(",")]


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


INSTR = {
    1: sum,
    2: mult,
    3: inp,
    4: outp,
    99: abrt
}


def exec(prg, inv):
    i = 0
    outv = []
    while 1:
        raw_op = prg[i]
        opcode = raw_op % 100
        op = INSTR[opcode]
        print(f"OPCODE {opcode}")
        raw_mode = str(raw_op)[:-2]
        modes = ("0" * (3 - len(raw_mode)) + raw_mode)[::-1]
        try:
            i = op(prg, modes, i, inv, outv)
        except ExecutionEnded:
            break
    return outv

outv = exec(clean_prg, [1])
print(outv)
