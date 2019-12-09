import itertools


class ExecutionEnded(Exception):
    pass

class WaitingForInput(Exception):
    pass

class MachineState:
    def __init__(self, prg, inv, outv):
        self.prg = prg
        self.inv = inv
        self.outv = outv
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

    def read(self, j):
        return self.prg[j]

    def write(self, j, v):
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

        self.write(j, self.inv.pop(0))

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

    def exec(self):
        while 1:
            i = self.i
            raw_op = self.prg[i]
            opcode = raw_op % 100
            op, numargs = self.INSTR[opcode]
            raw_mode = str(raw_op)[:-2]
            modes = ("0" * (numargs - len(raw_mode)) + raw_mode)[::-1]
            args = range(self.i+1, self.i+1+numargs)
            cursors = [self.get_cursor_pos(*t) for t in zip(args, modes)]

            try:
                op(*cursors)
                if i == self.i:
                    self.i += 1 + numargs
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


clean_prg = [int(n) for n in open("09/input.txt").read().split(",")] + [0 for x in range(10000)]

buf = []
m = MachineState(clean_prg.copy(), [2], buf)
m.exec()
print(buf)
