import sys
import math
from heapq import heappop, heappush
import itertools
import functools

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
#
KEYPAD = {  # key => [(press, neighbor), ...]
    "0": ("^2", ">A"),
    "A": ("<0", "^3"),
    "1": (">2", "^4"),
    "2": ("v0", "<1", "^5", ">3"),
    "3": ("<2", "^6", "vA"),
    "4": ("v1", "^7", ">5"),
    "5": ("v2", "^8", "<4", ">6"),
    "6": ("v3", "^9", "<5"),
    "7": ("v4", ">8"),
    "8": ("v5", ">9", "<7"),
    "9": ("v6", "<8"),
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
#
NUMPAD = {  # key => [(press, neighbor), ...]
    "<": (">v",),
    "v": ("<<", "^^", ">>"),
    ">": ("<v", "^A"),
    "^": ("vv", ">A"),
    "A": ("<^", "v>"),
}


def shortest_presses_between_keys(start, end, neighbors):
    """
    Given a start and end position on a pad (keypad or numpad), this will
    yield all shortest paths in the form of presses.

    >>> list(shortest_presses_between_keys("A", "2", KEYPAD))
    ['<^', '^<']
    """
    shortest_dist = {start: 0}
    dist_min_to_end = None

    heap = [(0, start, [])]
    seen = set()
    while heap:
        dist_min_node, min_node, presses = heappop(heap)
        seen.add(min_node)

        if min_node == end:
            if dist_min_to_end is None:
                dist_min_to_end = dist_min_node
            elif dist_min_node > dist_min_to_end:
                break
            yield "".join(presses)

        for press, neighbor in neighbors[min_node]:
            if neighbor in seen:
                continue
            dist_neighbor = dist_min_node + 1
            if dist_neighbor < shortest_dist.get(neighbor, math.inf):
                heappush(heap, (dist_neighbor, neighbor, presses + [press]))


def shortest_presses(code, neighbors):
    """Cartesian product of shortest presses between key pairs of a code.

    This time the A keypress is added, as we need to get each code character.

    >>> list(shortest_presses("326", KEYPAD))
    ['^A<A>^A', '^A<A^>A']
    >>> list(shortest_presses("A26", KEYPAD))
    ['A<^A>^A', 'A<^A^>A', 'A^<A>^A', 'A^<A^>A']
    """
    presses_per_step = []
    prev = "A"
    for current in code:
        presses_per_step.append(
            list(shortest_presses_between_keys(prev, current, neighbors))
        )
        prev = current

    for presses in itertools.product(*presses_per_step):
        yield "A".join(presses) + "A"


def split_chunks(presses):
    chunk = []
    for char in presses:
        chunk.append(char)
        if char == "A":
            yield "".join(chunk)
            chunk.clear()


@functools.cache
def count(presses, numpad):
    # Counts the number of presses needed after passing through the numerical pads.
    if numpad == 0:
        return len(presses)

    total = 0
    for chunk in split_chunks(presses):
        total += min(count(p, numpad - 1) for p in shortest_presses(chunk, NUMPAD))
    return total


def complexity(code, numpad):
    # We first apply the shortest presses on the keypad, then call the numpad count
    min_count = min(count(p, numpad) for p in shortest_presses(code, KEYPAD))
    return min_count * int(code[:-1])


codes = []
for row in sys.stdin:
    codes.append(row.strip())

print(sum(complexity(code, numpad=2) for code in codes))
print(sum(complexity(code, numpad=25) for code in codes))
