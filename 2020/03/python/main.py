import sys

data = []
for row in sys.stdin:
    data.append(row.strip())
width = len(data[0])

for y_slope, x_slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    total_trees = 0
    x, y = 0, 0
    while x < len(data):
        if data[x][y % width] == "#":
            total_trees += 1
        x += x_slope
        y += y_slope
    print(total_trees)
