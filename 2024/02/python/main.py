import sys
from itertools import pairwise

_input = sys.stdin.readlines()

reports = []
for row in _input:
    reports.append(list(map(int, row.split())))


def is_safe(report):
    # Checks are not computed if not necessary
    if any(abs(a - b) not in (1, 2, 3) for a, b in pairwise(report)):
        return False
    if all(a <= b for a, b in pairwise(report)):  # all increasing
        return True
    if all(a >= b for a, b in pairwise(report)):  # all decreasing
        return True
    return False


# PART 1
#
print(sum(is_safe(report) for report in reports))


# PART 2
#
def is_safe_2(report):
    safe = is_safe(report)
    if safe:
        return True
    for i in range(len(report)):
        if is_safe([*report[:i], *report[i + 1 :]]):
            return True
    return False


print(sum(is_safe_2(report) for report in reports))
