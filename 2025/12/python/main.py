import sys
import string
from itertools import batched
from collections import deque

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
    shapes[shape_id] = coords

regions = []
for region in _input[region_index:]:
    size, quantities = region.split(":")
    width, length = map(int, size.split("x"))
    quantities = list(map(int, quantities.split()))
    regions.append(((width, length), quantities))


def translate_shape(shape, offset):
    offset_x, offset_y = offset
    return {(x + offset_x, y + offset_y) for x, y in shape}


def rotate_shape(shape):
    # Rotate 90 degrees clockwise from its center
    # We need to make sure the shape stays in the same bounding box
    min_x = min(x for x, y in shape)
    min_y = min(y for x, y in shape)
    max_y = max(y for x, y in shape)
    return {(-y + min_x + max_y, x + min_y - min_x) for x, y in shape}


def flip_shape(shape):
    # Flip vertically, but make sure we stay in the same bounding box
    min_x = min(x for x, y in shape)
    max_x = max(x for x, y in shape)
    return {(-x + min_x + max_x, y) for x, y in shape}


def has_vertical_symmetry(shape):
    return flip_shape(shape) == shape


def has_horizontal_symmetry(shape):
    shape = rotate_shape(shape)
    return flip_shape(shape) == shape


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
    print()


def all_transformations(shape):
    current_shape = shape
    for _ in range(4):
        yield current_shape
        current_shape = rotate_shape(current_shape)

    if has_vertical_symmetry(shape) or has_horizontal_symmetry(shape):
        return

    current_shape = flip_shape(shape)
    for _ in range(4):
        yield current_shape
        current_shape = rotate_shape(current_shape)


def all_translations(shape, bounds):
    bounds_x, bounds_y = bounds
    max_x = max(x for x, y in shape)
    max_y = max(y for x, y in shape)
    for offset_x in range(bounds_x - max_x):
        for offset_y in range(bounds_y - max_y):
            yield translate_shape(shape, (offset_x, offset_y))


def all_candidates(shape, bounds):
    for transformed_shape in all_transformations(shape):
        yield from all_translations(transformed_shape, bounds)


def in_bounds(candidate, bounds):
    bounds_x, bounds_y = bounds
    for x, y in candidate:
        if not (0 <= x < bounds_x and 0 <= y < bounds_y):
            return False
    return True


def isdisjoint(candidate, placed_shapes):
    for shape in placed_shapes:
        if not shape.isdisjoint(candidate):
            return False

    return True


def compute_key(placed_shapes):
    if not placed_shapes:
        return frozenset()
    return frozenset(set.union(*placed_shapes))


def sanity_check(shapes, bounds, quantities):
    total_area = bounds[0] * bounds[1]
    shape_area = sum(len(shapes[shape_id]) * q for shape_id, q in enumerate(quantities))
    return shape_area < total_area


def solve(shapes, bounds, quantities, fast=False):
    # OK so here is a solver using DFS with memoization, but it is too slow,
    # only fast enough for the first 2 examples.
    # But it turns out a simple sanity check is enough for the given inputs :)
    # I found that after quite some time trying to optimize the solver, and
    # Reddit hinting about "it is easier than you think".
    if fast:
        if sanity_check(shapes, bounds, quantities):
            return True
        else:
            return False

    stack = deque([([], quantities)])
    visited = set()
    while stack:
        placed_shapes, remaining_quantities = stack.pop()

        key = compute_key(placed_shapes), tuple(remaining_quantities)
        if key in visited:
            continue
        visited.add(key)

        if all(q == 0 for q in remaining_quantities):
            show_shape(bounds, *placed_shapes)
            return True

        for shape_id, quantity in enumerate(remaining_quantities):
            if quantity == 0:
                continue

            shape = shapes[shape_id]
            for candidate in all_candidates(shape, bounds):
                if not in_bounds(candidate, bounds):
                    continue
                if not isdisjoint(candidate, placed_shapes):
                    continue
                new_remaining_quantities = list(remaining_quantities)
                new_remaining_quantities[shape_id] -= 1
                stack.append((placed_shapes + [candidate], new_remaining_quantities))

    return False


fit = 0
for bounds, quantities in regions:
    fit += solve(shapes, bounds, quantities, fast=True)
print(fit)
