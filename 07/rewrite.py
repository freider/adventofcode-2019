import itertools
from collections import deque

class ExecutionEnded(Exception):
    pass

class WaitingForInput(Exception):
    pass

class MachineState:
    def __init__(self, prg, inv):
        self.prg = prg
        self.inv = inv
        self.outv = deque()
        self.i = 0
        self.rel = 0
        self.INSTR = {
            1: (self.sum, 3),
            2: (self.mult, 3),
            3: (self.inp, 1),
            4: (self.outp, 1),
            5: (self.jumpiftrue, 2),
            6: (self.jumpiffalse, 2),
            7: (self.lessthan, 3),
            8: (self.equals, 3),
            9: (self.adjustrel, 1),
            99: (self.abrt, 0)
        }

    def checkmem(self, j):
        memsize = len(self.prg)
        if j >= memsize:
            expand_by = max(j - memsize + 1, 2 * memsize)
            self.prg += [0] * expand_by
    
    def read(self, j):
        self.checkmem(j)
        return self.prg[j]

    def write(self, j, v):
        self.checkmem(j)
        self.prg[j] = v

    def adjustrel(self, j):
        self.rel += self.read(j)

    def sum(self, j, k, l):
        self.write(l, self.read(j) + self.read(k))

    def mult(self, j, k, l):
        self.write(l, self.read(j) * self.read(k))

    def abrt(self):
        raise ExecutionEnded()

    def inp(self, j):
        if not self.inv:
            raise WaitingForInput()

        self.write(j, next(self.inv))

    def outp(self, j):
        o = self.read(j)
        self.outv.append(o)

    def jumpiftrue(self, j, k):
        if self.read(j):
            self.i = self.read(k)

    def jumpiffalse(self, j, k):
        if not self.read(j):
            self.i = self.read(k)

    def lessthan(self, j, k, l):
        self.write(l, int(self.read(j) < self.read(k)))

    def equals(self, j, k, l):
        self.write(l, int(self.read(j) == self.read(k)))

    def get_cursor_pos(self, rawpos, mode):
        if mode == "0":
            return self.prg[rawpos]
        elif mode == "1":
            return rawpos
        elif mode == "2":
            return self.prg[rawpos] + self.rel
        else:
            print(f"BAD MODE {mode}")

    def tick(self):
        i = self.i
        raw_op = self.prg[i]
        opcode = raw_op % 100
        op, numargs = self.INSTR[opcode]
        raw_mode = str(raw_op)[:-2]
        modes = ("0" * (numargs - len(raw_mode)) + raw_mode)[::-1]
        args = range(self.i+1, self.i+1+numargs)
        cursors = [self.get_cursor_pos(*t) for t in zip(args, modes)]

        op(*cursors)
        if i == self.i:
            self.i += 1 + numargs

    def exec(self):
        while 1:
            try:
                self.tick()
            except ExecutionEnded:
                break

    def iter_output(self):
        while 1:
            try:
                self.tick()
            except ExecutionEnded:
                break
            finally:
                while self.outv:
                    yield self.outv.popleft()

    def chain_input(self, ing):
        self.inv = itertools.chain(self.inv, ing)


def link_machines(machine_states):
    for i, m in enumerate(machine_states[1:], 1):
        m.chain_input(machine_states[i-1].iter_output())
    out = machine_states[-1].iter_output()
    out1, out2 = itertools.tee(out, 2)
    machine_states[0].chain_input(out1)
    return out2


clean_prg = [int(n) for n in open("07/input.txt").read().split(",")]


best = 0
best_phases = None
for phases in itertools.permutations(range(5, 10)):
    machine_states = [
        MachineState(clean_prg.copy(), iter([p]))
        for i, p in enumerate(phases)
    ]
    machine_states[0].chain_input(iter([0]))
    out = link_machines(machine_states)

    for o in out:
        pass
    v = o

    if v > best:
        best = v
        best_phases = phases

print(best, best_phases)

