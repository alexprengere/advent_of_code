import sys
from dataclasses import dataclass

arrow_to_dir = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

_input = sys.stdin.read()

grid, arrows = _input.split("\n\n")
grid = grid.splitlines()
directions = [arrow_to_dir[a] for a in arrows if a.strip()]

HEIGHT = len(grid)
WIDTH = len(grid[0]) * 2


def move(point, dir_):
    (x, y), (dx, dy) = point, dir_
    return (x + dx, y + dy)


def move_right(point):
    x, y = point
    return (x + 1, y)


def move_left(point):
    x, y = point
    return (x - 1, y)


@dataclass(slots=True)
class State:
    robot: tuple[int, int] | None
    walls: set
    left_boxes: set
    right_boxes: set

    def show(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) == self.robot:
                    print("@", end="")
                elif (x, y) in self.walls:
                    print("#", end="")
                elif (x, y) in self.left_boxes:
                    print("[", end="")
                elif (x, y) in self.right_boxes:
                    print("]", end="")
                else:
                    print(".", end="")
            print()

    def compute_total_gps(self):
        return sum(bx + by * 100 for bx, by in self.left_boxes)

    def _can_move(self, point, dir_, pushed):
        # Performance optimization, if point is in pushed, it means it has been
        # already checked along another path, so we can return True immediately
        if point in pushed:
            return True

        moved_point = move(point, dir_)

        if moved_point in self.walls:
            return False

        if moved_point not in self.left_boxes and moved_point not in self.right_boxes:
            return True

        vertical = dir_[1] != 0

        # moved_point is a box_part, calling recursively. Note that 'pushed' is
        # only containing the left part of the boxes.
        if moved_point in self.left_boxes:
            # We are pushing against the left part of the box, so check only that
            # the right part of the box can move (otherwise, an infinite loop)
            left_ok = self._can_move(moved_point, dir_, pushed) if vertical else True
            right_ok = self._can_move(move_right(moved_point), dir_, pushed)
            if left_ok and right_ok:
                pushed.add(moved_point)
        else:
            # We now have the right part of the box, so for any horizontal movement
            # we only need to check if the left part can move
            right_ok = self._can_move(moved_point, dir_, pushed) if vertical else True
            left_ok = self._can_move(move_left(moved_point), dir_, pushed)
            if left_ok and right_ok:
                pushed.add(move_left(moved_point))

        return left_ok and right_ok

    def can_move(self, point, dir_):
        pushed = set()
        ok = self._can_move(point, dir_, pushed)
        return ok, pushed


state = State(None, set(), set(), set())

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        point = (2 * x, y)
        if cell == "@":
            state.robot = point
        elif cell == "#":
            state.walls.add(point)
            state.walls.add(move_right(point))
        elif cell == "O":
            state.left_boxes.add(point)
            state.right_boxes.add(move_right(point))


for dir_ in directions:
    ok, pushed = state.can_move(state.robot, dir_)
    # It is possible to have 'pushed' non-empty, but not be able to move the robot,
    # for example if some boxes are able to move, but not others, nothing moves at all.
    if not ok:
        continue
    state.robot = move(state.robot, dir_)

    # Only left part of boxes are in the pushed set
    for box_part in pushed:
        state.left_boxes.remove(box_part)
        state.right_boxes.remove(move_right(box_part))
    for box_part in pushed:
        moved_box_part = move(box_part, dir_)
        state.left_boxes.add(moved_box_part)
        state.right_boxes.add(move_right(moved_box_part))

# state.show()
print(state.compute_total_gps())
