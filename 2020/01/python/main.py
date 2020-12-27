import sys
import itertools
import operator
from functools import reduce

data = []
for row in sys.stdin:
    data.append(int(row))

for numbers in itertools.combinations_with_replacement(data, 3):
    if sum(numbers) == 2020:
        print(reduce(operator.mul, numbers, 1))
        break
