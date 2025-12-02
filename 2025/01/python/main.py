import sys


_input = sys.stdin.readlines()

DIRECTIONS = {"R": 1, "L": -1}
SIZE = 100

dial = 50
points_at_zero = 0
crosses_zero = 0

for row in _input:
    prev_dial = dial
    direction, n = row[0], int(row[1:])
    shift = n * DIRECTIONS[direction]

    c, dial = divmod(dial + shift, SIZE)
    if dial == 0:
        points_at_zero += 1
    # The negative direction require some adjustments
    # * starting at 0 and going negative does not count as crossing zero
    # * ending at 0 is not already counted as crossing zero, so we add 1
    crosses_zero += abs(c)
    if shift < 0:
        if prev_dial == 0:
            crosses_zero -= 1
        if dial == 0:
            crosses_zero += 1

print(points_at_zero)
print(crosses_zero)
