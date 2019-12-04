clean_prg = [int(n) for n in open("02/input.txt").read().split(",")]

def sum(prg, i):
    a, b, c = prg[i+1: i+4]
    prg[c] = prg[a] + prg[b]
    return i+4

def mult(prg, i):
    a, b, c = prg[i+1: i+4]
    prg[c] = prg[a] * prg[b]
    return i+4

def abrt(prg, i):
    raise ExecutionEnded()

class ExecutionEnded(Exception):
    pass

INSTR = {
    1: sum,
    2: mult,
    99: abrt
}

def exec(prg):
    i = 0
    while 1:
        op = INSTR[prg[i]]
        try:
            i = op(prg, i)
        except ExecutionEnded:
            break


for a in range(100):
    for b in range(100):
        prg = [x for x in clean_prg]
        prg[1] = a
        prg[2] = b
        exec(prg)
        if prg[0] == 19690720:
            print(a * 100 + b)
            exit()
