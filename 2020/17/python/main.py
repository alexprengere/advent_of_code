import sys
from itertools import product


# PART 1: without the 4th dimension
# PART 2
#
def neighbors(coordinates):
    # Not using the sum over a zip is actually 4x faster.
    x, y, z, w = coordinates
    for dx, dy, dz, dw in product([-1, 0, 1], repeat=4):
        if (dx, dy, dz, dw) != (0, 0, 0, 0):
            yield x + dx, y + dy, z + dz, w + dw


def get_adjacent_inactive_cubes(active):
    # This could be done more efficiently, but it works and it is simple.
    inactive = set()
    for coord in active:
        for n in neighbors(coord):
            if n not in active:
                inactive.add(n)
    return inactive


# We only track active cubes coordinates, that's it.
active = set()
for y, row in enumerate(sys.stdin):
    for x, status in enumerate(row.rstrip()):
        if status == "#":
            active.add((x, y, 0, 0))


TURNS = 6
for turn in range(TURNS):
    changes = {}
    # Rule #1
    for coord in active:
        active_neighbors = sum(n in active for n in neighbors(coord))
        if active_neighbors not in (2, 3):
            changes[coord] = False
    # Rule #2
    for coord in get_adjacent_inactive_cubes(active):
        active_neighbors = sum(n in active for n in neighbors(coord))
        if active_neighbors == 3:
            changes[coord] = True

    for coord, status in changes.items():
        if status is True:
            active.add(coord)
        else:
            active.remove(coord)

    print(1 + turn, len(active))
