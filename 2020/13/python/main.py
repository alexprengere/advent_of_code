import sys
import itertools

timestamp = int(next(sys.stdin))
buses = [
    (bn, int(bus))
    for bn, bus in enumerate(next(sys.stdin).rstrip().split(","))
    if bus != "x"
]


def chinese_remainder_theorem(data):
    total, step = 0, 1
    for remainder, integer in data:
        for c in itertools.count(total, step):
            if (c + remainder) % integer == 0:
                total, step = c, step * integer
                break
    return total


# PART 1
#
waiting_time = []
for _, bus in buses:
    waiting_time.append((-timestamp % bus, bus))

time, bus = min(waiting_time)
print(time * bus)


# PART 2
#
print(chinese_remainder_theorem(buses))
