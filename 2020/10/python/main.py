import sys
from collections import Counter

adapters = []
for row in sys.stdin:
    adapters.append(int(row))

SOURCE = 0
TARGET = max(adapters) + 3
RANGE = 3

# PART 1
#
jolts = [SOURCE] + sorted(adapters) + [TARGET]
diffs = Counter()
for i, _ in enumerate(jolts[:-1]):
    diffs[jolts[i + 1] - jolts[i]] += 1

print(diffs[1] * diffs[3])


# PART 2
#
ways = {SOURCE: 1}
for a in sorted(adapters) + [TARGET]:
    ways[a] = sum(ways.get(a - i, 0) for i in range(1 + RANGE))

print(ways[TARGET])
