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


total = 0
for cycle, X in run():
    if cycle % 40 == 20:
        total += cycle * X
print(total)
