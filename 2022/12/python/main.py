import sys
from dataclasses import dataclass


def dijkstra_algorithm(graph, source):
    shortest_dist = {node: sys.maxsize for node in graph}
    shortest_dist[source] = 0

    previous_nodes = {}  # to re-build the shortest known path

    unvisited_nodes = list(graph)
    while unvisited_nodes:
        min_node = min(unvisited_nodes, key=lambda n: shortest_dist[n])

        for neighbor, dist in graph[min_node].neighbors:
            dist_from_min_node = shortest_dist[min_node] + dist
            if dist_from_min_node < shortest_dist[neighbor]:
                shortest_dist[neighbor] = dist_from_min_node
                previous_nodes[neighbor] = min_node

        unvisited_nodes.remove(min_node)

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
_, shortest_dist = dijkstra_algorithm(graph, target)
print(shortest_dist[source])


# PART 2
#
print(min(shortest_dist[node] for node in graph if graph[node].height == 0))
