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
