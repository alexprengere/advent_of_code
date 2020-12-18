import sys
from collections import defaultdict

rules = defaultdict(list)
ticket = None
nearby = []

part = 1
for row in sys.stdin:
    row = row.rstrip()
    if not row:
        pass
    elif row.startswith("your ticket"):
        part = 2
    elif row.startswith("nearby ticket"):
        part = 3
    elif part == 1:
        field, ranges = row.split(": ")
        for limits in ranges.split(" or "):
            inf, sup = limits.split("-")
            rules[field].append((int(inf), int(sup)))
    elif part == 2:
        ticket = [int(n) for n in row.split(",")]
    elif part == 3:
        nearby.append([int(n) for n in row.split(",")])


error_rate = 0
valid_tickets = []
for _ticket in nearby:
    invalid = False
    for n in _ticket:
        if not any(any(k[0] <= n <= k[1] for k in rule) for rule in rules.values()):
            error_rate += n
            invalid = True
    if not invalid:
        valid_tickets.append(_ticket)


# PART 1
#
print(error_rate)


# PART 2
#
# First we list the possible positions for each field
possibilities = defaultdict(set)
for field, rule in rules.items():
    for pos, _ in enumerate(ticket):
        for _ticket in valid_tickets:
            if not any(k[0] <= _ticket[pos] <= k[1] for k in rule):
                break
        else:  # no break = all valid
            possibilities[field].add(pos)

# Then we iteratively reduce the possibilities when only 1 position is possible.
# Note that the loop might never break, if the simple algorithm fails to reduce
# possibilities to {}.
# In that case we would need backtracking, like a Sudoku.
certainties = {}
while possibilities:
    for field in list(possibilities):
        if len(possibilities[field]) == 1:
            certainties[field] = pos = possibilities[field].pop()
            del possibilities[field]
            for other in possibilities:  # other fields
                if pos in possibilities[other]:
                    possibilities[other].remove(pos)

product = 1
for field, pos in certainties.items():
    if field.startswith("departure"):
        product *= ticket[pos]
print(product)
