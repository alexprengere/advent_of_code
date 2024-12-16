import sys

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
WIDTH = len(grid[0])


def move(point, dir_):
    (x, y), (dx, dy) = point, dir_
    return (x + dx, y + dy)


robot = None
walls = set()
boxes = set()


def show(robot, walls, boxes):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) == robot:
                print("@", end="")
            elif (x, y) in walls:
                print("#", end="")
            elif (x, y) in boxes:
                print("O", end="")
            else:
                print(".", end="")
        print()


for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        point = (x, y)
        if cell == "@":
            robot = point
        elif cell == "#":
            walls.add(point)
        elif cell == "O":
            boxes.add(point)


def _can_move(point, walls, boxes, dir_, pushed):
    moved_point = move(point, dir_)
    if moved_point in walls:
        return False

    if moved_point not in boxes:
        return True

    # moved_point is a box, calling recursively
    ok = _can_move(moved_point, walls, boxes, dir_, pushed)
    if ok:
        pushed.add(moved_point)
    return ok


def can_move(point, walls, boxes, dir_):
    pushed = set()
    ok = _can_move(point, walls, boxes, dir_, pushed)
    return ok, pushed


def compute_total_gps(boxes):
    return sum(bx + by * 100 for bx, by in boxes)


for dir_ in directions:
    ok, pushed = can_move(robot, walls, boxes, dir_)
    if ok:
        robot = move(robot, dir_)
        for box in pushed:
            boxes.remove(box)
        for box in pushed:
            boxes.add(move(box, dir_))

# show(robot, walls, boxes)
print(compute_total_gps(boxes))
