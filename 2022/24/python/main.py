import sys
import itertools
from collections import defaultdict


def movements(x, y):
    # Possible movements from a point (x, y)
    for dx, dy in [
        (+0, +0),  # waiting
        (+1, +0),
        (-1, +0),
        (+0, +1),
        (+0, -1),
    ]:
        yield x + dx, y + dy


def move(blizzards):
    # Simulate blizzards next turn.
    # Note that there is a period of math.lcm(X_MAX - 1, Y_MAX - 1)
    # in blizzards pattern, but we do not use that.
    updates = []

    for (x, y) in blizzards:
        for (dx, dy) in blizzards[x, y]:
            nx = x + dx
            ny = y + dy
            if (nx, ny) in WALLS:
                if dx == +1:
                    nx = X_MIN + 1
                elif dy == +1:
                    ny = Y_MIN + 1
                elif dx == -1:
                    nx = X_MAX - 1
                elif dy == -1:
                    ny = Y_MAX - 1
                else:
                    raise AssertionError("Unknown direction")
            updates.append(((x, y), (nx, ny), (dx, dy)))

    # The order matters here, otherwise you might remove a new blizzard
    # arriving at position p
    for p, _, direction in updates:
        blizzards[p].remove(direction)
    for _, p, direction in updates:
        blizzards[p].add(direction)


DIRECTIONS = {
    "<": (-1, +0),
    ">": (+1, +0),
    "v": (+0, +1),
    "^": (+0, -1),
}
WALLS = set()
blizzards = defaultdict(set)

_input = sys.stdin.read()
for y, row in enumerate(_input.splitlines()):
    for x, c in enumerate(row):
        point = x, y
        if c == "#":
            WALLS.add(point)
        elif c in "<>v^":
            blizzards[point].add(DIRECTIONS[c])

X_MIN = min(x for x, _ in WALLS)
X_MAX = max(x for x, _ in WALLS)
Y_MIN = min(y for _, y in WALLS)
Y_MAX = max(y for _, y in WALLS)

P0 = X_MIN + 1, Y_MIN
P1 = X_MAX - 1, Y_MAX

points, visited = {P0}, {P0: 0}
path = [P1, P0, P1]
target = path.pop()

for time in itertools.count():
    if target in visited:
        print(f"Time to reach: {visited[target]}")
        points, visited = {target}, {target: 0}
        if not path:
            break
        target = path.pop()

    # Update the blizzards positions
    move(blizzards)

    # Update points positions to their 'neighbors'
    for x, y in list(points):
        points.remove((x, y))
        for nx, ny in movements(x, y):
            if (nx, ny) in WALLS:
                continue
            if blizzards[nx, ny]:
                continue
            if 0 <= nx <= X_MAX and 0 <= ny <= Y_MAX:
                points.add((nx, ny))
                # points visiting a new coordinate are recorded in visited
                if (nx, ny) not in visited:
                    visited[nx, ny] = time + 1
