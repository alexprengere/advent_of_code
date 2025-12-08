import sys
from typing import NamedTuple
from functools import cache


class Point(NamedTuple):
    x: int
    y: int

    def has_exited(self):
        return self.y >= ROWS

    def down(self):
        return Point(self.x, self.y + 1)

    def left(self):
        return Point(self.x - 1, self.y)

    def right(self):
        return Point(self.x + 1, self.y)


def draw():
    print()
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) == source:
                print("S", end="")
            elif (x, y) in splitters:
                print("^", end="")
            elif (x, y) in beams:
                print("|", end="")
            else:
                print(".", end="")
        print()


_input = sys.stdin.readlines()
ROWS = len(_input)
COLS = len(_input[0].rstrip())

source = None
splitters = set()
for y, row in enumerate(_input):
    for x, value in enumerate(row.rstrip()):
        if value == "S":
            source = Point(x, y)
        elif value == "^":
            splitters.add(Point(x, y))


# PART 1
#
beams = {source}
splits = 0
for _ in range(ROWS):  # at most ROWS moves needed
    # import os
    # os.system("clear")
    # draw()
    beams_next = set()
    for beam in beams:
        beam = beam.down()
        if beam.has_exited():
            continue
        if beam in splitters:
            splits += 1
            beams_next.add(beam.left())
            beams_next.add(beam.right())
        else:
            beams_next.add(beam)
    beams = beams_next

print(splits)


# PART 2
#
@cache
def timelines(beam):
    beam = beam.down()
    if beam.has_exited():
        return 1
    if beam in splitters:
        return timelines(beam.left()) + timelines(beam.right())
    else:
        return timelines(beam)


print(timelines(source))
# print(timelines.cache_info())

"""
# Another way to do Part 2:
# This uses dynamic programming instead of recursion with memoization.
# The advantage is that it doesn't use the call stack, but the disadvantage is
# that it will compute the full grid even if not all points are needed, like
# the points left/right of the source.

dp = {}
for x in range(COLS):
    dp[Point(x, ROWS)] = 1  # base case: one way to exit from below the last row

for y in range(ROWS - 1, -1, -1):
    for x in range(COLS):
        point, down = Point(x, y), Point(x, y + 1)
        if point in splitters:
            dp[point] = dp[down.left()] + dp[down.right()]
        else:
            dp[point] = dp[down]

print(dp[source])
# print(len(dp))
"""
