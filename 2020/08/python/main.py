import sys


def run(program):
    seen = set()
    corrupted = False
    accumulator = 0
    pos = 0
    while pos < len(program):
        if pos in seen:
            corrupted = True
            break
        seen.add(pos)
        cmd, value = program[pos]
        if cmd == "nop":
            pos += 1
        elif cmd == "acc":
            accumulator += value
            pos += 1
        elif cmd == "jmp":
            pos += value
    return corrupted, accumulator


program = []
for row in sys.stdin:
    cmd, value = row.rstrip().split()
    program.append((cmd, int(value)))


# PART 1
#
print(run(program))


# PART 2
#
for pos, (cmd, value) in enumerate(program):
    if cmd == "nop":
        fixed_program = program.copy()
        fixed_program[pos] = ("jmp", value)
    elif cmd == "jmp":
        fixed_program = program.copy()
        fixed_program[pos] = ("nop", value)
    else:
        continue

    corrupted, accumulator = run(fixed_program)
    if not corrupted:
        print(pos, cmd, accumulator)
