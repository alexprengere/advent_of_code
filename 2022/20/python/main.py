import sys
from collections import deque

KEY = 811_589_153  # 1 for part 1
NB_MIXING = 10  # 1 for part 1
SHIFT = 1000, 2000, 3000

# Numbers are replaced by their position in input,
# this is to deal with duplicates.
# Actual numbers are called values here.
values = [int(v) * KEY for v in sys.stdin]
numbers = deque(range(len(values)))
N = len(numbers)

for _ in range(NB_MIXING):
    for num, val in enumerate(values):
        val %= N - 1
        index = numbers.index(num)
        numbers.rotate(N - 1 - index)
        numbers.pop()  # popping num from tail
        numbers.rotate(-val)
        numbers.append(num)


num_0 = values.index(0)
index_0 = numbers.index(num_0)

print(sum(values[numbers[(index_0 + i) % N]] for i in SHIFT))
