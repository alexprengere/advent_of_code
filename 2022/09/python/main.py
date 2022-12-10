import sys
import itertools
from dataclasses import dataclass


D_INDICES = set(itertools.product((-1, 0, 1), repeat=2))


@dataclass
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


N = 10  # for part 1, use N = 2
rope = [Point(0, 0) for _ in range(N)]
head, tail = rope[0], rope[-1]
history = {(tail.x, tail.y)}

for row in sys.stdin:
    move, n = row.rstrip().split()
    for _ in range(int(n)):
        if move == "R":
            head.x += 1
        elif move == "L":
            head.x -= 1
        elif move == "U":
            head.y += 1
        elif move == "D":
            head.y -= 1

        for n1, n2 in itertools.pairwise(rope):
            if n1.distance(n2) > 1:
                n2_new = min(n2.neighbors(), key=n1.manhattan)
                n2.x, n2.y = n2_new.x, n2_new.y

        history.add((tail.x, tail.y))

print(len(history))
