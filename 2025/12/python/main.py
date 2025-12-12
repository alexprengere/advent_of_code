import sys
import string
from collections import deque

try:
    from itertools import batched
except ImportError:

    def batched(iterable, n):
        # batched('ABCDEFG', 3) --> ABC DEF G
        # From Python 3.10 itertools recipes
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple([e for _, e in zip(range(n), it)]):  # noqa: B905
            yield batch


F = frozenset

_input = sys.stdin.readlines()

region_index = None
for i, row in enumerate(_input):
    if "x" in row:
        region_index = i
        break


shapes = {}
for present in batched(_input[:region_index], n=5):
    shape_id, *shape, _ = present
    shape_id = int(shape_id.split(":")[0])
    coords = set()
    for y, row in enumerate(shape):
        for x, char in enumerate(row.rstrip()):
            if char == "#":
                coords.add((x, y))
    shapes[shape_id] = F(coords)

regions = []
for region in _input[region_index:]:
    size, quantities = region.split(":")
    width, length = map(int, size.split("x"))
    quantities = list(map(int, quantities.split()))
    regions.append(((width, length), quantities))


def translate_shape(shape, offset):
    offset_x, offset_y = offset
    return F((x + offset_x, y + offset_y) for x, y in shape)


def rotate_shape(shape):
    # Rotate 90 degrees clockwise from its center, and make sure
    # we stay in the same bounding box.
    min_x = min(x for x, y in shape)
    min_y = min(y for x, y in shape)
    max_y = max(y for x, y in shape)
    return F((-y + min_x + max_y, x + min_y - min_x) for x, y in shape)


def flip_shape(shape):
    # Flip vertically, but make sure we stay in the same bounding box
    min_x = min(x for x, y in shape)
    max_x = max(x for x, y in shape)
    return F((-x + min_x + max_x, y) for x, y in shape)


def show_shape(bounds, *placed_shapes):
    bounds_x, bounds_y = bounds
    letters = {}
    for i, shape in enumerate(placed_shapes):
        letter = string.ascii_uppercase[i % 26]
        for coord in shape:
            letters[coord] = letter

    for y in range(bounds_y):
        for x in range(bounds_x):
            if (x, y) in letters:
                print(letters[x, y], end="")
            else:
                print(".", end="")
        print()
    print(flush=True)


def all_transformations(shape):
    seen = set()
    seen.add(shape)
    yield shape
    # return
    for _ in range(3):
        shape = rotate_shape(shape)
        if shape not in seen:
            seen.add(shape)
            yield shape

    shape = flip_shape(shape)
    if shape in seen:
        return
    seen.add(shape)
    yield shape

    for _ in range(3):
        shape = rotate_shape(shape)
        if shape not in seen:
            seen.add(shape)
            yield shape


def all_translations(shape, bounds):
    bounds_x, bounds_y = bounds
    max_x = max(x for x, y in shape)
    max_y = max(y for x, y in shape)
    for offset_x in range(bounds_x - max_x):
        for offset_y in range(bounds_y - max_y):
            yield translate_shape(shape, (offset_x, offset_y))


def stuck_to(candidate, placed_shapes):
    # This is a simple heuristic to avoid generating shapes
    # that are not connected to the already placed ones.
    if not placed_shapes:
        return True
    for x, y in candidate:
        neighbors = F({(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)})
        for shape in placed_shapes:
            if not shape.isdisjoint(neighbors):
                return True
    return False


def impossible(shapes, bounds, quantities):
    # Check if the total area of the shapes exceeds the bounding box area
    total_area = bounds[0] * bounds[1]
    shape_area = sum(len(shapes[shape_id]) * q for shape_id, q in enumerate(quantities))
    return shape_area > total_area


def trivial(shapes, bounds, quantities):
    # Find if we can just stack the 9x9 shapes in a grid
    total_area = bounds[0] * bounds[1]
    return sum(quantities) * 9 <= total_area


def generate_children(placed_shapes, remaining_quantities, shapes, bounds):
    for shape_id, quantity in enumerate(remaining_quantities):
        if quantity == 0:
            continue
        shape = shapes[shape_id]
        # The order is important here for pruning the search space, we first
        # want to yield translations of the original shape, in case we hit
        # the easy case where translating without rotation/flip is enough.
        for transformed in all_transformations(shape):
            for candidate in all_translations(transformed, bounds):
                if any(not candidate.isdisjoint(s) for s in placed_shapes):
                    continue
                if not stuck_to(candidate, placed_shapes):
                    continue
                new_remaining_quantities = list(remaining_quantities)
                new_remaining_quantities[shape_id] -= 1
                yield ((placed_shapes + [candidate], new_remaining_quantities))


def compute_key(state):
    placed_shapes, remaining_quantities = state
    return F().union(*placed_shapes), tuple(remaining_quantities)


def solve(shapes, bounds, quantities, fast_mode=True):
    # OK so here is a solver using DFS with lazy generation of children states,
    # to avoid keeping all states in memory at once.
    # We use DFS to go deep quickly and find a solution fast if it exists.
    # It should run the example in a few minutes, the actual AoC input being
    # trivially solved by the sanity checks :).
    # I found that after quite some time trying to optimize the solver, and
    # Reddit hinting about "it is easier than you think".
    if impossible(shapes, bounds, quantities):
        return False
    elif trivial(shapes, bounds, quantities) and fast_mode:
        return True

    visited = set()
    state = ([], quantities)
    stack = deque([(state, generate_children(*state, shapes, bounds))])

    while stack:
        state, it = stack[-1]

        _, remaining_quantities = state
        if all(q == 0 for q in remaining_quantities):
            return True

        """
        placed_shapes = state[0]
        show_shape(bounds, *placed_shapes)
        print(f"Remaining: {remaining_quantities}")
        print(f"Stack size: {len(stack)}")
        print(f"Visited states: {len(visited)}")
        print("-----", flush=True)
        """
        try:
            state_child = next(it)
            key = compute_key(state_child)
            if key in visited:
                continue
            visited.add(key)
            stack.append((state_child, generate_children(*state_child, shapes, bounds)))
        except StopIteration:
            stack.pop()

    return False


fit = 0
for bounds, quantities in regions:
    fit += solve(shapes, bounds, quantities, fast_mode=True)
print(fit)
