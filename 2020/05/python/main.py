import sys


def compute_seat_id(data):
    row = 0
    for cn, c in enumerate(data[:7]):
        if c == "B":
            row += 2 ** (6 - cn)

    col = 0
    for cn, c in enumerate(data[7:]):
        if c == "R":
            col += 2 ** (2 - cn)

    return row * 8 + col


seats = set(compute_seat_id(line.rstrip()) for line in sys.stdin)


# PART 1
#
print(max(seats))


# PART 2
#
for i in reversed(range(max(seats) + 1)):
    if i not in seats:
        print(i)
        break
