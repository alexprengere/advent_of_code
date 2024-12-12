import sys
from collections import defaultdict

data = sys.stdin.read().splitlines()

ROWS = len(data)
COLS = len(data[0])

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


grid = {}
blocks = set()
for r, row in enumerate(data):
    for c, cell in enumerate(row):
        point = c, r
        if cell == ".":
            blocks.add(point)
        else:
            grid[point] = int(cell)


def get_neighbors(c, r):
    for dc, dr in NEIGHBORS:
        n_point = nc, nr = c + dc, r + dr
        if n_point not in blocks:
            if 0 <= nc < COLS and 0 <= nr < ROWS:
                yield n_point


SOURCE, TARGET = 0, 9

start_points = [p for p, value in grid.items() if value == SOURCE]


# PART 1
#
def compute_score(start_point):
    stack = [start_point]
    visited = set()
    while stack:
        point = stack.pop()
        visited.add(point)
        for n_point in get_neighbors(*point):
            if n_point in visited:
                continue
            if grid[n_point] - grid[point] == 1:
                stack.append(n_point)

    return len([p for p in visited if grid[p] == TARGET])


print(sum(compute_score(p) for p in start_points))


# PART 2
#
def compute_rating(start_point):
    stack = [start_point]
    ratings = defaultdict(int)
    while stack:
        point = stack.pop()
        for n_point in get_neighbors(*point):
            if grid[n_point] - grid[point] == 1:
                ratings[n_point] += 1
                stack.append(n_point)

    return sum(ratings[p] for p in ratings if grid[p] == TARGET)


print(sum(compute_rating(p) for p in start_points))
