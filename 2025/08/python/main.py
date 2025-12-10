import os
import sys
import math
import heapq
from itertools import combinations
from collections import Counter
from typing import NamedTuple

PART_1_N = int(os.getenv("PART_1_N", "1000"))


class Point(NamedTuple):
    x: int
    y: int
    z: int


class UnionFind:
    """Generic implementation of the Union-Find algorithm."""

    def __init__(self):
        self.parent = {}
        self.rank = {}
        # This parameter is not part of a generic implementation
        # of Union-Find, but is useful for this specific problem.
        # We use it to track the number of disjoint sets.
        self.disjoint_sets_count = 0

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
            # As we just merged two disjoint sets, we decrease the count.
            self.disjoint_sets_count -= 1

    def add(self, node):
        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0
            # When adding a new node, we have one more disjoint set,
            # as it is initially in its own set.
            self.disjoint_sets_count += 1


def dist(pair):
    p0, p1 = pair
    return (p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2 + (p0.z - p1.z) ** 2


# We technically don't need to store the grid as a set, as it is also stored in the
# Union-Find structure. However, it makes the code clearer, as Union-Find is not
# supposed to expose anything other than union/find/add operations.
grid = set()
uf = UnionFind()
for row in sys.stdin.readlines():
    point = Point(*map(int, row.split(",")))
    grid.add(point)
    uf.add(point)

# We only need relative distances, so we use `dist` which skips the square root.
# Apparently there are better algorithms to find the closest pairs of points.
# but given the input size, this brute-force approach is sufficient.
sorted_points_pair = sorted(combinations(grid, r=2), key=dist)


# PART 1
#
step = 0
while step < PART_1_N:  # 1_000 for the real input, 10 for the example
    p0, p1 = sorted_points_pair[step]
    uf.union(p0, p1)
    step += 1

assert step == PART_1_N
circuits = Counter()  # circuit 'root' -> circuit size
for point in grid:
    circuits[uf.find(point)] += 1

print(math.prod(heapq.nlargest(3, circuits.values())))


# PART 2
#
# This is basically Kruskal's algorithm to find the Minimum Spanning Tree, except
# the problem is not asking for the MST itself, but just to continue adding edges,
# regardless of the cycle they create, until all points are connected.
while uf.disjoint_sets_count > 1:
    p0, p1 = sorted_points_pair[step]
    uf.union(p0, p1)
    step += 1

print(p0.x * p1.x)  # last union operation that connected all points
