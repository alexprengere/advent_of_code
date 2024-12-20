import sys
from functools import cache

patterns, designs = sys.stdin.read().split("\n\n")
patterns = patterns.strip().split(", ")
designs = designs.strip().splitlines()


@cache
def count_ways(target):
    if not target:
        return 1
    res = 0
    for p in filtered_patterns:
        if target.startswith(p):
            res += count_ways(target[len(p) :])
    return res


# Small trick: we make the count_ways() function only rely on its 'target' parameter,
# and the filtered patterns as global variable, to make sure the cache key does not
# depend on 'filtered patterns', so the cache is effectively shared accross 'designs'.
total_1, total_2 = 0, 0

for design in designs:
    filtered_patterns = [p for p in patterns if p in design]
    count = count_ways(design)
    total_1 += bool(count)
    total_2 += count

print(total_1)
print(total_2)
