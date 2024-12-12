import sys
import itertools
from collections import defaultdict

data = sys.stdin.read().splitlines()

ROWS = len(data)
COLS = len(data[0])

antennas = defaultdict(set)
for r, row in enumerate(data):
    for c, cell in enumerate(row):
        if cell != ".":
            antennas[cell].add(complex(c, r))


def in_bounds(point):
    return 0 <= point.imag < ROWS and 0 <= point.real < COLS


# PART 1
#
antinodes = set()
for _, coords in antennas.items():
    for a, b in itertools.combinations(coords, 2):
        vector = b - a
        for point in [a - vector, b + vector]:
            if in_bounds(point):
                antinodes.add(point)

print(len(antinodes))


# PART 2
#
antinodes = set()
for _, coords in antennas.items():
    for a, b in itertools.combinations(coords, 2):
        vector = b - a
        for point, direction in [(a, -1), (b, +1)]:
            while in_bounds(point):
                antinodes.add(point)
                point += vector * direction

print(len(antinodes))
