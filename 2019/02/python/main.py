import sys


def run(code, noun, verb):
    code = code[:]
    code[1], code[2] = noun, verb
    pos = 0
    while pos < len(code):
        opcode = code[pos]
        if opcode == 1:
            p1, p2, p3 = code[pos + 1], code[pos + 2], code[pos + 3]
            code[p3] = code[p1] + code[p2]
            pos += 4
        elif opcode == 2:
            p1, p2, p3 = code[pos + 1], code[pos + 2], code[pos + 3]
            code[p3] = code[p1] * code[p2]
            pos += 4
        elif opcode == 99:
            break
    return code[0]


code = [int(i) for i in next(sys.stdin).split(",")]


# PART 1
#
print(run(code, 12, 2))


# PART 2
#
for noun in range(100):
    for verb in range(100):
        if run(code, noun, verb) == 19690720:
            print(100 * noun + verb)
            break
