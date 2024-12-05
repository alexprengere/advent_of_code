import sys
from collections import defaultdict
from functools import cmp_to_key

orders, updates = sys.stdin.read().split("\n\n")

greater = defaultdict(set)
for order in orders.splitlines():
    low, high = map(int, order.split("|"))
    greater[low].add(high)


def cmp(a, b):
    # This is a comparison function for sorting the numbers
    # It can be converted to a key function by using functools.cmp_to_key
    # This key function can then be used in the sort function.
    if a in greater[b]:
        return 1
    if b in greater[a]:
        return -1
    return 0


total_1, total_2 = 0, 0

for update in updates.splitlines():
    numbers = [int(x) for x in update.split(",")]
    ordered = sorted(numbers, key=cmp_to_key(cmp))
    if numbers == ordered:
        total_1 += numbers[len(numbers) // 2]
    else:
        total_2 += ordered[len(numbers) // 2]

print(total_1, total_2)
