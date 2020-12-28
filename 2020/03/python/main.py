import sys
import operator
from functools import reduce

DIRECTIONS = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def compute_trees_encountered(data, y_slope, x_slope):
    width = len(data[0])
    total_trees = 0
    x, y = 0, 0
    while x < len(data):
        if data[x][y % width] == "#":
            total_trees += 1
        x += x_slope
        y += y_slope
    return total_trees


data = []
for row in sys.stdin:
    data.append(row.strip())

trees = {slope: compute_trees_encountered(data, *slope) for slope in DIRECTIONS}

print(trees[3, 1])
print(reduce(operator.mul, trees.values(), 1))
