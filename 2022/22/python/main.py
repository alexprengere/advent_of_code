import sys
import math
from typing import NamedTuple


class Position(NamedTuple):
    # We could use complex numbers to represent positions,
    # but I wanted to try something else.
    x: int
    y: int

    def move(self, direction):
        return self.__class__(self.x + direction.x, self.y + direction.y)


class Direction(NamedTuple):
    x: int
    y: int

    def right(self):
        return self.__class__(-self.y, self.x)

    def left(self):
        return self.__class__(self.y, -self.x)

    def opposite(self):
        return self.__class__(-self.x, -self.y)

    def facing(self):
        if self == (+1, +0):
            return 0
        if self == (+0, +1):
            return 1
        if self == (-1, +0):
            return 2
        if self == (+0, -1):
            return 3
        raise NotImplementedError()


_input = sys.stdin.read().splitlines()
_board, _path = _input[:-2], _input[-1]

TILES, WALLS = set(), set()
for y, row in enumerate(_board):
    for x, c in enumerate(row):
        position = Position(x, y)
        if c == ".":
            TILES.add(position)
        elif c == "#":
            WALLS.add(position)
CUBE = TILES | WALLS

PART = 2

# This part is a bit hardcoded but any input from AoC should work
# regardless, as the shape of the flatten cube is the same for everyone:
#
#          +-----+-----+
#          | 1,0 | 2,0 |
#          +-----+-----+
#          | 1,1 |
#    +-----+-----+
#    | 0,2 | 1,2 |
#    +-----+-----+
#    | 0,3 |
#    +-----+
#
# It will not work on the sample input, which has a different shape.
#
if PART == 2:
    assert math.isqrt(len(CUBE) // 6) == 50
#
# This maps "side + direction" to (new direction, func), where
# func is used to compute the new position.
WRAP2 = {
    (1, 0, -1, +0): (Direction(+1, +0), lambda p: Position(0, 149 - p.y)),
    (1, 0, +0, -1): (Direction(+1, +0), lambda p: Position(0, p.x + 100)),
    (2, 0, +1, +0): (Direction(-1, +0), lambda p: Position(99, 149 - p.y)),
    (2, 0, +0, +1): (Direction(-1, +0), lambda p: Position(99, p.x - 50)),
    (2, 0, +0, -1): (Direction(+0, -1), lambda p: Position(p.x - 100, 199)),
    (1, 1, +1, +0): (Direction(+0, -1), lambda p: Position(p.y + 50, 49)),
    (1, 1, -1, +0): (Direction(+0, +1), lambda p: Position(p.y - 50, 100)),
    (1, 2, +1, +0): (Direction(-1, +0), lambda p: Position(149, 149 - p.y)),
    (1, 2, +0, +1): (Direction(-1, +0), lambda p: Position(49, 100 + p.x)),
    (0, 2, -1, +0): (Direction(+1, +0), lambda p: Position(50, 149 - p.y)),
    (0, 2, +0, -1): (Direction(+1, +0), lambda p: Position(50, 50 + p.x)),
    (0, 3, +1, +0): (Direction(+0, -1), lambda p: Position(p.y - 100, 149)),
    (0, 3, +0, +1): (Direction(+0, +1), lambda p: Position(p.x + 100, 0)),
    (0, 3, -1, +0): (Direction(+0, +1), lambda p: Position(p.y - 100, 0)),
}

if PART == 1:
    def wrap(position, direction):
        opposite = direction.opposite()
        next_pos = position.move(opposite)
        while next_pos in CUBE:
            position = next_pos
            next_pos = position.move(opposite)
        # It is not useful to return direction here,
        # as it has not changed from input, but this is
        # done to have the same signature with part 2.
        return position, direction
else:
    def wrap(position, direction):
        side = position.x // 50, position.y // 50
        direction, func = WRAP2[*side, *direction]
        return func(position), direction


instructions, acc = [], ""
for c in _path:
    if c in ("R", "L"):
        instructions.append(int(acc))
        instructions.append(c)
        acc = ""
    else:
        acc += c
if acc:
    instructions.append(int(acc))

position = min(p for p in TILES if p.y == 0)
direction = Direction(+1, +0)

for ins in instructions:
    if ins == "R":
        direction = direction.right()
    elif ins == "L":
        direction = direction.left()
    else:
        for _ in range(ins):
            next_pos = position.move(direction)
            next_dir = direction
            if next_pos not in CUBE:
                next_pos, next_dir = wrap(position, direction)
            if next_pos in WALLS:
                break
            position = next_pos
            direction = next_dir

print(1000 * (position.y + 1) + 4 * (position.x + 1) + direction.facing())
