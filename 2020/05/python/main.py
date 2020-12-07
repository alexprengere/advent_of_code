import sys


seats = set()

for line in sys.stdin:
    line = line.strip()

    row = 0
    for cn, c in enumerate(line[:7]):
        if c == "B":
            row += 2 ** (6 - cn)

    col = 0
    for cn, c in enumerate(line[7:]):
        if c == "R":
            col += 2 ** (2 - cn)

    seat_id = 8 * row + col
    seats.add(seat_id)


for i in range(max(seats) + 1):
    if i not in seats:
        print(i)
