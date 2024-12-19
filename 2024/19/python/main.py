import sys
from functools import cache

patterns, designs = sys.stdin.read().split("\n\n")
patterns = patterns.strip().split(", ")
designs = designs.strip().splitlines()


# PART 1
#
def is_possible(target, patterns, impossible):
    for p in patterns:
        if target.startswith(p):
            remaining = target[len(p) :]
            if remaining in impossible:
                continue
            if not remaining:
                return True
            if is_possible(remaining, patterns, impossible):
                return True
            impossible.add(remaining)

    return False


# Pre-filtering the possible patterns gives a nice performance boost.
# The rest is standard BFS using recursion, plus caching of the
# impossible sub-strings already computed.
total = 0
impossible: set[str] = set()
for design in designs:
    filtered_patterns = [p for p in patterns if p in design]
    if is_possible(design, filtered_patterns, impossible):
        total += 1
print(total)


# PART 2
#
@cache
def count_ways(target):
    res = 0
    for p in filtered_patterns:
        if target.startswith(p):
            remaining = target[len(p) :]
            if remaining in impossible:
                continue
            if not remaining:
                res += 1
            else:
                res += count_ways(remaining)

    return res


# Same as before, expect we directly cache the count_ways() results.
# We also re-use the 'impossible' set for part 1.
# Small trick: we make the count_ways() function only rely on its target
# parameter, and the filtered patterns as global variable, to make
# sure the cache key does not depend on the patterns, so the cache
# is effectively shared accross designs.
total = 0
for design in designs:
    filtered_patterns = [p for p in patterns if p in design]
    total += count_ways(design)
print(total)
