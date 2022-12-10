import sys
import dataclasses
import itertools


D_INDICES = set(itertools.product((-1, 0, 1), repeat=2))


@dataclasses.dataclass(eq=True)
class Point:
    x: int
    y: int

    def neighbors(self):
        for dx, dy in D_INDICES:
            yield Point(self.x + dx, self.y + dy)

    def distance(self, p):
        return max(abs(self.x - p.x), abs(self.y - p.y))

    def manhattan(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)


moves = []
for row in sys.stdin:
    move, n = row.rstrip().split()
    moves.append((move, int(n)))

# In positions we store copies using dataclasses.replace
h, t = Point(0, 0), Point(0, 0)
positions = [[dataclasses.replace(h), dataclasses.replace(t)]]

for move, n in moves:
    for _ in range(n):
        if move == "R":
            h.x += 1
        elif move == "L":
            h.x -= 1
        elif move == "U":
            h.y += 1
        elif move == "D":
            h.y -= 1

        if h.distance(t) > 1:
            t = min(t.neighbors(), key=h.manhattan)

        positions.append([dataclasses.replace(h), dataclasses.replace(t)])


# from pprint import pprint
# pprint(positions)

print(len(set((t.x, t.y) for _, t in positions)))

"""
min_x = min(h.x for h, _ in positions)
max_x = max(h.x for h, _ in positions)
min_y = min(h.y for h, _ in positions)
max_y = max(h.y for h, _ in positions)

for hy in range(max_y, min_y - 1, -1):
    for hx in range(min_x, max_x + 1):
        try:
            turn = 1
        except ValueError:
            print(".", end="")
        else:
            print(f"{turn % 10}", end="")
    print()
"""

