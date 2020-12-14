import sys

DIRECTIONS = ["N", "W", "S", "E"]
VECTORS = {
    "N": 1j,
    "S": -1j,
    "E": 1,
    "W": -1,
}
ROTATIONS = {
    -270: 1j,
    -180: -1,
    -90: -1j,
    0: 1,
    90: 1j,
    180: -1,
    270: -1j,
}


data = []
for row in sys.stdin:
    action, value = row[0], int(row[1:])
    data.append((action, value))


# PART 1
#
class Ferry:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def move(self, value, direction):
        self.point += value * VECTORS[direction]

    def turn(self, degrees):
        new_index = DIRECTIONS.index(self.direction) + degrees // 90
        self.direction = DIRECTIONS[new_index % len(DIRECTIONS)]


ferry = Ferry(0j, "E")

for action, value in data:
    if action == "L":
        ferry.turn(value)
    elif action == "R":
        ferry.turn(-value)
    elif action == "F":
        ferry.move(value, direction=ferry.direction)
    else:  # action is a direction in [N, W, S, E]
        ferry.move(value, direction=action)

print(abs(ferry.point.real) + abs(ferry.point.imag))


# PART 2
#
class Ferry:
    def __init__(self, point, waypoint):
        self.point = point
        self.waypoint = waypoint

    def move_waypoint(self, value, direction):
        self.waypoint += value * VECTORS[direction]

    def rotate_waypoint(self, degrees):
        self.waypoint *= ROTATIONS[degrees]

    def go_to_waypoint(self, value):
        self.point += value * self.waypoint


ferry = Ferry(0j, 10 + 1j)

for action, value in data:
    if action == "L":
        ferry.rotate_waypoint(value)
    elif action == "R":
        ferry.rotate_waypoint(-value)
    elif action == "F":
        ferry.go_to_waypoint(value)
    else:  # action is a direction in [N, W, S, E]
        ferry.move_waypoint(value, direction=action)

print(abs(ferry.point.real) + abs(ferry.point.imag))
