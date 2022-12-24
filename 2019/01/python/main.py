import sys
import math


_input = sys.stdin.read()


# PART 1
#
def compute_fuel(mass):
    return max(0, math.floor(mass / 3) - 2)


print(sum(compute_fuel(int(row)) for row in _input.splitlines()))


# PART 2
#
total = 0
for row in _input.splitlines():
    mass = int(row)
    fuel = compute_fuel(mass)
    while fuel > 0:
        total += fuel
        fuel = compute_fuel(fuel)

print(total)
