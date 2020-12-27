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


def stabilize(seats, get_neighbors, limit):
    # Deep copying to not modify the input
    seats = [list(row) for row in seats]

    while True:
        changes = {}
        for rn, row in enumerate(seats):
            for sn, seat in enumerate(row):
                neighbors = list(get_neighbors(seats, rn, sn))
                if seat == "L":
                    if all(n != "#" for n in neighbors):
                        changes[rn, sn] = "#"
                elif seat == "#":
                    if sum(n == "#" for n in neighbors) >= limit:
                        changes[rn, sn] = "L"
        if not changes:
            break
        for (rn, sn), status in changes.items():
            seats[rn][sn] = status

    return sum(row.count("#") for row in seats)


# PART 1: get_adjacent_seats & 4 occupied
# PART 2: get_visible_seats & 5 occupied
#
seats = []
for line in sys.stdin:
    seats.append(list(line.rstrip()))

print(stabilize(seats, get_adjacent_seats, limit=4))
print(stabilize(seats, get_visible_seats, limit=5))
