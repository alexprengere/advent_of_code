import sys
from itertools import islice

numbers = []
for row in sys.stdin:
    numbers.append(int(row))


# PART 1
#
PREAMBLE = 25
for position, value in islice(enumerate(numbers), PREAMBLE, None):
    prev_numbers = numbers[position - PREAMBLE : position]
    sums = set(a + b for a in prev_numbers for b in prev_numbers if a != b)
    if value not in sums:
        N = value
        print(N)
        break


# PART 2
#
for start_position, start_value in enumerate(numbers):
    total = start_value
    for position, value in enumerate(numbers[start_position + 1:]):
        total += value
        if total == N:
            values = numbers[start_position : start_position + position + 1]
            print(min(values) + max(values))
