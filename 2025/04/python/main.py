import sys
import itertools


D_INDICES = set(itertools.product((-1, 0, 1), repeat=2))


def neighbors(x, y):
    for dx, dy in D_INDICES:
        if (dx, dy) != (0, 0):
            yield (x + dx, y + dy)


_input = sys.stdin.readlines()
ROWS = len(_input)
COLS = len(_input[0].rstrip())

grid = set()
for y, row in enumerate(_input):
    for x, value in enumerate(row.rstrip()):
        if value == "@":
            grid.add((x, y))


def draw_grid(grid, reachable):
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in reachable:
                print("x", end="")

            elif (x, y) in grid:
                print("@", end="")
            else:
                print(".", end="")
        print()


reachable = set()
for point in grid:
    total = sum(neigh in grid for neigh in neighbors(*point))
    if total < 4:
        reachable.add(point)

print(len(reachable))
