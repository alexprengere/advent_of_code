import sys
from dataclasses import dataclass, replace, astuple

data = sys.stdin.read().splitlines()

ROWS = len(data)
COLS = len(data[0])


def in_bounds(position):
    return 0 <= position.imag < ROWS and 0 <= position.real < COLS


@dataclass
class Guard:
    position: complex
    direction: complex


cell_to_dir = {
    "^": -1j,
    ">": +1,
    "v": +1j,
    "<": -1,
}

blocks = set()
guard = None
for r, row in enumerate(data):
    for c, cell in enumerate(row):
        position = complex(c, r)
        if cell == "#":
            blocks.add(position)
        elif cell in "^>v<":
            guard = Guard(position, cell_to_dir[cell])

assert guard is not None  # for mypy


# PART 1
#
def get_guard_positions(guard, blocks):
    guard = replace(guard)  # copy to not modify the original

    positions = {guard.position}
    while in_bounds(position := guard.position + guard.direction):
        if position not in blocks:
            guard.position = position
            positions.add(position)
        else:
            guard.direction *= 1j

    return positions


print(len(get_guard_positions(guard, blocks)))


# PART 2
#
def detect_loop(guard, blocks):
    guard = replace(guard)  # copy to not modify the original

    past_states = {astuple(guard)}
    while in_bounds(position := guard.position + guard.direction):
        if position not in blocks:
            guard.position = position
        else:
            guard.direction *= 1j

            state = astuple(guard)
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
