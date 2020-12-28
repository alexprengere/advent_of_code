import sys
from itertools import islice

PREAMBLE = 25


def find_invalid_number(numbers, preamble=PREAMBLE):
    for position, value in islice(enumerate(numbers), preamble, None):
        prev_numbers = numbers[position - preamble : position]
        sums = set(a + b for a in prev_numbers for b in prev_numbers if a != b)
        if value not in sums:
            return value


def find_encryption_weakness(numbers, invalid_number):
    for start_position, start_value in enumerate(numbers):
        total = start_value
        for position, value in enumerate(numbers[start_position + 1 :]):
            total += value
            if total == invalid_number:
                values = numbers[start_position : start_position + position + 1]
                return min(values) + max(values)


numbers = []
for row in sys.stdin:
    numbers.append(int(row))


# PART 1
#
invalid_number = find_invalid_number(numbers)
print(invalid_number)


# PART 2
#
print(find_encryption_weakness(numbers, invalid_number))
