import sys
import itertools

timestamp = int(next(sys.stdin))
buses = [
    (bn, int(bus))
    for bn, bus in enumerate(next(sys.stdin).rstrip().split(","))
    if bus != "x"
]


# PART 1
#
wait_duration = []
for _, bus in buses:
    wait_duration.append((-timestamp % bus, bus))

print(min(wait_duration))


# PART 2
#
# Chinese remainder theorem
total, step = 0, 1
for bn, bus in buses:
    for c in itertools.count(total, step):
        if (c + bn) % bus == 0:
            total, step = c, step * bus
            break

print(total)
