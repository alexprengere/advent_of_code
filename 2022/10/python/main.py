import sys


def run():
    X = 1
    cycle = 0
    for row in sys.stdin:
        row = row.rstrip().split()
        if row[0] == "noop":
            cycle += 1
            yield cycle, X
        elif row[0] == "addx":
            for _ in range(2):
                cycle += 1
                yield cycle, X
            _, n = row
            X += int(n)


execution = list(run())


# PART 1
#
total = 0
for cycle, X in execution:
    if cycle % 40 == 20:
        total += cycle * X
print(total)


# PART 2
#
for cycle, X in execution:
    crt_position = (cycle - 1) % 40
    if X - 1 <= crt_position <= X + 1:
        print("#", end="")
    else:
        print(" ", end="")
    if crt_position == 39:
        print()
