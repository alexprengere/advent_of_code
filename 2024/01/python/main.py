import sys
from itertools import groupby

_input = sys.stdin.readlines()

left, right = [], []
for row in _input:
    L, R = map(int, row.split())
    left.append(L)
    right.append(R)

left.sort()
right.sort()


# PART 1
#
print(sum(abs(L - R) for L, R in zip(left, right)))


# PART 2
#
# The easy :) way to do it is to use a data structure to count the elements
# of the right list, then iterate over the left list. This can be done
# quite efficiently with collections.Counter and the likes, but there is
# a way to do it with O(1) in space complexity.
#
# We leverage the fact that both lists are already sorted, so we just have
# to iterate over both 'at the same time' and just group the elements of the
# right list together. We even group the left elements together for max speed.
#
# Because the inputs are not that big, it does not make much of a difference
# on AoC input, even more so because everything is in Python code here.

L_groups = groupby(left)
R_groups = groupby(right)

total = 0
R = -1
try:
    for L, Lg in L_groups:
        # We go to the next group of R's that matches the current L
        while R < L:
            R, Rg = next(R_groups)  # this will raise when there is no more R
        # If R > L, it means that the L value never appeared in the R list, we skip
        if R == L:
            # We do not have to store the group length as both L's and R's are grouped
            # So we will never call list() over the same group twice.
            total += L * len(list(Lg)) * len(list(Rg))
except StopIteration:
    pass

print(total)
