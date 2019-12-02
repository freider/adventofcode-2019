clean_prg = [int(n) for n in open("input.txt").read().split(",")]


def run(prg):
    for i in range(len(prg)/4):
        instr = prg[i*4:(i+1)*4]
        if instr[0] == 1:
            prg[instr[3]] = prg[instr[1]] + prg[instr[2]]
        elif instr[0] == 2:
            prg[instr[3]] = prg[instr[1]] * prg[instr[2]]
        elif instr[0] == 99:
            break
        else:
            print("bad instr", instr[0])
            break


for a in xrange(100):
    for b in xrange(100):
        prg = [x for x in clean_prg]
        prg[1] = a
        prg[2] = b
        run(prg)
        if prg[0] == 19690720:
            print(a * 100 + b)
            exit()
