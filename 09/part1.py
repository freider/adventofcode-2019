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
            1: self.sum,
            2: self.mult,
            3: self.inp,
            4: self.outp,
            5: self.jumpiftrue,
            6: self.jumpiffalse,
            7: self.lessthan,
            8: self.equals,
            9: self.adjustrel,
            99: self.abrt
        }

    def read(self, arg, mode):
        if mode == "0":
            return self.prg[arg]
        elif mode == "1":
            return arg
        elif mode == "2":
            return self.prg[self.rel + arg]
        else:
            print(f"BAD MODE {mode}")

    def write(self, arg, mode, v):
        if mode == "0":
            self.prg[arg] = v
        elif mode == "1":
            print(f"Can't write with mode={mode}")
        elif mode == "2":
            self.prg[self.rel + arg] = v

    def adjustrel(self, modes):
        a, = list(zip(self.prg[self.i+1: self.i+2], modes))
        self.rel += self.read(*a)
        return self.i+2

    def sum(self, modes):
        a, b, c = list(zip(self.prg[self.i+1: self.i+4], modes))
        self.write(c[0], c[1], self.read(*a) + self.read(*b))
        return self.i+4

    def mult(self, modes):
        a, b, c = list(zip(self.prg[self.i+1: self.i+4], modes))
        self.write(c[0], c[1], self.read(*a) * self.read(*b))
        return self.i+4

    def abrt(self, modes):
        raise ExecutionEnded()

    def inp(self, modes):
        if not self.inv:
            raise WaitingForInput()
        a, = list(zip(self.prg[self.i+1:self.i+2], modes))

        self.write(a[0], a[1], self.inv.pop(0))
        return self.i+2

    def outp(self, modes):
        a, = list(zip(self.prg[self.i+1:self.i+2], modes))
        o = self.read(*a)
        self.outv.append(o)
        return self.i+2

    def jumpiftrue(self, modes):
        a, b = list(zip(self.prg[self.i+1: self.i+3], modes))
        if self.read(*a):
            return self.read(*b)
        return self.i + 3

    def jumpiffalse(self, modes):
        a, b = list(zip(self.prg[self.i+1: self.i+3], modes))
        if not self.read(*a):
            return self.read(*b)
        return self.i + 3

    def lessthan(self, modes):
        a, b, c = list(zip(self.prg[self.i+1: self.i+4], modes))
        self.write(c[0], c[1], int(self.read(*a) < self.read(*b)))
        return self.i+4

    def equals(self, modes):
        a, b, c = list(zip(self.prg[self.i+1: self.i+4], modes))
        self.write(c[0], c[1], int(self.read(*a) == self.read(*b)))
        return self.i+4

    def exec(self):
        while 1:
            raw_op = self.prg[self.i]
            opcode = raw_op % 100
            op = self.INSTR[opcode]
            raw_mode = str(raw_op)[:-2]
            modes = ("0" * (3 - len(raw_mode)) + raw_mode)[::-1]
            try:
                self.i = op(modes)
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
