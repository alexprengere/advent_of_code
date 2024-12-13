import sys
from operator import mul
from functools import reduce
from collections import Counter

bag = Counter({"red": 12, "green": 13, "blue": 14})

part1 = 0
part2 = 0
for row in sys.stdin:
    game_id, game = row.split(":")
    game_id = int(game_id.split()[1])

    fewest = Counter()
    for cubes in game.split(";"):
        for cube in cubes.split(","):
            count, color = cube.strip().split()
            fewest[color] = max(int(count), fewest[color])

    if fewest <= bag:  # is a valid game
        part1 += game_id
    part2 += reduce(mul, fewest.values(), 1)

print(part1)
print(part2)
