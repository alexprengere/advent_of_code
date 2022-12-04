import sys

PRIORITIES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_priority(item):
    return PRIORITIES.find(item) + 1


def part1():
    sum_of_priorities = 0
    for row in sys.stdin:
        items = row.rstrip()
        comp_0 = items[: len(items) // 2]
        comp_1 = items[len(items) // 2 :]
        common = (set(comp_0) & set(comp_1)).pop()
        sum_of_priorities += get_priority(common)
    print(sum_of_priorities)


# PART 2
#
from itertools import islice


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def part2():
    sum_of_priorities = 0
    for group in batched((row.rstrip() for row in sys.stdin), 3):
        common = set.intersection(*(set(rs) for rs in group)).pop()
        sum_of_priorities += get_priority(common)
    print(sum_of_priorities)


part2()
