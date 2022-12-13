import sys
from dataclasses import dataclass
from heapq import heappush, heappop


def dijkstra(graph, source):
    previous_nodes = {}  # to re-build the shortest known path
    shortest_dist = {node: sys.maxsize for node in graph}
    shortest_dist[source] = 0

    # This can be converted to a A* algorithm by inserting a heuristic
    # function when pushing / popping the heap.
    seen = set()
    heap = [(0, source)]
    while heap:
        dist_min_node, min_node = heappop(heap)
        seen.add(min_node)
        for neighbor, dist in graph[min_node].neighbors:
            if neighbor in seen:
                continue
            dist_neighbor = dist_min_node + dist
            if dist_neighbor < shortest_dist[neighbor]:
                shortest_dist[neighbor] = dist_neighbor
                previous_nodes[neighbor] = min_node
                heappush(heap, (dist_neighbor, neighbor))

    return previous_nodes, shortest_dist


@dataclass
class NodeData:
    height: int
    neighbors: list


graph = {}
for y, row in enumerate(sys.stdin):
    for x, elevation in enumerate(row.rstrip()):
        node = x, y
        if elevation == "S":
            elevation, source = "a", node
        elif elevation == "E":
            elevation, target = "z", node
        height = ord(elevation) - ord("a")
        graph[node] = NodeData(height=height, neighbors=[])


for node in graph:
    x, y = node
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_node = x + dx, y + dy
        if adj_node not in graph:
            continue
        # The condition is swapped on purpose here, as we will
        # go from target to source (useful for part 2)
        if graph[node].height <= graph[adj_node].height + 1:
            graph[node].neighbors.append((adj_node, 1))


# PART 1
#
_, shortest_dist = dijkstra(graph, target)
print(shortest_dist[source])


# PART 2
#
sources = [node for node in graph if graph[node].height == 0]
print(min(shortest_dist[node] for node in sources))
