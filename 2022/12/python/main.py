import sys
from dataclasses import dataclass


def dijkstra_algorithm(graph, source):
    # Cost of visiting each node and update it as we move along the graph
    shortest_dist = {node: sys.maxsize for node in graph}
    shortest_dist[source] = 0

    # This dict saves the shortest known path to a node found so far
    previous_nodes = {}

    # The algorithm executes until we visit all nodes
    unvisited_nodes = list(graph)
    while unvisited_nodes:
        min_node = min(unvisited_nodes, key=lambda n: shortest_dist[n])

        # The code block below retrieves the current node's neighbors
        # and updates their distances & best path
        for neighbor, dist in graph[min_node].neighbors:
            dist_from_min_node = shortest_dist[min_node] + dist
            if dist_from_min_node < shortest_dist[neighbor]:
                shortest_dist[neighbor] = dist_from_min_node
                previous_nodes[neighbor] = min_node

        unvisited_nodes.remove(min_node)

    return previous_nodes, shortest_dist


Node = tuple[int, int]
Distance = int


@dataclass
class NodeData:
    height: int
    neighbors: list[tuple[Node, Distance]]


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
        if graph[adj_node].height <= graph[node].height + 1:
            graph[node].neighbors.append((adj_node, 1))


_, shortest_dist = dijkstra_algorithm(graph, source)
print(shortest_dist[target])
