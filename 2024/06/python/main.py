import sys
from dataclasses import dataclass, replace

data = sys.stdin.read().splitlines()

ROWS = len(data)
COLS = len(data[0])


def in_bounds(position):
    r, c = position
    return 0 <= r < ROWS and 0 <= c < COLS


@dataclass
class Guard:
    position: tuple
    facing: int  # index in "^>v<"

    def turn_right(self):
        # We could have implemented this with a dict matching the directions
        # to their counterparts after turning right, but this is faster
        if self.facing < 3:
            self.facing += 1
        else:  # 3 => 0
            self.facing = 0

    def position_forward(self):
        r, c = self.position
        if self.facing == 0:
            return r - 1, c
        if self.facing == 1:
            return r, c + 1
        if self.facing == 2:
            return r + 1, c
        if self.facing == 3:
            return r, c - 1

    def state(self):
        return (*self.position, self.facing)  # immutable representation


blocks = set()
guard = None
for r, row in enumerate(data):
    for c, cell in enumerate(row):
        position = r, c
        if cell == "#":
            blocks.add(position)
        elif cell in "^>v<":
            guard = Guard(position, cell.index(cell))

assert guard is not None  # for mypy


# PART 1
#
def get_guard_positions(guard, blocks):
    guard = replace(guard)  # copy to not modify the original

    positions = {guard.position}
    while in_bounds(position := guard.position_forward()):
        if position not in blocks:
            guard.position = position
            positions.add(position)
        else:
            guard.turn_right()

    return positions


print(len(get_guard_positions(guard, blocks)))


# PART 2
#
def detect_loop(guard, blocks):
    guard = replace(guard)  # copy to not modify the original

    past_states = {guard.state()}
    while in_bounds(position := guard.position_forward()):
        if position not in blocks:
            guard.position = position
        else:
            guard.turn_right()

        state = guard.state()
        if state in past_states:
            return True  # loop detected
        past_states.add(state)

    return False  # guard just left the grid


print(
    sum(
        detect_loop(guard, blocks | {p})
        for p in get_guard_positions(guard, blocks) - {guard.position}
    )
)
