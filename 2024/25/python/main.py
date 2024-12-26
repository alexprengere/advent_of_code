import sys
from itertools import product

_input = map(str.splitlines, sys.stdin.read().split("\n\n"))

locks, keys = [], []

for lines in _input:
    if lines[0] == "#####":
        locks.append([column.index(".") for column in zip(*lines)])
    else:
        keys.append([column.index("#") for column in zip(*lines)])

# L <= K means that the lock is higher than the key, on that column
print(sum(all(L <= K for L, K in zip(*pair)) for pair in product(locks, keys)))
