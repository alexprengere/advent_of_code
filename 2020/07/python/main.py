import sys
from collections import defaultdict

rules = defaultdict(list)

for row in sys.stdin:
    row = row.strip().split()
    color, inside = row[:2], row[4:]
    for n in range(len(inside) // 4):
        volume, *col = inside[n * 4 : n * 4 + 3]
        rules[tuple(color)].append((int(volume), tuple(col)))


# PART 1
#
stack = [("shiny", "gold")]
solutions = set()
while stack:
    target_color = stack.pop()
    for color, inside in rules.items():
        for _, col in inside:
            if col == target_color:
                if color not in solutions:
                    stack.append(color)
                    solutions.add(color)

print(len(solutions))


# PART 2
#
stack = [("shiny", "gold")]
total = 0
while stack:
    color = stack.pop()
    for n, col in rules[color]:
        for _ in range(n):
            total += 1
            stack.append(col)

print(total)
