import sys
import re
import math
from itertools import combinations


def floyd_warhshall(graph):
    dist = {}
    for node in graph:
        dist[node] = {n: math.inf for n in graph}
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
    is_open = {v: False for v in FLOWS}
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
        is_open[position] = True
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
REMAINING_TIME = 26
START = "AA"

results = {}
stack = [((), set(FLOWS))]

while stack:
    path, todo = stack.pop()
    if not todo:
        score, _, _ = play(path, START, REMAINING_TIME)
        results[path] = score

    for done in todo:
        new_path = path + (done,)
        new_todo = todo - {done}

        score, *state = play(new_path, START, REMAINING_TIME)
        upper_bound = compute_upper_bound(new_todo, *state)
        results[new_path] = score
        # Here we cannot cut the tree, as we are not trying
        # to only get the best score. We want all scores for later.
        if upper_bound > 0:
            stack.append((new_path, new_todo))


# Mostly to speed things up, we precompute the best score per
# path set of points.
results_by_set = {}
for path, score in results.items():
    key = frozenset(path)
    if key not in results_by_set or results_by_set[key] < score:
        results_by_set[key] = score

print(
    max(
        s1 + s2
        for (p1, s1), (p2, s2) in combinations(results_by_set.items(), r=2)
        if not (p1 & p2)
    )
)
