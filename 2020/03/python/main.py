import sys

data = []
for row in sys.stdin:
    data.append(row.strip())


for y_slope, x_slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    total_trees = 0
    x, y = 0, 0
    while x + 1 < len(data):
        x = x + x_slope
        y = y + y_slope
        if data[x][y % len(data[x])] == "#":
            total_trees += 1
    print(total_trees)
