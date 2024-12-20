import sys

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


def get_neighbors(node):
    x, y = node
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            yield nx, ny


def get_points_at_max_dist(node, max_dist):
    # Get all points at a manhattan distance of at most max_dist from node
    x, y = node
    for d in range(1, 1 + max_dist):
        for dx in range(max(-d, -x), min(d + 1, WIDTH - x)):
            dy = d - abs(dx)
            if 0 <= y + dy < HEIGHT:
                yield d, (x + dx, y + dy)
            if dy > 0 and 0 <= y - dy < HEIGHT:
                yield d, (x + dx, y - dy)


# Note that Dijkstra's algorithm is not needed here, since there is *only*
# one possible path from the start to the end, so we use a simple DFS.
path = []

seen = set()
stack = [start]
while stack:
    node = stack.pop()
    seen.add(node)
    path.append(node)

    for neighbor in get_neighbors(node):
        if neighbor not in seen and neighbor not in walls:
            stack.append(neighbor)

# We want to be able to tell the distance from any node to the end,
# so that when we are evaluating the gain of a cheat, we can just
# check if the end of the cheat is much closer to the end than the
# start of the cheat.
# As we have the path from start to end, and there is only one path,
# the distance from any node to the end is just their position.
dist_to_end = {node: n for n, node in enumerate(reversed(path))}


def count_cheats(max_dist, min_gain):
    # We evaluate all cheats along the path, by checking all end cheats at
    # a distance of max_dist from the start cheat.
    total = 0
    for start_cheat in path:
        dist_start_cheat_to_end = dist_to_end[start_cheat]
        for dist_of_cheat, end_cheat in get_points_at_max_dist(start_cheat, max_dist):
            if end_cheat in walls:
                continue
            gain = dist_start_cheat_to_end - (dist_of_cheat + dist_to_end[end_cheat])
            if gain >= min_gain:
                total += 1
    return total


print(count_cheats(2, 100))
print(count_cheats(20, 100))
