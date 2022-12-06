import sys

signal = sys.stdin.read().rstrip()

size = 14  # part 1: put 4 instead
for n in range(size, len(signal) + 1):
    if len(set(signal[n - size : n])) == size:
        print(n)
        break
