import sys
from collections import defaultdict
from dataclasses import dataclass
from bisect import bisect, bisect_left, insort

data = sys.stdin.read().splitlines()

ROWS = len(data)
COLS = len(data[0])


@dataclass
class Guard:
    col: int
    row: int
    facing: int  # index in "^>v<"

    facing_to_delta = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def turn_right(self):
        # We could have implemented this with a dict matching the directions
        # to their counterparts after turning right, but this is faster
        if self.facing < 3:
            self.facing += 1
        else:  # 3 => 0
            self.facing = 0

    def next_position(self):
        d_col, d_row = self.facing_to_delta[self.facing]
        return self.col + d_col, self.row + d_row

    def set_position(self, position):
        self.col, self.row = position

    def get_position(self):
        return self.col, self.row

    def state(self):
        # Much faster than dataclasses.astuple(self)
        return self.col, self.row, self.facing


blocks = set()
blocks_per_row = defaultdict(list)
blocks_per_col = defaultdict(list)
guard = None

for r, row in enumerate(data):
    for c, cell in enumerate(row):
        if cell == "#":
            blocks.add((c, r))
            blocks_per_row[r].append(c)
            blocks_per_col[c].append(r)
        elif cell in "^>v<":
            guard = Guard(c, r, "^>v<".index(cell))

assert guard is not None  # for mypy


# COMMON
#
def in_bounds(position):
    c, r = position
    return 0 <= r < ROWS and 0 <= c < COLS


def get_guard_states(guard, blocks):
    # Returns all the guard states until it goes out of bounds
    yield guard.state()
    while in_bounds(position := guard.next_position()):
        if position not in blocks:
            guard.set_position(position)
        else:
            guard.turn_right()
        yield guard.state()


def detect_loop(guard, blocks_per_row, blocks_per_col):
    # Returns True if the guard goes in a loop, False otherwise
    # Note that the guard is modified in place
    left_or_right = {1, 3}
    positive_direction = {1, 2}

    past_states = {guard.state()}
    while True:
        if guard.facing in left_or_right:
            blocks, point = blocks_per_row[guard.row], guard.col
        else:
            blocks, point = blocks_per_col[guard.col], guard.row

        if not blocks:  # no blocks in this direction
            return False

        # Use bisect to get the next block in the direction of the guard
        index = bisect(blocks, point)

        if guard.facing in positive_direction:  # we end up *before* the block
            if index == len(blocks):  # no more blocks in this direction
                return False
            next_point = blocks[index] - 1
        else:  # going "backward", so we end up *after* the block
            if index == 0:  # no more blocks in this direction
                return False
            next_point = blocks[index - 1] + 1

        # The guard "jumps" directly right before the next block
        if guard.facing in left_or_right:
            guard.col = next_point
        else:
            guard.row = next_point

        # Then... it turns right
        guard.turn_right()

        state = guard.state()
        if state in past_states:
            return True  # loop detected
        past_states.add(state)

    raise RuntimeError("Should never reach this point")


# PART 1
#
guard_initial_position = guard.get_position()  # for part 2

guard_states = list(get_guard_states(guard, blocks))
guard_positions = {(gc, gr) for (gc, gr, _) in guard_states}
print(len(guard_positions))


# PART 2
#
first_step_at_position = {}
for n, (gc, gr, _) in enumerate(guard_states):
    if (gc, gr) not in first_step_at_position:
        first_step_at_position[gc, gr] = n

total = 0
for gc, gr in guard_positions - {guard_initial_position}:
    # Except for the initial position, we need to insert the guard position
    # into the sorted lists of blocks per row and column
    blocks_per_row_for_gr = blocks_per_row[gr]
    blocks_per_col_for_gc = blocks_per_col[gc]
    insort(blocks_per_row_for_gr, gc)
    insort(blocks_per_col_for_gc, gr)

    # We only compute the loop detection from the movement just before
    # the guard would hit it, as the movement before would not change.
    # This can never be 0 as we removed the initial guard position,
    # so all the steps are > 0.
    starting_step = first_step_at_position[gc, gr] - 1
    starting_state = guard_states[starting_step]
    if detect_loop(Guard(*starting_state), blocks_per_row, blocks_per_col):
        total += 1

    # Remove inserted element using bisect as it's faster
    del blocks_per_row_for_gr[bisect_left(blocks_per_row_for_gr, gc)]
    del blocks_per_col_for_gc[bisect_left(blocks_per_col_for_gc, gr)]
    # Those are equivalent to, but faster than:
    # blocks_per_row_for_gr.remove(gc)
    # blocks_per_col_for_gc.remove(gr)

print(total)
