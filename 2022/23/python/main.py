import sys
import itertools
from collections import defaultdict, deque


NEIGHBORS = (
    (+1, +0),
    (-1, +0),
    (+0, +1),
    (+0, -1),
    (+1, +1),
    (-1, -1),
    (+1, -1),
    (-1, +1),
)

RULES = [
    [[(-1, +1), (+0, +1), (+1, +1)], (+0, +1)],  # NW, N, NE => N
    [[(-1, -1), (+0, -1), (+1, -1)], (+0, -1)],  # SW, S, SE => S
    [[(-1, -1), (-1, +0), (-1, +1)], (-1, +0)],  # SW, W, NW => W
    [[(+1, -1), (+1, +0), (+1, +1)], (+1, +0)],  # SE, E, NE => E
]


def move(point, direction):
    px, py = point
    dx, dy = direction
    return px + dx, py + dy


def count_ground_tiles(elves):
    x_min = min(x for x, _ in elves)
    x_max = max(x for x, _ in elves)
    y_min = min(y for _, y in elves)
    y_max = max(y for _, y in elves)

    total = (y_max - y_min + 1) * (x_max - x_min + 1)
    return total - len(elves)


_input = sys.stdin.read().splitlines()

elves = set()
for y, row in enumerate(reversed(_input)):
    for x, c in enumerate(row):
        if c == "#":
            elves.add((x, y))

rules = deque(RULES)

for turn in itertools.count(1):
    proposed = {}
    targets = defaultdict(list)

    for elf in elves:
        if not elves.isdisjoint(move(elf, d) for d in NEIGHBORS):
            for positions, choice in rules:
                if elves.isdisjoint(move(elf, d) for d in positions):
                    target = move(elf, choice)
                    proposed[elf] = target
                    targets[target].append(elf)
                    break

    for target, candidates in targets.items():
        if len(candidates) > 1:
            for elf in candidates:
                del proposed[elf]

    if not proposed:
        print(turn)
        break

    for elf, target in proposed.items():
        elves.remove(elf)
        elves.add(target)

    rules.rotate(-1)

    if turn == 10:
        print(count_ground_tiles(elves))
