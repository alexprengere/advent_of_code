import sys
import itertools

_input = sys.stdin.readlines()
ROWS = len(_input)
COLS = len(_input[0].rstrip())


def draw(rolls):
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in rolls:
                print(len(rolls[x, y]), end="")
            else:
                print(".", end="")
        print()


D_INDICES = set(itertools.product((-1, 0, 1), repeat=2)) - {(0, 0)}


def neighbors(x, y):
    for dx, dy in D_INDICES:
        yield x + dx, y + dy


# rolls is the mapping of {roll: {neighbor rolls}}, this is what is mutated.
# Basically at each step, when a roll is removed, it "tells its neighbors",
# then is actually removed from rolls. Only such neighbors are considered
# for removal at the next step.
# This way, it avoids re-counting rolls in neighbors at each step.
# And we iterate until rolls is stable.
rolls = {}
for y, row in enumerate(_input):
    for x, value in enumerate(row.rstrip()):
        if value == "@":
            rolls[x, y] = set()

for point in rolls:
    for neighbor in neighbors(*point):
        if neighbor in rolls:
            rolls[point].add(neighbor)

nb_rolls_at_start = len(rolls)
to_remove = [p for p in rolls if len(rolls[p]) < 4]
candidates = set()
print(len(to_remove))  # part 1

while to_remove:
    for point in to_remove:
        for neighbor in rolls[point]:
            rolls[neighbor].remove(point)
            candidates.add(neighbor)
        del rolls[point]
    to_remove[:] = [p for p in candidates if p in rolls and len(rolls[p]) < 4]
    candidates.clear()
    # import os
    # os.system('clear')
    # draw(rolls)

print(nb_rolls_at_start - len(rolls))  # part 2
