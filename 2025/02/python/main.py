import sys


def is_invalid_part1(n):
    n = str(n)
    half = len(n) // 2
    # Is the first half equal to the second half
    return n[:half] == n[half:]


def is_invalid_part2(n):
    n = str(n)
    length = len(n)
    for size in range(1, length // 2 + 1):
        # Check if the number can be constructed by repeating
        # a substring of size `size`, length / size times
        k, remainder = divmod(length, size)
        if remainder == 0 and n[:size] * k == n:
            return True
    return False


_input = sys.stdin.read().rstrip()

total_part_1 = 0
total_part_2 = 0

for a, b in [r.split("-") for r in _input.split(",")]:
    for n in range(int(a), int(b) + 1):
        if is_invalid_part1(n):
            total_part_1 += n
        if is_invalid_part2(n):
            total_part_2 += n

print(total_part_1)
print(total_part_2)
