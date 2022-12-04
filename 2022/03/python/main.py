import sys

PRIORITIES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_priority(item):
    return PRIORITIES.find(item) + 1


sum_of_priorities = 0
for row in sys.stdin:
    items = row.rstrip()
    comp_0 = items[: len(items) // 2]
    comp_1 = items[len(items) // 2:]
    common = (set(comp_0) & set(comp_1)).pop()
    sum_of_priorities += get_priority(common)
print(sum_of_priorities)
