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

N = 10  # for part 1, use N = 2
rope = [Point(0, 0) for _ in range(N)]

# In history we store copies using dataclasses.replace
history = [[dataclasses.replace(n) for n in rope]]

for move, n in moves:
    for _ in range(n):
        if move == "R":
            rope[0].x += 1
        elif move == "L":
            rope[0].x -= 1
        elif move == "U":
            rope[0].y += 1
        elif move == "D":
            rope[0].y -= 1

        for n1, n2 in itertools.pairwise(rope):
            if n1.distance(n2) > 1:
                n2_new = min(n2.neighbors(), key=n1.manhattan)
                n2.x, n2.y = n2_new.x, n2_new.y

        history.append([dataclasses.replace(n) for n in rope])

print(len(set((t.x, t.y) for *_, t in history)))
