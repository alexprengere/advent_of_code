import sys
import math
from statistics import variance
from dataclasses import dataclass
from collections import Counter

data = sys.stdin.read()

WIDTH = 101
HEIGHT = 103

# This matters when solving things
assert WIDTH % 2 == 1
assert HEIGHT % 2 == 1
assert math.gcd(WIDTH, HEIGHT) == 1


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    def move(self, turns=1):
        self.px = (self.px + self.vx * turns) % WIDTH
        self.py = (self.py + self.vy * turns) % HEIGHT

    def get_quadrant(self):
        # Place the robot in the quadrant of the screen, 0 for the middle
        #
        #  11 0 33
        #  11 0 33
        #  0000000
        #  22 0 44
        #  22 0 44
        #
        px, py = self.px, self.py

        if px == WIDTH // 2 or py == HEIGHT // 2:
            return 0

        if px < WIDTH // 2:
            if py < HEIGHT // 2:
                return 1
            else:
                return 2
        else:
            if py < HEIGHT // 2:
                return 3
            else:
                return 4


def compute_safety_factor(robots):
    robots_per_quadrant = Counter()
    for robot in robots:
        robots_per_quadrant[robot.get_quadrant()] += 1

    result = 1
    for quadrant in (1, 2, 3, 4):
        result *= robots_per_quadrant[quadrant]
    return result


def show_grid(robots):
    robots_per_position = Counter()
    for robot in robots:
        robots_per_position[robot.px, robot.py] += 1

    for y in range(HEIGHT):
        for x in range(WIDTH):
            n = robots_per_position[x, y]
            print(n if n > 0 else ".", end="")
        print()


robots = []

for row in data.splitlines():
    p, v = row.split()
    px, py = p[2:].split(",")
    vx, vy = v[2:].split(",")
    robot = Robot(
        int(px),
        int(py),
        int(vx),
        int(vy),
    )
    robots.append(robot)


# PART 1
#
for robot in robots:
    robot.move(turns=100)

print(compute_safety_factor(robots))

for robot in robots:
    robot.move(turns=-100)  # reset to the initial position


# PART 2
#
def chinese_remainder_theorem(t1, n1, t2, n2):
    """Chinese Remainder Theorem

    Solve for 't' the system of congruences:

    t = t1 (mod n1)
    t = t2 (mod n2)

    >>> chinese_remainder_theorem(2, 3, 3, 5)
    8

    In the above example, 8 is the smallest solution that satisfies
    8 % 2 == 2 and 8 % 3 == 3.
    """
    # n1 and n2 must be coprime, meaning that gcd(n1, n2) = 1
    n1_inv = pow(n1, -1, n2)  # n1 * n1_inv = 1 (mod n2)
    n2_inv = pow(n2, -1, n1)  # n2 * n2_inv = 1 (mod n1)

    # This number has indeed t1 (mod n1) and t2 (mod n2)
    return (t1 * n2 * n2_inv + t2 * n1 * n1_inv) % (n1 * n2)


# As the robots wrap around the edges, we know that:
#
# * the period of the x movements is WIDTH
# * the period of the y movements is HEIGHT
#
# We also know that the movements are independent, so we can solve
# the problem for x and y separately. If we can find a specific turn
# where 'something happens' for x and y, we can find the turn where
# 'something happens' for both x and y, by solving the following system
# of congruences:
# x_turn (mod WIDTH) = y_turn (mod HEIGHT)
#
# Or equivalently:
# x_turn + k1 * WIDTH = y_turn + k2 * HEIGHT
#
# The 'something happens' we are looking for is the turn where the variance
# of the positions is minimized. We only need to compute this up to the turn
# max(WIDTH, HEIGHT) as the movements are periodic.
#
x_variance_low = variance([robot.px for robot in robots])
y_variance_low = variance([robot.py for robot in robots])

x_turn = 0  # turn where x variance is minimized
y_turn = 0  # turn where y variance is minimized

last_turn = max(WIDTH, HEIGHT)

for turn in range(1, 1 + last_turn):
    for robot in robots:
        robot.move()

    x_variance = variance([robot.px for robot in robots])
    if x_variance < x_variance_low:
        x_variance_low, x_turn = x_variance, turn

    y_variance = variance([robot.py for robot in robots])
    if y_variance < y_variance_low:
        y_variance_low, y_turn = y_variance, turn


xy_turn = chinese_remainder_theorem(x_turn, WIDTH, y_turn, HEIGHT)
print(xy_turn)

# Just for fun, let's see that tree!
for robot in robots:
    robot.move(turns=xy_turn - last_turn)
show_grid(robots)
