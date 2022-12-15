import sys
import re

_regex = re.compile(
    "Sensor at x=([0-9-]+), y=([0-9-]+):"
    " closest beacon is at x=([0-9-]+), y=([0-9-]+)"
)


def manhattan(p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    return abs(x1 - x0) + abs(y1 - y0)


def possible(grid, p):
    return all(manhattan(sensor, p) > dist for sensor, dist in grid.items())


grid, beacons = {}, set()
for row in sys.stdin:
    sx, sy, bx, by = map(int, _regex.match(row).groups())
    grid[sx, sy] = manhattan((sx, sy), (bx, by))
    beacons.add((bx, by))


x_min, *_, x_max = sorted(sx for sx, _ in grid)
dist_max = max(grid.values())


# PART 1
#
x_range = range(x_min - dist_max, x_max + dist_max + 1)
y = 2_000_000
impossible = sum(
    (x, y) not in beacons and not possible(grid, (x, y)) for x in x_range
)
print(impossible)


# PART 2
#
MIN, MAX = 0, 4_000_000

for x in range(MIN, MAX + 1):
    print(x)
    for y in range(MIN, MAX + 1):
        if possible(grid, (x, y)):
            print(x * 4_000_000 + y)
            break
