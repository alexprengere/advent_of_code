import sys
import itertools

grid = sys.stdin.read().splitlines()

ROWS = len(grid)
COLS = len(grid[0])


def horizontals(grid):
    yield from grid


def verticals(grid):
    for column in zip(*grid):
        yield "".join(column)


def diagonals(grid):
    # Up and Down diagonals starting from the first column on the left
    for r in range(ROWS):
        yield "".join(grid[r + c][c] for c in range(min(ROWS - r, COLS - r)))
        yield "".join(grid[r - c][c] for c in range(r + 1))

    # Up and Down diagonals starting from the last column on the right
    # The range starts at 1 and goes to ROWS - 1 because the first and last
    # diagonals were already covered
    for r in range(1, ROWS - 1):
        yield "".join(grid[r + c][-c - 1] for c in range(min(ROWS - r, COLS - r)))
        yield "".join(grid[r - c][-c - 1] for c in range(r + 1))


# PART 1
#
print(
    sum(
        s.count("XMAS") + s.count("SAMX")  # faster than using s[::-1] :)
        for s in itertools.chain(
            horizontals(grid),
            verticals(grid),
            diagonals(grid),
        )
    )
)


# PART 2
#
GRID_INDICES = list(itertools.product(range(ROWS), range(COLS)))
CROSS_INDICES = [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)]
XMAS = {
    "MSAMS",
    "SMASM",
    "SSAMM",
    "MMASS",
}


def cross(grid, r, c):
    return "".join(
        grid[r + dr][c + dc]
        for dr, dc in CROSS_INDICES
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS
    )


print(sum(cross(grid, r, c) in XMAS for r, c in GRID_INDICES))
