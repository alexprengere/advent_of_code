import sys
from collections import defaultdict

grid = {}
for r, row in enumerate(sys.stdin):
    for c, cell in enumerate(row.rstrip()):
        grid[r, c] = cell


class UnionFind:
    """Generic implementation of the Union-Find algorithm."""

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def add(self, node):
        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0


def get_neighbors(r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yield (r + dr, c + dc)


def get_down_and_right_neighbors(r, c):
    yield (r + 1, c)
    yield (r, c + 1)


def find_garden_plots(grid):
    # This could very well be done using BFS for every point,
    # reaching every other point in the same plot, then removing
    # all those from an unvisited set, and repeating until that set
    # is empty. But I wanted to try out Union-Find!
    uf = UnionFind()

    for point in grid:
        uf.add(point)

    for point in grid:
        for n_point in get_down_and_right_neighbors(*point):
            if n_point in grid and grid[point] == grid[n_point]:
                uf.union(point, n_point)

    plots = defaultdict(list)
    for point in grid:
        plots[uf.find(point)].append(point)

    return plots


def area(plot):
    return len(plot)


def perimeter(plot):
    # For each point in the plot, check if one of its neighbors is not in the plot.
    # If not, we need to build a fence, so this counts as a perimeter.
    perimeter = 0
    for point in plot:
        for n_point in get_neighbors(*point):
            if n_point not in plot:
                perimeter += 1
    return perimeter


# PART 1
#
plots = find_garden_plots(grid)
print(sum(area(plot) * perimeter(plot) for plot in plots.values()))


# PART 2
#
# Triplets of corners indices including diagonals:
# UR = UP, UP+RIGHT, RIGHT
# RD = RIGHT, RIGHT+DOWN, DOWN
# DL = DOWN, DOWN+LEFT, LEFT
# LU = LEFT, LEFT+UP, UP
#
TRIPLETS = {
    "UR": ((-1, 0), (-1, 1), (0, 1)),
    "RD": ((0, 1), (1, 1), (1, 0)),
    "DL": ((1, 0), (1, -1), (0, -1)),
    "LU": ((0, -1), (-1, -1), (-1, 0)),
}


def get_corner_triplets(r, c):
    for triplet in TRIPLETS.values():
        yield [(r + dr, c + dc) for dr, dc in triplet]


def count_corners(plot, point):
    corners = 0
    for n1, n2, n3 in get_corner_triplets(*point):
        shape = n1 in plot, n2 in plot, n3 in plot
        #
        # Only 3 shapes of corners are possible, for example in the case of the LU,
        # assuming we are looking at the "A" point and its 1/2/3 neighbors:
        #
        #  2 | 3
        #  --+--
        #  1 | A
        #
        #  B | B
        #  --+--  => (0, 0, 0)
        #  B | A
        #
        #  A | B
        #  --+--  => (1, 0, 1)
        #  B | A
        #
        #  B | A
        #  --+--  => (0, 1, 0)
        #  A | A
        #
        if shape in {(0, 0, 0), (1, 0, 1), (0, 1, 0)}:
            corners += 1

    return corners


def count_sides(plot):
    # Counting the total number of corners is the same as counting the numbers of sides
    return sum(count_corners(plot, point) for point in plot)


print(sum(area(plot) * count_sides(plot) for plot in plots.values()))
