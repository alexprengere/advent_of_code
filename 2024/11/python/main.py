import sys
from functools import cache

stone = list(map(int, sys.stdin.read().split()))


@cache
def count(stone, blinks):
    if blinks == 0:
        return 1

    if stone == 0:
        return count(1, blinks - 1)

    s = str(stone)
    if len(s) % 2 == 0:
        half = len(s) // 2
        left, right = int(s[:half]), int(s[half:])
        return count(left, blinks - 1) + count(right, blinks - 1)

    return count(stone * 2024, blinks - 1)


print(sum(count(stone, 25) for stone in stone))
print(sum(count(stone, 75) for stone in stone))
# print(count.cache_info())
