import sys
import math
from heapq import heappop, heappush

falling = {}
for n, row in enumerate(sys.stdin, start=1):
    x, y = map(int, row.split(","))
    falling[x, y] = n


START = 0, 0
EXIT = 70, 70
SIZE = 71


def get_neighbors(node, fallen):
    x, y = node

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = (x + dx, y + dy)
        if (nx, ny) in fallen:
            continue
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            yield nx, ny


def find_steps_to_reach_exit(N):
    fallen = {point for point, n in falling.items() if n <= N}

    # This is a pretty standard Dijkstra algorithm, except we do not even
    # keep the previous nodes. A* would *not* be a better choice, because of
    # the up/down/left/right movements, we cannot go diagonally to the exit.
    shortest_dist = {START: 0}

    seen = set()
    heap = [(0, START)]
    while heap:
        dist_min_node, min_node = heappop(heap)
        seen.add(min_node)

        if min_node == EXIT:
            return dist_min_node

        for neighbor in get_neighbors(min_node, fallen):
            if neighbor in seen:
                continue
            dist_neighbor = dist_min_node + 1
            if dist_neighbor < shortest_dist.get(neighbor, math.inf):
                shortest_dist[neighbor] = dist_neighbor
                heappush(heap, (dist_neighbor, neighbor))

    return None


# PART 1
#
print(find_steps_to_reach_exit(1024))


# PART 2
#
n_min = 1024 + 1  # we know that the path is not blocked before this step
n_max = max(falling.values())  # last byte to fall

# Find the first step where the path is blocked using binary search
while n_min < n_max:
    n = (n_min + n_max) // 2
    if find_steps_to_reach_exit(n) is None:
        n_max = n
    else:
        n_min = n + 1

for point, n in falling.items():
    if n == n_min:  # n_min == n_max here
        x, y = point
        print(f"{x},{y}")
