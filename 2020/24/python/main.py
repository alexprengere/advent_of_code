import sys
from collections import Counter

# In a E/NE coordinates system
#
DIRECTIONS = {
    "e": (1, 0),
    "se": (1, -1),
    "sw": (0, -1),
    "w": (-1, 0),
    "nw": (-1, 1),
    "ne": (0, 1),
}


def compute_coordinates(path):
    # Convert path to final E/NE coordinates
    # 1se = -1nw
    # 1sw = -1ne
    # 1w = -1e
    # 1nw = 1ne - 1e
    p = Counter(path)
    return (
        p["e"] - p["w"] - p["nw"] + p["se"],
        p["ne"] - p["sw"] + p["nw"] - p["se"],
    )


def neighbors(tile):
    x, y = tile
    for dx, dy in DIRECTIONS.values():
        yield x + dx, y + dy


def get_adjacent_white_tiles(black):
    white = set()
    for tile in black:
        for n in neighbors(tile):
            if n not in black:
                white.add(n)
    return white


def after_some_days(black, days):
    for _ in range(days):
        changes = {}
        # Rule #1
        for tile in black:
            black_neighbors = sum(n in black for n in neighbors(tile))
            if black_neighbors == 0 or black_neighbors > 2:
                changes[tile] = False
        # Rule #2
        for tile in get_adjacent_white_tiles(black):
            black_neighbors = sum(n in black for n in neighbors(tile))
            if black_neighbors == 2:
                changes[tile] = True

        for tile, status in changes.items():
            if status is True:
                black.add(tile)
            else:
                black.remove(tile)

    return black


# READING INPUT
#
PATHS = []
for row in sys.stdin:
    rest, path = "", []
    for c in row.rstrip():
        if rest + c in DIRECTIONS:
            path.append(rest + c)
            rest = ""
        else:
            rest = c
    PATHS.append((path))


# PART 1
#
flipped = Counter(compute_coordinates(path) for path in PATHS)
print(sum(f % 2 == 1 for f in flipped.values()))


# PART 2
#
black = set(coords for coords, f in flipped.items() if f % 2 == 1)
print(len(after_some_days(black, 100)))
