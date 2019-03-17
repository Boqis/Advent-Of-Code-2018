#!/usr/local/bin/python3
import re

# the 16 opcode-functions should be refactored... Most are very similar.

def addr(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] + reg[ins[2]]
    return out

def addi(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] + ins[2]
    return out

def mulr(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] * reg[ins[2]]
    return out

def muli(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] * ins[2]
    return out

def banr(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] & reg[ins[2]]
    return out

def bani(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] & ins[2]
    return out

def borr(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] | reg[ins[2]]
    return out

def bori(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]] | ins[2]
    return out

def setr(reg, ins):
    out = reg.copy()
    out[ins[3]] = reg[ins[1]]
    return out

def seti(reg, ins):
    out = reg.copy()
    out[ins[3]] = ins[1]
    return out

def gtir(reg, ins):
    out = reg.copy()
    if ins[1] > reg[ins[2]]:
        out[ins[3]] = 1
    else:
        out[ins[3]] = 0
    return out

def gtri(reg, ins):
    out = reg.copy()
    if reg[ins[1]] > ins[2]:
        out[ins[3]] = 1
    else:
        out[ins[3]] = 0
    return out

def gtrr(reg, ins):
    out = reg.copy()
    if reg[ins[1]] > reg[ins[2]]:
        out[ins[3]] = 1
    else:
        out[ins[3]] = 0
    return out

def eqir(reg, ins):
    out = reg.copy()
    if ins[1] == reg[ins[2]]:
        out[ins[3]] = 1
    else:
        out[ins[3]] = 0
    return out

def eqri(reg, ins):
    out = reg.copy()
    if reg[ins[1]] == ins[2]:
        out[ins[3]] = 1
    else:
        out[ins[3]] = 0
    return out

def eqrr(reg, ins):
    out = reg.copy()
    if reg[ins[1]] == reg[ins[2]]:
        out[ins[3]] = 1
    else:
        out[ins[3]] = 0
    return out


functions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

samples = []
sampleopcodes = []

num_part1 = 0

# scan input
with open('16.txt') as f:
    before = [-1,-1,-1,-1]
    while True:
        before = [int(x) for x in re.findall('\d',f.readline())]
        if len(before) < 4:
            break
        instruction = [int(x) for x in re.findall('\d+',f.readline())]
        after = [int(x) for x in re.findall('\d',f.readline())]
        f.readline() # whitespace
        outputs = [func(before, instruction) for func in functions]
        if outputs.count(after) >= 3:
            num_part1 += 1
        samples.append([x == after for x in outputs])
        sampleopcodes.append(instruction[0])

    print('Part 1:', num_part1)

    opcodes = dict()

    # part 2
    while len(opcodes) < 16:
        for i, sample in enumerate(samples):
            if sample.count(True) == 1:
                ind = sample.index(True)
                opcodes[sampleopcodes[i]] = functions[ind]
                # set to false ('easier' than delete)
                for sample in samples:
                    sample[ind] = False

    f.readline() # whitespace

    # run testprogram
    registers = [0,0,0,0]
    line = f.readline()
    while line:
        instruction = [int(x) for x in re.findall('\d+',line)]
        line = f.readline()
        func = opcodes[instruction[0]]
        registers = func(registers, instruction)

    print('Part 2:', registers[0])
