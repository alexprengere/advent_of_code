import sys
from functools import cache


@cache
def divisors(L):
    """Return all divisors of n less than n/2"""
    res = []
    for d in range(1, L // 2 + 1):
        k, rem = divmod(L, d)
        if rem == 0:
            res.append((d, k))
    return res


def is_invalid_part1(n):
    half = len(n) // 2
    return n[:half] == n[half:]


def is_invalid_part2(n):
    for d, k in divisors(len(n)):
        if n[:d] * k == n:
            return True
    return False


# Note: this can be completely solved analytically, as this is basically
# a counting problem: we need to count the numbers we can build by
# repeating substrings, in a given number range.
_input = sys.stdin.read().rstrip()

total_part_1 = 0
total_part_2 = 0

for a, b in [r.split("-") for r in _input.split(",")]:
    for i in range(int(a), int(b) + 1):
        n = str(i)
        if is_invalid_part1(n):
            total_part_1 += i
        if is_invalid_part2(n):
            total_part_2 += i

print(total_part_1)
print(total_part_2)
