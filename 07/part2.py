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
    if not inv:
        raise WaitingForInput()
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

class WaitingForInput(Exception):
    pass

class MachineState:
    def __init__(self, prg, inv, outv):
        self.prg = prg
        self.inv = inv
        self.outv = outv
        self.i = 0

    def exec(self):
        while 1:
            raw_op = self.prg[self.i]
            opcode = raw_op % 100
            op = INSTR[opcode]
            raw_mode = str(raw_op)[:-2]
            modes = ("0" * (3 - len(raw_mode)) + raw_mode)[::-1]
            try:
                self.i = op(self.prg, modes, self.i, self.inv, self.outv)
            except ExecutionEnded:
                break


def run(machine_states):
    while 1:
        for r, ms in enumerate(machine_states):
            #print(f"using {ms.inv}")
            try:
                ms.exec()
            except WaitingForInput:
                pass
            else:
                #print(f"Halting {r}")
                if r == len(machine_states)-1:
                    return

def link_machines(machine_states):
    for i, m in enumerate(machine_states):
        m.outv = machine_states[(i+1) % len(machine_states)].inv


clean_prg = [int(n) for n in open("07/input.txt").read().split(",")]

best = 0
best_phases = None
for phases in itertools.permutations(range(5, 10)):
    machine_states = [
        MachineState(clean_prg.copy(), [p], None)
        for p in phases
    ]
    link_machines(machine_states)
    machine_states[0].inv.append(0)

    run(machine_states)
    v = machine_states[4].outv[-1]

    if v > best:
        best = v
        best_phases = phases

print(best, best_phases)
