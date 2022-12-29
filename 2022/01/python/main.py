import sys

data = []
acc = 0

for line in sys.stdin:
    if line.isspace():
        data.append(acc)
        acc = 0
    else:
        acc += int(line)
data.append(acc)

data.sort()
print(sum(data[-3:]))
