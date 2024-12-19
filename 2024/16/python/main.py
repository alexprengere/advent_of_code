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
    # Returns neighbors of a node with their distance, in this
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
# with the same distance. This is because we want to backtrack from the end to
# the start, and go through all possible paths matching the minimum distance.
# We do not go for the A* algorithm, as it would not changed much in this case,
# I tried it :). Due to the maze shape, A* heuristics are not very useful.
start_dir = (1, 0)
source = (start, start_dir)
shortest_dist = {source: 0}
previous_nodes = defaultdict(list)  # node -> [previous_node, ...]

# We want to record all the 'end' nodes that have the minimum distance to reach the
# end position. In theory there might be multiple directions to reach the end node
# with the same distance. In practive with AoC input, there was only one.
dist_min_to_end = None
end_nodes_with_min_dist = []

seen = set()
heap = [(0, source)]
while heap:
    dist_min_node, min_node = heappop(heap)
    seen.add(min_node)

    min_point, _ = min_node
    if min_point == end:
        # Reaching the end means we can break early, but only if we have
        # exceeded the minimum distance to reach the end node. There can be
        # multiple path to the end node with the same distance. We only want
        # to keep the ones that have the minimum distance.
        if dist_min_to_end is None:
            dist_min_to_end = dist_min_node
        elif dist_min_node > dist_min_to_end:
            break  # not interested in non-optimal paths to 'end'
        end_nodes_with_min_dist.append(min_node)

    for dist, neighbor in get_neighbors(min_node, walls):
        if neighbor in seen:
            continue
        dist_neighbor = dist_min_node + dist
        # This is not the standard Dijkstra algorithm, where you would only
        # keep the previous neighbor that has the shortest distance.
        shortest_dist_neighbor = shortest_dist.get(neighbor, math.inf)
        if dist_neighbor < shortest_dist_neighbor:
            previous_nodes[neighbor] = [min_node]
            shortest_dist[neighbor] = dist_neighbor
            heappush(heap, (dist_neighbor, neighbor))
        elif dist_neighbor == shortest_dist_neighbor:
            previous_nodes[neighbor].append(min_node)


# PART 1
#
# Just showing the minimum cost to reach the end node
print(dist_min_to_end)


# PART 2
#
# We need to backtrack from the end to the start, and go through all possible paths.
stack = [*end_nodes_with_min_dist]
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
