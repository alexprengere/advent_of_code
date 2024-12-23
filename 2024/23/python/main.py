import sys
from collections import defaultdict

graph = defaultdict(set)

for row in sys.stdin:
    u, v = row.rstrip().split("-")
    graph[u].add(v)
    graph[v].add(u)


def expand(graph, start_nodes, size=None):
    # This function takes a list of start nodes, and put each one into its
    # own clique. The we iteratively attempt to grow each clique by seeing
    # if any of its members neighbors is fully interconnected with the rest.
    # We stop when the cliques are no longer growing.
    if size is None:
        size = len(graph)

    cliques = {frozenset({node}) for node in start_nodes}

    for _ in range(size - 1):
        next_cliques = set()
        for clique in cliques:
            clique_neighbors = set()
            for node in clique:
                clique_neighbors |= graph[node]
            for neighbor in clique_neighbors - clique:
                # Here we could check if "clique | {neighbor}" is already
                # in new_cliques and skip the check, but it ends up slower
                if graph[neighbor].issuperset(clique):
                    next_cliques.add(clique | {neighbor})
        if not next_cliques:
            break
        cliques = next_cliques

    return cliques


# PART 1
#
t_nodes = [node for node in graph if node.startswith("t")]

cliques_3 = expand(graph, t_nodes, size=3)
print(len(cliques_3))


# PART 2 (OBSOLETE)
#
# We set remaining_nodes to the whole set of nodes.
# We expand a random node until we reach the biggest cliques from
# that node, then we record the biggest clique size, and remove all
# nodes from those cliques from the remaining_nodes set.
# Then we repeat the process until remaining_nodes is empty, this avoids
# expanding nodes that will lead to the same cliques.
#
def find_biggest_clique(graph):
    remaining_nodes = set(graph)

    clique_max = None
    clique_max_size = 0

    while remaining_nodes:
        node = remaining_nodes.pop()
        for clique in expand(graph, [node]):
            if len(clique) > clique_max_size:
                clique_max_size = len(clique)
                clique_max = clique
            remaining_nodes -= clique

    return clique_max


# This runs in about 1s, but the Bron-Kerbosch algorithm is much faster,
# and runs in a few ms.
# clique_max = find_biggest_clique(graph)
# print(",".join(sorted(clique_max)))


# ACTUAL PART 2
#
# For posterity, here is the optimal algorithm to find the biggest
# clique in a graph. I would never have come up with it myself :)
def bron_kerbosch(graph, r, p, x):
    def degree(node):
        return len(graph[node])

    if len(p) == 0 and len(x) == 0:
        yield r
    else:
        pivot = max(p | x, key=degree)
        for v in p - graph[pivot]:
            neighbours = graph[v]
            yield from bron_kerbosch(
                graph,
                r | {v},
                p & neighbours,
                x & neighbours,
            )
            p.remove(v)
            x.add(v)


clique_max = max(
    bron_kerbosch(
        graph,
        set(),
        set(graph),
        set(),
    ),
    key=len,
)
print(",".join(sorted(clique_max)))
