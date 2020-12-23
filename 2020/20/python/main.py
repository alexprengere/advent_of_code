import sys
import math
from itertools import chain
from collections import defaultdict


# Those small functions could be memoize with functools.lru_cache().
# But then we woud need to make tiles immutable.
#
def flip(tile):
    return ["".join(row) for row in zip(*tile)]


def rotate(tile):
    return ["".join(row) for row in zip(*tile[::-1])]


def rotations(tile):
    yield tile
    for _ in range(3):
        tile = rotate(tile)
        yield tile


def edges(tile, reverse=False):
    res = [
        tile[0],
        tile[-1],
        "".join(row[0] for row in tile),
        "".join(row[-1] for row in tile),
    ]
    if reverse:
        for edge in res[:]:
            res.append(edge[::-1])
    return set(res)


# For part 2
#
def orient_corner(corner, right, down):
    edges_r = edges(right, reverse=True)
    edges_d = edges(down, reverse=True)
    for corner in chain(rotations(corner), rotations(flip(corner))):
        corner_d = corner[-1]
        corner_r = "".join(row[-1] for row in corner)
        if corner_d in edges_d and corner_r in edges_r:
            return corner
    raise ValueError()


def orient_right(t1, t2):
    t1_r = "".join(row[-1] for row in t1)
    for t2 in chain(rotations(t2), rotations(flip(t2))):
        t2_l = "".join(row[0] for row in t2)
        if t2_l == t1_r:
            return t2
    raise ValueError()


def orient_down(t1, t2):
    t1_d = t1[-1]
    for t2 in chain(rotations(t2), rotations(flip(t2))):
        t2_u = t2[0]
        if t2_u == t1_d:
            return t2
    raise ValueError()


def mark_monster(image, x, y, monster):
    for (mx, my) in monster:
        px = x + mx
        py = y + my
        try:
            if image[py][px] != "#":
                return False, image
        except IndexError:  # monster would not fit
            return False, image
    # Never returned: MONSTER!
    for (mx, my) in monster:
        px = x + mx
        py = y + my
        image[py] = image[py][:px] + "O" + image[py][px + 1 :]
    return True, image


# READING INPUT
#
tiles = {}
tile_name, tile = None, None

for row in sys.stdin:
    row = row.rstrip()
    if row.startswith("Tile"):
        tile_name = int(row.split()[1].rstrip(":"))
        tile = []
    elif not row:  # end of tile
        tiles[tile_name] = tile
    else:
        tile.append(row)
if tile:
    tiles[tile_name] = tile

size = int(math.sqrt(len(tiles)))


# PART 1
#
matches = defaultdict(set)
for t1_name, t1 in tiles.items():
    for t2_name, t2 in tiles.items():
        if t1_name != t2_name:
            # Intersection of edges means that t1 and t2 can fit
            if edges(t1) & edges(t2, reverse=True):
                matches[t1_name].add(t2_name)
                matches[t2_name].add(t1_name)

# This condition is sufficient but not necessary.
corners = [t_name for t_name, matched in matches.items() if len(matched) == 2]
assert len(corners) == 4

product = 1
for corner in corners:
    product *= corner
print(product)


# PART 2
#
# Random corner placed, does not matter
puzzle = {0: corners[0]}
placed = {corners[0]}

# Placing tiles in the puzzle
#
for j in range(size - 1):
    for m in matches[puzzle[j * 1j]]:
        if m not in placed and len(matches[m]) < 4:
            puzzle[(j + 1) * 1j] = m
            placed.add(m)
            break

for i in range(size):
    for j in range(size):
        for m in matches[puzzle[i + j * 1j]] - placed:  # only 1
            puzzle[i + 1 + j * 1j] = m
            placed.add(m)
            break

for i in range(size):
    for j in range(size):
        print(puzzle.get(i + j * 1j, "...."), end=" ")
    print()


# Re-orienting tiles correctly
#
tiles[puzzle[0]] = orient_corner(
    tiles[puzzle[0]],
    tiles[puzzle[1j]],
    tiles[puzzle[1]],
)

for i in range(size):
    if i != 0:
        tiles[puzzle[i]] = orient_down(
            tiles[puzzle[i - 1]],
            tiles[puzzle[i]],
        )

    for j in range(size):
        if j != 0:
            tiles[puzzle[i + j * 1j]] = orient_right(
                tiles[puzzle[i + (j - 1) * 1j]],
                tiles[puzzle[i + j * 1j]],
            )

# Building full image
#
# [1:-1] is for cropping borders
image = []
for i in range(size):
    tmp = defaultdict(list)
    for j in range(size):
        tile_name = puzzle[i + j * 1j]
        for rn, row in enumerate(tiles[tile_name][1:-1]):
            tmp[rn].append(row[1:-1])
    for rn in sorted(tmp):
        image.append("".join(tmp[rn]))

MONSTER = [
    "                  #  ",
    "#    ##    ##    ### ",
    " #  #  #  #  #  #    ",
]

monster = set()
for y, line in enumerate(MONSTER):
    for x, char in enumerate(line):
        if char == "#":
            monster.add((x, y))

oriented = False
for image in chain(rotations(image), rotations(flip(image))):
    for x, _ in enumerate(image):
        for y, _ in enumerate(image):
            found, image = mark_monster(image, x, y, monster)
            if found:
                oriented = True
    if oriented:  # once a monster have been found, we stop the image rotations/flips
        break

print("\n".join(image))
print(sum(row.count("#") for row in image))
