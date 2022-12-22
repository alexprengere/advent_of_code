import sys
import re
import math
from itertools import combinations
from collections import defaultdict


def floyd_warhshall(graph):
    dist = {}
    for node in graph:
        dist[node] = {n: math.inf for n in graph}
        dist[node][node] = 0
        for neighbor in graph[node]:
            dist[node][neighbor] = 1

    for r in graph:
        for p in graph:
            for q in graph:
                dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])

    return dist


_regex = re.compile(
    r"^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
)
_graph = {}
_flows = {}
for row in sys.stdin:
    valve, flow, leads_to = _regex.match(row.rstrip()).groups()
    _graph[valve] = leads_to.split(", ")
    _flows[valve] = int(flow)


FLOWS = {v: f for v, f in _flows.items() if f > 0}
DISTANCES = floyd_warhshall(_graph)


def play(path, start, remaining_time):
    # Play out a given path from a starting point
    path = iter(path)
    total_pressure = 0
    total_flow = 0

    target = next(path)
    wait = DISTANCES[start][target]
    while remaining_time >= 1:
        remaining_time -= 1
        total_pressure += total_flow
        if wait > 0:
            wait -= 1
            continue
        position = target
        total_flow += FLOWS[position]
        try:
            target = next(path)
            wait = DISTANCES[position][target]
        except StopIteration:
            break

    for _ in range(remaining_time):
        total_pressure += total_flow

    # We return the remaining time when the player
    # stopped moving, this is useful to determine
    # upper bounds of scores later.
    return total_pressure, position, remaining_time


def compute_upper_bound(todo, position, remaining_time):
    # This computes the max. pressure you would have
    # if you could magically turn on all remaining valves,
    # from a given position, all at once.
    total_pressure = 0
    distances_from_position = DISTANCES[position]
    for valve in todo:
        flow_time = remaining_time - distances_from_position[valve] - 1
        if flow_time > 0:
            total_pressure += FLOWS[valve] * flow_time
    return total_pressure


# PART 1
#
REMAINING_TIME = 30
START = "AA"

best_score = -1
stack = [((), set(FLOWS))]

while stack:
    path, todo = stack.pop()
    if not todo:
        score, _, _ = play(path, START, REMAINING_TIME)
        if score > best_score:
            best_score = score

    for done in todo:
        new_path = path + (done,)
        new_todo = todo - {done}

        score, *state = play(new_path, START, REMAINING_TIME)
        upper_bound = compute_upper_bound(new_todo, *state)
        if upper_bound == 0:
            # Here this means that we do not need to visit new_todo
            # as the upper bound is 0. Most likely due to lack of time.
            if score > best_score:
                best_score = score
        # Branch & bound strategy, we only visit if score + upper bound
        # can beat the current best score
        elif score + upper_bound > best_score:
            stack.append((new_path, new_todo))

print(best_score)


# PART 2
#
MASK = {f: 1 << i for i, f in enumerate(FLOWS)}

REMAINING_TIME = 26
START = "AA"

# 'results' stores the path as a bitmask, which is way faster
# than storing frozenset(path) for the key. This works because
# there are not that many valves.
results = defaultdict(int)
stack = [(0, (), set(FLOWS))]

while stack:
    bits, path, todo = stack.pop()
    if not todo:
        score, _, _ = play(path, START, REMAINING_TIME)
        results[bits] = max(results[bits], score)

    for done in todo:
        new_bits = bits | MASK[done]
        new_path = path + (done,)
        new_todo = todo - {done}

        score, *state = play(new_path, START, REMAINING_TIME)
        upper_bound = compute_upper_bound(new_todo, *state)
        results[new_bits] = max(results[new_bits], score)
        # Here we cannot cut the tree, as we are not trying
        # to only get the best score. We want all scores for later.
        if upper_bound > 0:
            stack.append((new_bits, new_path, new_todo))

print(
    max(
        s1 + s2
        for (p1, s1), (p2, s2) in combinations(results.items(), r=2)
        if not (p1 & p2)
    )
)
