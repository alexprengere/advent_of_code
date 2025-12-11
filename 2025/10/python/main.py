import sys
from collections import deque
from itertools import combinations


def parse_button_as_int(s):
    # s looks like (0,1,4), we convert it to an int where each position is a bit
    res = 0
    for c in s[1:-1].split(","):
        res |= 1 << int(c)
    return res


def parse_button_as_list(s):
    return list(map(int, s[1:-1].split(",")))


def parse_diagram_as_int(s):
    # s looks like [.#..#], we convert it to an int where each # is a 1 bit
    res = 0
    for i, c in enumerate(s[1:-1]):
        if c == "#":
            res |= 1 << i
    return res


def parse_joltage(s):
    return list(map(int, s[1:-1].split(",")))


machines = []
for row in sys.stdin:
    _diagram, *_buttons, _joltage = row.rstrip().split()
    diagram = parse_diagram_as_int(_diagram)
    buttons_as_int = list(map(parse_button_as_int, _buttons))
    buttons_as_list = list(map(parse_button_as_list, _buttons))
    joltage = parse_joltage(_joltage)
    machines.append((diagram, buttons_as_int, buttons_as_list, joltage))


# PART 1
#
# First: each button needs to be pressed either 0 or 1 times, as a second
# press will just toggle the same lights back off.
# We need to iterate over all possible combinations of button presses.
# As we want to minimize the number of presses, we start with all the
# combinations of 1 button presses, then move to 2 presses, etc.
#
# Note that here we use a cute trick for performance: lights and buttons
# are represented as a single integer, whose individual bits are the on/off
# statut for lights, and which light are affected for buttons.
# With this, pressing a button is just applying a XOR with the lights.
#
def solve_part_1(machine):
    diagram, buttons_as_int, _, _ = machine
    for presses in range(1 + len(buttons_as_int)):
        for comb in combinations(buttons_as_int, presses):
            lights = 0
            for button in comb:
                lights ^= button
            if lights == diagram:
                return presses


print(sum(map(solve_part_1, machines)))


# PART 2
#
# The first function is my initial attempt, using a breadth-first search
# to explore all possible states. It works fine for the example, but is too
# slow for the full input, even with some pruning based on joltage values.
#
def solve_part_2_only_for_example(machine):
    _, _, buttons_as_list, joltage = machine
    target = tuple(joltage)

    start = (0,) * len(joltage)
    if start == target:
        return 0

    stack = deque([(start, 0)])
    visited = set()
    while stack:
        jolt, presses = stack.popleft()

        for button in buttons_as_list:
            jolt_list = list(jolt)
            for pos in button:
                jolt_list[pos] += 1
            jolt_next = tuple(jolt_list)

            if jolt_next == target:
                return presses + 1
            if jolt_next in visited:
                continue
            visited.add(jolt_next)
            if all(jolt_next[i] <= target[i] for i in range(len(target))):
                stack.append((jolt_next, presses + 1))

    raise ValueError("No solution found")


# The second function uses integer linear programming to solve the problem.
# We set up a system of linear equations where each button press is a variable,
# and each equation ensures that the total number of presses for each light
# matches the required joltage. We then minimize the sum of the button presses.
#
# So we build the matrix B that contains which buttons affect which lights:
# If buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
#
# B = [[0 0 0 0 1 1]
#      [0 1 0 0 0 1]
#      [0 0 1 1 1 0]
#      [1 1 0 1 0 0]]
#
# J = [3 5 4 7]
#
# Then we solve for x the system Bx = J where J is the joltage vector
#
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def solve_part_2(machine):
    _, _, buttons_as_list, joltage = machine

    B = np.zeros((len(joltage), len(buttons_as_list)), dtype=int)
    for i, button in enumerate(buttons_as_list):
        for j in button:
            B[j, i] = 1

    J = np.array(joltage, dtype=float)
    n_vars = len(buttons_as_list)
    c = np.ones(n_vars, dtype=float)
    constraints = LinearConstraint(B, lb=J, ub=J)
    bounds = Bounds(lb=np.zeros(n_vars), ub=np.full(n_vars, np.inf))
    integrality = np.ones(n_vars, dtype=int)  # bool is also fine

    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)
    if not result.success:
        raise ValueError("No solution found")

    x = np.rint(result.x).astype(int)
    return sum(x)


# print(sum(map(solve_part_2_only_for_example, machines)))
print(sum(map(solve_part_2, machines)))
