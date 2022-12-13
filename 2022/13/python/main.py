import sys
import ast
import itertools
import functools


def compare_signal(left, right):
    if isinstance(left, list) and isinstance(right, int):
        right = [right]

    elif isinstance(left, int) and isinstance(right, list):
        left = [left]

    elif isinstance(left, int) and isinstance(right, int):
        return left - right

    # (list, list) case
    for li, ri in zip(left, right):
        res = compare_signal(li, ri)
        if res != 0:
            return res

    return len(left) - len(right)


signal = [[]]
for row in sys.stdin:
    if row.isspace():
        signal.append([])
    else:
        packet = ast.literal_eval(row)
        signal[-1].append(packet)


# PART 1
#
total = 0
for index, (left, right) in enumerate(signal, start=1):
    if compare_signal(left, right) <= 0:  # left < right
        total += index
print(total)


# PART 2
#
dividers = [[[2]], [[6]]]

signal = list(itertools.chain.from_iterable(signal))
signal += dividers
signal.sort(key=functools.cmp_to_key(compare_signal))

decoder_key = 1
for index, packet in enumerate(signal, start=1):
    if packet in dividers:
        decoder_key *= index
print(decoder_key)
