import sys
from collections import defaultdict


def find_bags_containing(rules, searched_color):
    solutions = set()
    stack = [searched_color]
    while stack:
        target_color = stack.pop()
        for color, inside in rules.items():
            for _, col in inside:
                if col == target_color:
                    if color not in solutions:
                        stack.append(color)
                        solutions.add(color)
    return len(solutions)


def find_bags_inside(rules, root_color):
    total = 0
    stack = [root_color]
    while stack:
        color = stack.pop()
        for n, col in rules[color]:
            for _ in range(n):
                total += 1
                stack.append(col)
    return total


# READING INPUT
#
rules = defaultdict(list)

for row in sys.stdin:
    row = row.strip().split()
    color, inside = row[:2], row[4:]
    for n in range(len(inside) // 4):
        volume, *col = inside[n * 4 : n * 4 + 3]
        rules[tuple(color)].append((int(volume), tuple(col)))


# PART 1
#
print(find_bags_containing(rules, ("shiny", "gold")))


# PART 2
#
print(find_bags_inside(rules, ("shiny", "gold")))
