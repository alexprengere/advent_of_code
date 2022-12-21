import sys
import itertools

_input = sys.stdin.read().rstrip()

SHAPES = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]
PATTERNS = [(+1, 0) if p == ">" else (-1, 0) for p in _input]

NB_ROCKS = 1_000_000_000_000  # 2022 for part 1
X_RANGE = range(0, 7)


def get_shape_at(highest, _iterator=itertools.cycle(enumerate(SHAPES))):
    shape_id, shape = next(_iterator)
    return shape_id, {(2 + dx, 4 + highest + dy) for (dx, dy) in shape}


def get_top_layout(rocks):
    y_min = min(max(y for x, y in rocks if x == xi) for xi in X_RANGE)
    return frozenset((x, y - y_min) for x, y in rocks if y >= y_min)


patterns = itertools.cycle(enumerate(PATTERNS))
rocks = {(x, 0) for x in X_RANGE}
highest = 0
shape_id, shape = get_shape_at(0)
step = 0

nb_rocks = 0
memory = {}
while nb_rocks < NB_ROCKS:
    step += 1
    if step % 2 == 0:
        dx, dy = 0, -1
    else:
        pattern_id, (dx, dy) = next(patterns)
        # Cycle detection
        layout = get_top_layout(rocks)
        key = shape_id, pattern_id, layout
        if key not in memory:
            memory[key] = nb_rocks, highest
        else:
            prev_nb_rocks, prev_highest = memory[key]
            diff_nb_rocks = nb_rocks - prev_nb_rocks
            repetition = (NB_ROCKS - nb_rocks) // diff_nb_rocks
            nb_rocks += repetition * diff_nb_rocks
            y_shift = repetition * (highest - prev_highest)
            highest += y_shift
            y_max_layout = max(y for _, y in layout)
            rocks.update((x, y - y_max_layout + highest) for x, y in layout)
            shape = {(x, y + y_shift) for (x, y) in shape}

    next_shape = {(x + dx, y + dy) for (x, y) in shape}
    x_min, *_, x_max = sorted(x for x, _ in next_shape)
    y_min = min(y for _, y in next_shape)
    collision = bool(rocks & next_shape)

    # 1. Bumping into walls
    # 2. Bumping into other rocks on non-downward move
    # 3. Collision
    # 4. Moving down
    if x_min < X_RANGE.start or x_max >= X_RANGE.stop:
        pass
    elif collision and dy != -1:
        pass
    elif collision:
        nb_rocks += 1
        rocks |= shape
        y_max = max(y for _, y in shape)
        if highest < y_max:
            highest = y_max
        shape_id, shape = get_shape_at(highest)
        step = 0
    else:
        shape = next_shape

print(highest)
