import sys

signal = [[]]
for row in sys.stdin:
    if row.isspace():
        signal.append([])
    else:
        packet_data = eval(row.rstrip())
        signal[-1].append(packet_data)


def compare(left, right):
    if isinstance(left, list) and isinstance(right, int):
        right = [right]

    if isinstance(left, int) and isinstance(right, list):
        left = [left]

    if isinstance(left, int) and isinstance(right, int):
        return None if left == right else left < right

    if isinstance(left, list) and isinstance(right, list):
        for li, ri in zip(left, right):
            res = compare(li, ri)
            if res is not None:
                return res
        return None if len(left) == len(right) else len(left) < len(right)


total = 0
for index, (left, right) in enumerate(signal, start=1):
    if compare(left, right) is True:
        total += index
print(total)
