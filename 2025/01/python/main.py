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
    crosses_zero += abs(c)
    if dial == 0:
        points_at_zero += 1
    # The negative direction require some adjustments
    # A) starting at 0 and going negative does not count as crossing zero
    # B) ending at 0 is not already counted as crossing zero, so we add 1:
    #    99 // 100 =>  0: OK, 0 crossing
    #   100 // 100 =>  1: OK, 1 crossing
    #   -99 // 100 => -1: OK, 1 crossing (assuming start > 0)
    #  -100 // 100 => -1: not OK, as we actually cross twice
    if shift < 0:
        if prev_dial == 0:
            crosses_zero -= 1  # case A
        if dial == 0:
            crosses_zero += 1  # case B

print(points_at_zero)
print(crosses_zero)
