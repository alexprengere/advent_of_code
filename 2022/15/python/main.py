import sys
import re

_regex = re.compile(
    r"^Sensor at x=(-?\d+), y=(-?\d+):"
    " closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def manhattan(p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    return abs(x1 - x0) + abs(y1 - y0)


def has_possible_beacon(grid, p):
    return all(manhattan(sensor, p) > dist for sensor, dist in grid.items())


grid, beacons = {}, set()
for row in sys.stdin:
    sx, sy, bx, by = map(int, _regex.match(row).groups())
    grid[sx, sy] = manhattan((sx, sy), (bx, by))
    beacons.add((bx, by))


# PART 1
#
x_min, *_, x_max = sorted(sx for sx, _ in grid)
dist_max = max(grid.values())

x_range = range(x_min - dist_max, x_max + dist_max + 1)
y = 2_000_000
impossible = sum(
    not has_possible_beacon(grid, (x, y)) and (x, y) not in beacons
    for x in x_range
)
print(impossible)


# PART 2
#
MIN, MAX = 0, 4_000_000


def get_points_at_distance(p, dist):
    # Yields all points at distance dist of p.
    x, y = p
    if dist == 0:
        yield x, y
    else:
        for i in range(dist):
            yield x - dist + i, y + i
            yield x + i, y + dist - i
            yield x + dist - i, y - i
            yield x - i, y - dist + i


def get_candidates(grid):
    # Candidates are points exactly at "dist + 1" from a sensor
    for sensor, dist in grid.items():
        for nx, ny in get_points_at_distance(sensor, dist + 1):
            if MIN <= nx <= MAX and MIN <= ny <= MAX:
                yield nx, ny


for nx, ny in get_candidates(grid):
    if has_possible_beacon(grid, (nx, ny)):
        print(nx * 4_000_000 + ny)
        break
