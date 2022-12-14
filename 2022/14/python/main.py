import sys
import itertools


def straight_line(p0, p1):
    x1, y1 = p1
    xi, yi = p0
    while (xi, yi) != p1:
        yield xi, yi
        xi += (x1 > xi) - (xi > x1)
        yi += (y1 > yi) - (yi > y1)
    yield p1


class OverflowingSand(Exception):
    pass


def get_sand_position(grid, source, bottom, bottom_blocks=False):
    xs, ys = source
    while ys <= bottom:
        for dx in (0, -1, 1):
            next_xs = xs + dx
            next_ys = ys + 1
            value = grid.get((next_xs, next_ys), ".")
            blocked = (next_ys == bottom and bottom_blocks) or value in "#o"
            if not blocked:
                xs, ys = next_xs, next_ys
                break
        else:  # no break = sand is blocked
            return xs, ys
    raise OverflowingSand()


SOURCE = (500, 0)
grid = {SOURCE: "+"}

for row in sys.stdin:
    for p0, p1 in itertools.pairwise(row.split("->")):
        x0, y0 = map(int, p0.split(","))
        x1, y1 = map(int, p1.split(","))
        for p in straight_line((x0, y0), (x1, y1)):
            grid[p] = "#"

y_max = max(y for _, y in grid)

for turn in itertools.count(1):
    try:
        sand = get_sand_position(
            grid,
            SOURCE,
            bottom=y_max,
            bottom_blocks=False,
        )
    except OverflowingSand:
        print(turn - 1)  # -1 because we want the turn before overflow
        break
    else:
        grid[sand] = "o"

for turn in itertools.count(turn):
    sand = get_sand_position(
        grid,
        SOURCE,
        bottom=y_max + 2,
        bottom_blocks=True,
    )
    if sand == SOURCE:
        print(turn)
        break
    grid[sand] = "o"
