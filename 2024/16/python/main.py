import sys
import math
from heapq import heappop, heappush
from collections import defaultdict

_input = sys.stdin.read().splitlines()

HEIGHT = len(_input)
WIDTH = len(_input[0])

start, end = None, None
walls = set()

for y, row in enumerate(_input):
    for x, cell in enumerate(row):
        point = (x, y)
        if cell == "#":
            walls.add(point)
        elif cell == "S":
            start = point
        elif cell == "E":
            end = point

assert start is not None
assert end is not None


def show(path):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            point = (x, y)
            if point in walls:
                print("#", end="")
            elif point in path:
                print("O", end="")
            else:
                print(".", end="")
        print()


def get_neighbors(node, walls):
    # Returns neighbors of a node with their cost, in this
    # context, a node is a tuple of (point, direction)
    (x, y), (dx, dy) = node

    # First neighbor is just moving forward
    nx, ny = (x + dx, y + dy)
    if (nx, ny) not in walls:
        yield 1, ((nx, ny), (dx, dy))

    # Second/third neighbors are left/right rotations
    yield 1000, ((x, y), (-dy, dx))
    yield 1000, ((x, y), (dy, -dx))


# This is a pretty standard Dijkstra algorithm, with the only difference
# being that we track in previous_nodes all the nodes that can reach a node
# with the same cost. This is because we want to backtrack from the end to the
# start, and go through all possible paths.
start_dir = (1, 0)
source = (start, start_dir)
shortest_dist = {source: 0}
previous_nodes = defaultdict(list)  # node -> [previous_node, ...]

seen = set()
heap = [(0, source)]
while heap:
    dist_min_node, min_node = heappop(heap)
    seen.add(min_node)

    for dist, neighbor in get_neighbors(min_node, walls):
        if neighbor in seen:
            continue
        dist_neighbor = dist_min_node + dist
        # This is not the standard Dijkstra algorithm, where you would only
        # keep the previous neighbor that has the shortest distance.
        shortest_dist_neighbor = shortest_dist.get(neighbor, math.inf)
        if dist_neighbor <= shortest_dist_neighbor:
            if dist_neighbor < shortest_dist_neighbor:
                previous_nodes[neighbor] = [min_node]
                shortest_dist[neighbor] = dist_neighbor
            else:
                previous_nodes[neighbor].append(min_node)
            heappush(heap, (dist_neighbor, neighbor))

# After the Dijkstra algorithm, we have the shortest distance to all nodes,
# now we need to find the shortest path to the end node. We need to loop
# through all the nodes and find those whose position is 'end', as there
# can be multiple directions as well.
min_cost = math.inf
for node, cost in shortest_dist.items():
    point, _ = node
    if point == end and cost < min_cost:
        min_cost = cost

# PART 1
#
# Just showing the minimum cost to reach the end node
print(min_cost)


# PART 2
#
# We need to backtrack from the end to the start, and go through all possible paths.
# First we need to find all the nodes that have the minimum cost to reach the end node.
# In theory there might be multiple directions to reach the end node with the same cost.
# In practive with AoC input, there was only one.
min_cost_end_nodes = []
for node, cost in shortest_dist.items():
    point, _ = node
    if point == end and cost == min_cost:
        min_cost_end_nodes.append(node)


stack = [*min_cost_end_nodes]
seen = set()
while stack:
    node = stack.pop()
    seen.add(node)
    for prev_node in previous_nodes[node]:
        if prev_node not in seen:
            stack.append(prev_node)

seats = {point for point, _ in seen}
print(len(seats))
# show(seats)
