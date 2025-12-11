import sys
from functools import cache

graph = {}
for row in sys.stdin:
    source, target = row.rstrip().split(": ")
    graph[source] = target.split()


# PART 1
#
@cache
def count_paths_1(node, target):
    if node == target:
        return 1
    return sum(count_paths_1(n, target) for n in graph.get(node, []))


print(count_paths_1("you", "out"))


# PART 2
#
@cache
def count_paths_2(node, target, required):
    required -= {node, target}  # this creates a new frozenset without 'node'
    if node == target:
        return 0 if required else 1

    return sum(count_paths_2(n, target, required) for n in graph.get(node, []))


print(count_paths_2("svr", "out", frozenset({"dac", "fft"})))

# PART 2 - alternative solution
#
# Fun fact: since there can be no cycles (otherwise PART 1 would be infinite),
# you can decompose the path counting in PART 2 into independent segments and
# just re-use count_paths_1 to compute the same result.
# All paths from A to C via B are just paths from A to B times paths from B to C.
#
# import math
# from itertools import starmap, pairwise
# path_1 = ["svr", "fft", "dac", "out"]
# path_2 = ["svr", "dac", "fft", "out"]  # is 0 on AoC input
# print(math.prod(starmap(count_paths_1, pairwise(path_1))))
# print(math.prod(starmap(count_paths_1, pairwise(path_2))))
