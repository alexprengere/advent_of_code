import sys
import math
import itertools
from collections import defaultdict

DIRECTIONS = {
    "<": (-1, +0),
    ">": (+1, +0),
    "v": (+0, +1),
    "^": (+0, -1),
}


def neighbors(x, y):
    for dx, dy in [
        (+0, +0),  # not moving
        (+1, +0),
        (-1, +0),
        (+0, +1),
        (+0, -1),
    ]:
        yield x + dx, y + dy


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


def move(blizzards):
    # Simulate blizzards next turn.
    # Note that there is a period of math.lcm(X_MAX - 1, Y_MAX - 1)
    # in blizzards pattern, but we do not use that.
    changes = []

    for (x, y) in blizzards:
        for (dx, dy) in blizzards[x, y]:
            nx = x + dx
            ny = y + dy
            if (nx, ny) in WALLS:
                if dx == 1:
                    nx = 1
                elif dy == 1:
                    ny = 1
                elif dx == -1:
                    nx = X_MAX - 1
                elif dy == -1:
                    ny = Y_MAX - 1
                else:
                    raise AssertionError("Unknown direction")
            changes.append(((x, y), (nx, ny), (dx, dy)))

    for p, _, direction in changes:
        blizzards[p].remove(direction)
    for _, p, direction in changes:
        blizzards[p].add(direction)


def advance(explored, blizzards):
    # Move explored points to their neighbors based on latest blizzards.
    for x, y in list(explored):
        explored.remove((x, y))
        for nx, ny in neighbors(x, y):
            if (nx, ny) in WALLS:
                continue
            if blizzards[nx, ny]:
                continue
            if 0 <= nx <= X_MAX and 0 <= ny <= Y_MAX:
                explored.add((nx, ny))


P0 = X_MIN + 1, Y_MIN
P1 = X_MAX - 1, Y_MAX

explored = {P0}
fastest = {}

path = [P1, P0, P1]
target = path.pop()

for time in itertools.count():
    if target in fastest:
        print(fastest[target])
        explored = {target}
        fastest.clear()
        if path:
            target = path.pop()
        else:
            break

    move(blizzards)
    advance(explored, blizzards)
    for p in explored:
        fastest[p] = min(fastest.get(p, math.inf), time + 1)
