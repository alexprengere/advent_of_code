import sys
import bisect

_ranges, _ingredients = sys.stdin.read().split("\n\n")

ranges = []
for r in _ranges.splitlines():
    start, end = map(int, r.split("-"))
    ranges.append((start, end))
    assert 0 < start <= end

ingredients = [int(i) for i in _ingredients.splitlines()]


# PART 0: computing distinct ranges
#
# Initial ranges:
# |----|
#    |---|
#            |------|
#
# After merging:
# |------|   |------|
#
distinct_ranges = []
ranges.sort()  # sort by start value
current_start, current_end = ranges[0]
for start, end in ranges:
    if start > current_end:
        distinct_ranges.append((current_start, current_end))
        current_start, current_end = start, end
    else:
        current_end = max(current_end, end)
# Append the last range
distinct_ranges.append((current_start, current_end))


# PART 1
#
# Use binary search to retrieve the range that might contain the ingredient
total_fresh = 0
for ingredient in ingredients:
    matching_range = bisect.bisect(distinct_ranges, (ingredient, ingredient))
    if matching_range == 0:  # before the first range
        continue
    start, end = distinct_ranges[matching_range - 1]
    if start <= ingredient <= end:
        total_fresh += 1
print(total_fresh)


# PART 2
#
print(sum(end - start + 1 for start, end in distinct_ranges))
