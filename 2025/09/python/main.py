import sys
from bisect import bisect
from collections import defaultdict
from typing import NamedTuple
from itertools import combinations, pairwise, chain


class Point(NamedTuple):
    x: int
    y: int


def compute_area(p0, p1):
    dx = 1 + abs(p0.x - p1.x)
    dy = 1 + abs(p0.y - p1.y)
    return dx * dy


def generate_straight_line(p0, p1):
    if p0.x == p1.x:
        for y in range(min(p0.y, p1.y) + 1, max(p0.y, p1.y)):
            yield Point(p0.x, y)
    elif p0.y == p1.y:
        for x in range(min(p0.x, p1.x) + 1, max(p0.x, p1.x)):
            yield Point(x, p0.y)
    else:
        raise ValueError("Only horizontal or vertical lines are supported")


def draw(reds, greens, highlights=None):
    reds = set(reds)
    greens = set(greens)
    groups = [reds, greens, highlights or set()]

    x_min = min(p.x for p in chain.from_iterable(groups))
    x_max = max(p.x for p in chain.from_iterable(groups))
    y_min = min(p.y for p in chain.from_iterable(groups))
    y_max = max(p.y for p in chain.from_iterable(groups))

    for y in range(y_min, y_max + 1):
        row = []
        for x in range(x_min, x_max + 1):
            p = Point(x, y)
            if p in highlights:
                row.append("*")
            elif p in reds:
                row.append("R")
            elif p in greens:
                row.append("G")
            else:
                row.append(".")
        print("".join(row))
    print()


reds = []
for row in sys.stdin.readlines():
    x, y = map(int, row.split(","))
    reds.append(Point(x, y))


greens = []
for p0, p1 in pairwise(chain(reds, [reds[0]])):  # chain to close the shape
    for point in generate_straight_line(p0, p1):
        greens.append(point)

decreasing_red_pairs = sorted(
    ((compute_area(*pair), pair) for pair in combinations(reds, r=2)),
    reverse=True,
)


# PART 1
#
largest_area, _ = decreasing_red_pairs[0]
print(largest_area)


# PART 2
#
# We maintain lists of all x and y coordinates for each fixed y and x coordinate,
# to allow for fast checking of whether a line crosses the interior of the shape.
# The algorithm for this is to do a binary search to find the insertion points of
# the endpoints of the line segment, and if these differ, then there is at least
# one point in between, meaning the line crosses the boundary.
y_lists = defaultdict(list)
x_lists = defaultdict(list)

for point in chain(reds, greens):
    y_lists[point.x].append(point.y)
    x_lists[point.y].append(point.x)

for y_list in y_lists.values():
    y_list.sort()
for x_list in x_lists.values():
    x_list.sort()


# The next part is actually NOT necessary to solve any AoC input, as they do not contain
# such adverse cases. Look at this example:
#
# RGGGGGGR..........
# G......G..........
# G.RGGGGR..........
# G.RGGGGR..........
# G......G..........
# RGGGGR.G..........
# RGGGGR.G..........
# G......G..........
# G..RR..RGGGGGGGGGR
# G..GG............G
# RGGRRGGGGGGGGGGGGR
#
# Here, you can see there are "adjacent edges" that create situations where a line
# could cross the boundary twice without actually "leaving" the shape. To avoid dealing
# with such cases, we filter out adjacent coordinates, so that they are not counted
# as a crossing of the boundary.
#
def remove_adjacent(coords):
    filtered = []
    prev = None
    for c in coords:
        if prev is None or c - prev > 1:
            filtered.append(c)
        elif filtered:  # c "cancels" previous crossing
            filtered.pop()
        prev = c
    return filtered


for x in y_lists:
    y_lists[x] = remove_adjacent(y_lists[x])
for y in x_lists:
    x_lists[y] = remove_adjacent(x_lists[y])


def contains_rectangle(p0, p1):
    # We only test the interior, so we shrink the rectangle by 1 on all sides.
    # This helps avoid tricky cases related "walking along the edge".
    x_min = min(p0.x, p1.x) + 1
    x_max = max(p0.x, p1.x) - 1
    y_min = min(p0.y, p1.y) + 1
    y_max = max(p0.y, p1.y) - 1

    # We test all four edges of the rectangle, this is enough as we know the shape
    # does not have holes.
    if bisect(y_lists[x_min], y_min) != bisect(y_lists[x_min], y_max):
        return False
    if bisect(y_lists[x_max], y_min) != bisect(y_lists[x_max], y_max):
        return False
    if bisect(x_lists[y_min], x_min) != bisect(x_lists[y_min], x_max):
        return False
    if bisect(x_lists[y_max], x_min) != bisect(x_lists[y_max], x_max):
        return False

    # But! If you try really hard you can construct counter-examples
    # (not for AoC inputs): a '0-width tunnel' could introduce a hole:
    #
    # ...RGGGGGGGGR
    # ...G........G
    # ...G.RGGGGR.G
    # ...G.G....G.G
    # RGRG.GRGR.G.G
    # G.GG.GG.G.G.G
    # G.GRGRG.G.G.G
    # G.RGGGR.G.G.G
    # G.......G.G.G
    # G.......RGR.G
    # G...........G
    # RGGGGGGGGGGGR
    #
    # Now that we checked the edges, we include an extra check for all interior rows
    # and columns, note that this is NOT needed for AoC inputs, and it should
    # not be too long as most cases will have already failed (in the main loop,
    # we start by the bigger rectangles).
    for y in range(y_min, y_max + 1):
        if bisect(x_lists[y], x_min) != bisect(x_lists[y], x_max):
            return False
    for x in range(x_min, x_max + 1):
        if bisect(y_lists[x], y_min) != bisect(y_lists[x], y_max):
            return False

    # Final and very important check: we need to be sure that the constructed
    # rectangle is actually inside the shape, and not outside of it:
    #
    # RGR............RGR
    # G.G............G.G
    # G.G............G.G
    # G.G............G.G
    # G.G............G.G
    # G.G............G.G
    # G.RGGGGGGGGGGGGR.G
    # G....RGGGGGGR....G
    # G....G......G....G
    # RGGGGR......RGGGGR
    #
    # Again, this is NOT needed for AoC inputs, but is necessary for correctness.
    # Testing a single interior point is enough.
    if bisect(x_lists[y_max], x_max) % 2 == 0:
        return False

    return True


# As we go from largest to smallest area, the first one we find that is contained
# must be the largest contained one.
# I also tested from smallest to largest and kept track of the largest found so far,
# but it gives similar performance for more complex code in this case.
for area, pair in decreasing_red_pairs:
    if contains_rectangle(*pair):
        print(area)
        # draw(reds, greens, highlights=pair)
        break
