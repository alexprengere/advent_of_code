import sys
import itertools
import operator
from functools import reduce


def find_sum(data, N):
    for numbers in itertools.combinations_with_replacement(data, N):
        if sum(numbers) == 2020:
            return reduce(operator.mul, numbers, 1)


data = []
for row in sys.stdin:
    data.append(int(row))

print(find_sum(data, 2))
print(find_sum(data, 3))
