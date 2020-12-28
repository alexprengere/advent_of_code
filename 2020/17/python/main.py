import sys
from itertools import product


def neighbors(coordinates, dim):
    # We could have written a more generic code here.
    # But not using the sum over a zip is actually 4x faster.
    if dim == 3:
        x, y, z = coordinates
        for dx, dy, dz in product([-1, 0, 1], repeat=3):
            if (dx, dy, dz) != (0, 0, 0):
                yield x + dx, y + dy, z + dz
    elif dim == 4:
        x, y, z, w = coordinates
        for dx, dy, dz, dw in product([-1, 0, 1], repeat=4):
            if (dx, dy, dz, dw) != (0, 0, 0, 0):
                yield x + dx, y + dy, z + dz, w + dw


def get_adjacent_inactive_cubes(active, dim):
    # This could be done more efficiently, but it works and it is simple.
    inactive = set()
    for coord in active:
        for n in neighbors(coord, dim):
            if n not in active:
                inactive.add(n)
    return inactive


def run_cycles(active, dim, cycles):
    for _ in range(cycles):
        changes = {}
        # Rule #1
        for coord in active:
            active_neighbors = sum(n in active for n in neighbors(coord, dim))
            if active_neighbors not in (2, 3):
                changes[coord] = False
        # Rule #2
        for coord in get_adjacent_inactive_cubes(active, dim):
            active_neighbors = sum(n in active for n in neighbors(coord, dim))
            if active_neighbors == 3:
                changes[coord] = True

        for coord, status in changes.items():
            if status is True:
                active.add(coord)
            else:
                active.remove(coord)

    return active


# PART 1: 3D
# PART 2: 4D
#
rows = list(sys.stdin)

for dim in (3, 4):
    # We only track active cubes coordinates, that's it.
    active = set()
    for y, row in enumerate(rows):
        for x, status in enumerate(row.rstrip()):
            if status == "#":
                if dim == 3:
                    active.add((x, y, 0))
                elif dim == 4:
                    active.add((x, y, 0, 0))

    print(len(run_cycles(active, dim=dim, cycles=6)))
