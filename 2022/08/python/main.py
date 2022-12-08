import sys
import itertools


trees = {}
for r, line in enumerate(sys.stdin):
    for c, h in enumerate(line.rstrip()):
        trees[r, c] = [int(h), False]

R = 1 + max(r for r, _ in trees)
C = 1 + max(c for _, c in trees)

positions = list(itertools.product(range(R), range(C)))


def set_visibility_for_row(trees, r, columns):
    max_height_so_far = -1
    for c in columns:
        height, _ = trees[r, c]
        if height > max_height_so_far:
            max_height_so_far = height
            trees[r, c][1] = True


def set_visibility_for_col(trees, c, rows):
    max_height_so_far = -1
    for r in rows:
        height, _ = trees[r, c]
        if height > max_height_so_far:
            max_height_so_far = height
            trees[r, c][1] = True


for r in range(R):
    set_visibility_for_row(trees, r, range(C))
    set_visibility_for_row(trees, r, reversed(range(C)))


for c in range(C):
    set_visibility_for_col(trees, c, range(R))
    set_visibility_for_col(trees, c, reversed(range(R)))


# PART 1
#
print(sum(1 for p in positions if trees[p][1]))


# PART 2
#
DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]


def compute_scenic_score(trees, position):
    score = 1
    height, _ = trees[position]
    for dr, dc in DIRECTIONS:
        r, c = position
        r += dr
        c += dc
        distance = 0
        while 0 <= r < R and 0 <= c < C:
            h, _ = trees[r, c]
            distance += 1
            if h >= height:
                break
            r += dr
            c += dc
        score *= distance
    return score


print(max(compute_scenic_score(trees, p) for p in positions))
