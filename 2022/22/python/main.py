import sys
from typing import NamedTuple


class Position(NamedTuple):
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
for y, row in enumerate(_board, start=1):
    for x, c in enumerate(row, start=1):
        position = Position(x, y)
        if c == ".":
            TILES.add(position)
        elif c == "#":
            WALLS.add(position)
BOARD = TILES | WALLS

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


def wrap(position, direction):
    opposite = direction.opposite()
    next_pos = position.move(opposite)
    while next_pos in BOARD:
        position = next_pos
        next_pos = position.move(opposite)
    return position


position = min(p for p in TILES if p.y == 1)
direction = Direction(+1, +0)

for ins in instructions:
    if ins == "R":
        direction = direction.right()
    elif ins == "L":
        direction = direction.left()
    else:
        for _ in range(ins):
            next_pos = position.move(direction)
            if next_pos not in BOARD:
                next_pos = wrap(position, direction)
            if next_pos in WALLS:
                break
            position = next_pos

print(1000 * position.y + 4 * position.x + direction.facing())
