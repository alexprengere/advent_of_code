import sys
import itertools

SHAPES = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]


MAX_ROCKS = 2022  # part 1
PATTERNS = sys.stdin.read().rstrip()
X_START = 2
Y_START = 3
Y_FLOOR = -1
X_WALLS = -1, 7


def get_next_shape(highest_rock, _iterator=itertools.cycle(SHAPES)):
    y_delta = Y_START + 1 + highest_rock
    return {(X_START + dx, y_delta + dy) for (dx, dy) in next(_iterator)}


patterns = itertools.cycle([(-1 if p == "<" else +1, 0) for p in PATTERNS])
rocks = set()
highest_rock = Y_FLOOR
shape = get_next_shape(Y_FLOOR)
step = 0

total_rocks = 0
while total_rocks < MAX_ROCKS:
    step += 1
    if step % 2 == 1:
        dx, dy = next(patterns)
    else:
        dx, dy = (0, -1)

    next_shape = {(x + dx, y + dy) for (x, y) in shape}
    x_min, *_, x_max = sorted(x for x, _ in next_shape)
    y_min = min(y for _, y in next_shape)
    collision = bool(rocks & next_shape)

    if x_min <= X_WALLS[0] or x_max >= X_WALLS[1] or collision and dy != -1:
        # 1. Bumping into walls
        # 2. Bumping into other rocks on non-downward move
        pass
    elif collision or y_min <= Y_FLOOR:
        total_rocks += 1
        rocks |= shape
        y_max = max(y for _, y in shape)
        if highest_rock < y_max:
            highest_rock = y_max
        shape = get_next_shape(highest_rock)
        step = 0
    else:
        shape = next_shape

print(highest_rock - Y_FLOOR)
