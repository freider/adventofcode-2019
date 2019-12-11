import itertools
from lib.machine import IterMachine

clean_prg = [int(n) for n in open("07/input.txt").read().split(",")]

best = 0
best_phases = None
for phases in itertools.permutations(range(5, 10)):
    machines = [
        IterMachine(clean_prg.copy(), iter([p]))
        for i, p in enumerate(phases)
    ]
    machines[0].chain_input(iter([0]))

    for i, m in enumerate(machines):
        m.chain_input(machines[i-1].iter_output())

    machines[0].inv, peek = itertools.tee(machines[0].inv, 2)
    for v in peek:
       pass

    if v > best:
        best = v
        best_phases = phases

print(best, best_phases)
