import sys


def part1():
    redundant = 0
    for row in sys.stdin:
        s0, s1 = row.rstrip().split(",")
        s0 = s0.split("-")
        s1 = s1.split("-")
        sections_0_limits = int(s0[0]), int(s0[1]) + 1
        sections_1_limits = int(s1[0]), int(s1[1]) + 1
        sections_0 = set(range(*sections_0_limits))
        sections_1 = set(range(*sections_1_limits))
        if sections_0 <= sections_1 or sections_1 <= sections_0:
            redundant += 1
    print(redundant)


part1()
