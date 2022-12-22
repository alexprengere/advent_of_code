import sys

INDICES = [
    (+1, +0, +0),
    (-1, +0, +0),
    (+0, +1, +0),
    (+0, -1, +0),
    (+0, +0, +1),
    (+0, +0, -1),
]


def neighbors(x, y, z):
    for dx, dy, dz in INDICES:
        yield x + dx, y + dy, z + dz


def surface(points):
    exposed = 0
    for point in points:
        exposed += sum(n not in points for n in neighbors(*point))
    return exposed


lava = set()
for row in sys.stdin:
    lava.add(tuple(int(n) for n in row.split(",")))


# PART 1
#
print(surface(lava))


# PART 2
#
x_min, *_, x_max = sorted(x for x, _, _ in lava)
y_min, *_, y_max = sorted(y for _, y, _ in lava)
z_min, *_, z_max = sorted(z for _, _, z in lava)

grid = {
    (x, y, z)
    for x in range(x_min - 1, x_max + 2)
    for y in range(y_min - 1, y_max + 2)
    for z in range(z_min - 1, z_max + 2)
}
assert min(grid) not in lava

stack = [min(grid)]
reachable = set()
while stack:
    point = stack.pop()
    reachable.add(point)
    for n in neighbors(*point):
        # 1. Test that n is not going out of bounds
        # 2. If point is lava, we cannot reach its neighbors
        # 3. Test that we do not process same n multiple times
        if n in grid and n not in lava and n not in reachable:
            stack.append(n)

interior = grid - reachable - lava
print(surface(lava | interior))  # same as surface(lava) - surface(interior)
