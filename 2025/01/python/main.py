import sys


def move(start, shift):
    crosses, dial = divmod(start + shift, 100)
    crosses = abs(crosses)
    if shift < 0:
        # The negative direction require some adjustments
        # * starting at 0 and going negative does not count as crossing zero
        # * ending at 0 is not already counted as crossing zero, so we add 1
        if start == 0:
            crosses -= 1
        if dial == 0:
            crosses += 1
    return crosses, dial


_input = sys.stdin.readlines()

DIRECTIONS = {"R": 1, "L": -1}
points_at_zero = 0
crosses_zero = 0
dial = 50

for row in _input:
    direction, n = row[0], int(row[1:])
    if direction == "R":
        shift = n
    elif direction == "L":
        shift = -n

    crosses, dial = move(dial, n * DIRECTIONS[direction])
    crosses_zero += crosses
    if dial == 0:
        points_at_zero += 1

print(points_at_zero)
print(crosses_zero)
