import sys
import itertools


def show(grid):
    x_min, *_, x_max = sorted(x for x, _ in grid)
    y_min, *_, y_max = sorted(y for _, y in grid)
    for y in range(y_min, y_max + 1):
        print(y, end=" ")
        for x in range(x_min, x_max + 1):
            print(grid.get((x, y), "."), end="")
        print()


def straight_line(p0, p1):
    x1, y1 = p1
    xi, yi = p0
    while (xi, yi) != p1:
        yield xi, yi
        xi += (x1 > xi) - (xi > x1)
        yi += (y1 > yi) - (yi > y1)
    yield p1


def get_sand_position(grid, source):
    y_max = max(y for _, y in grid)
    xs, ys = source
    while ys <= y_max:
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            next_s = xs + dx, ys + dy
            if grid.get(next_s) not in {"#", "o", "+"}:
                xs, ys = next_s
                break
        else:  # no break = sand is blocked
            return xs, ys
    else:  # ys > y_max
        return None


grid = {}
for row in sys.stdin:
    for p0, p1 in itertools.pairwise(row.split("->")):
        x0, y0 = map(int, p0.split(","))
        x1, y1 = map(int, p1.split(","))
        for p in straight_line((x0, y0), (x1, y1)):
            grid[p] = "#"


SOURCE = (500, 0)
grid[SOURCE] = "+"

for turn in itertools.count():
    sand = get_sand_position(grid, SOURCE)
    if sand is None:
        break
    grid[sand] = "o"

# show(grid)
print(turn)
