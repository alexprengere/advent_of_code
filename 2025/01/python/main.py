import sys


def count_zeros(start, stop):
    # Dividing by 100 to count how many times we crossed a multiple of 100,
    # and adjusting for direction of movement: we add -1 when moving left to
    # adjust when we start exactly on zero.
    if stop > start:
        return stop // 100 - start // 100
    else:
        return (start - 1) // 100 - (stop - 1) // 100


_input = sys.stdin.readlines()

points_at_zero = 0
clicks_at_zero = 0
dial = 50

for row in _input:
    r, n = row[0], int(row[1:])
    if r == "R":
        new_dial = dial + n
    elif r == "L":
        new_dial = dial - n

    clicks_at_zero += count_zeros(dial, new_dial)
    dial = new_dial % 100
    if dial == 0:
        points_at_zero += 1

print(points_at_zero)
print(clicks_at_zero)
