prg = [int(n) for n in open("input.txt").read().split(",")]

prg[1] = 12
prg[2] = 2


for i in range(len(prg)/4):
    instr = prg[i*4:(i+1)*4]
    if instr[0] == 1:
        prg[instr[3]] = prg[instr[1]] + prg[instr[2]]
    elif instr[0] == 2:
        prg[instr[3]] = prg[instr[1]] * prg[instr[2]]
    elif instr[0] == 99:
        break
    else:
        print ("bad instr", instr[0])
        break

print prg[0]
