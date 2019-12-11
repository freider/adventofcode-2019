import itertools
from collections import deque

class ExecutionEnded(Exception):
    pass

class WaitingForInput(Exception):
    pass

class Machine:
    def __init__(self, prg, inv=None):
        self.prg = prg
        self.inv = inv if inv is not None else deque()
        self.outv = deque()
        self._started = False
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

    def adjustrel(self, j):
        self.rel += self.prg[j]

    def sum(self, j, k, l):
        self.prg[l] = self.prg[j] + self.prg[k]

    def mult(self, j, k, l):
        self.prg[l] = self.prg[j] * self.prg[k]

    def abrt(self):
        raise ExecutionEnded()

    def inp(self, j):
        if not self.inv:
            raise WaitingForInput()

        self.prg[j] = self.inv.popleft()

    def outp(self, j):
        o = self.prg[j]
        self.outv.append(o)

    def jumpiftrue(self, j, k):
        if self.prg[j]:
            self.i = self.prg[k]

    def jumpiffalse(self, j, k):
        if not self.prg[j]:
            self.i = self.prg[k]

    def lessthan(self, j, k, l):
        self.prg[l] = int(self.prg[j] < self.prg[k])

    def equals(self, j, k, l):
        self.prg[l] = int(self.prg[j] == self.prg[k])

    def get_cursor_pos(self, rawpos, mode):
        if mode == 0:
            return self.prg[rawpos]
        elif mode == 1:
            return rawpos
        elif mode == 2:
            return self.prg[rawpos] + self.rel
        else:
            print(f"BAD MODE {mode}")

    def tick(self):
        i = self.i
        raw_op = self.prg[i]
        opcode = raw_op % 100
        op, numargs = self.INSTR[opcode]
        
        cursors = [
            self.get_cursor_pos(i+1, (raw_op//100) % 10),
            self.get_cursor_pos(i+2, (raw_op//1000) % 10),
            self.get_cursor_pos(i+3, (raw_op//10000) % 10)
        ][:numargs]
        self.checkmem(max(cursors + [i]))
        op(*cursors)
        if i == self.i:
            self.i += 1 + numargs

    def prep_execution(self):
        assert not self._started, "Execution already started"
        self._started = True

    def exec(self):
        self.prep_execution()
        while 1:
            try:
                self.tick()
            except ExecutionEnded:
                break

    def iter_output(self):
        self.prep_execution()
        while 1:
            try:
                self.tick()
            except ExecutionEnded:
                break
            finally:
                while self.outv:
                    yield self.outv.popleft()

class IterMachine(Machine):
    # machine using iterator input
    def inp(self, j):
        self.prg[j] = next(self.inv)
