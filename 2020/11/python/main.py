import sys


DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def get_adjacent_seats(seats, rn, sn):
    for i in (rn - 1, rn, rn + 1):
        if not 0 <= i < len(seats):
            continue
        for j in (sn - 1, sn, sn + 1):
            if not 0 <= j < len(seats[i]):
                continue
            if (i, j) != (rn, sn):
                yield seats[i][j]


def get_visible_seats(seats, rn, sn):
    for x_slope, y_slope in DIRECTIONS:
        v_rn, v_sn = rn, sn
        while True:
            v_rn += x_slope
            v_sn += y_slope
            if not 0 <= v_rn < len(seats):
                break
            if not 0 <= v_sn < len(seats[v_rn]):
                break
            if seats[v_rn][v_sn] != ".":
                yield seats[v_rn][v_sn]
                break


# PART 1: get_adjacent_seats & 4 occupied
# PART 2: get_visible_seats & 5 occupied
#
seats = []
for line in sys.stdin:
    seats.append(list(line.rstrip()))


while True:
    changes = {}

    for rn, row in enumerate(seats):
        for sn, seat in enumerate(row):
            visible = list(get_visible_seats(seats, rn, sn))
            if seat == "L":
                if all(v != "#" for v in visible):
                    changes[rn, sn] = "#"
            elif seat == "#":
                if sum(v == "#" for v in visible) >= 5:
                    changes[rn, sn] = "L"

    if not changes:
        break
    for (rn, sn), status in changes.items():
        seats[rn][sn] = status

print(sum(row.count("#") for row in seats))
