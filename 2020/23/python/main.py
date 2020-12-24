import sys


def move(cups, turns):
    min_cup, max_cup = min(cups), max(cups)

    # clockwise holds positions of the clockwise neighbor cup
    # First min_cup positions will never be used.
    clockwise = [0] * (len(cups) + min_cup)
    for i, _ in enumerate(cups[:-1]):
        clockwise[cups[i]] = cups[i + 1]
    clockwise[cups[-1]] = cups[0]

    current_cup = cups[0]
    for _ in range(turns):
        # Ugly, but faster than an explicit for loop ;)
        picked = [
            clockwise[current_cup],
            clockwise[clockwise[current_cup]],
            clockwise[clockwise[clockwise[current_cup]]],
        ]

        # Finding the destination cup
        destination = current_cup - 1
        if destination < min_cup:
            destination = max_cup
        while destination in picked:
            destination -= 1
            if destination < min_cup:
                destination = max_cup

        # New neighbor of current cup is the neighbor of the last picked
        clockwise[current_cup] = clockwise[picked[-1]]

        # Insert the picked cups after the destination
        clockwise[picked[-1]] = clockwise[destination]
        clockwise[destination] = picked[0]

        # New current cup is the clockwise neighbor
        current_cup = clockwise[current_cup]

    return clockwise


# PART 1
#
cups = [int(c) for c in sys.stdin.read().strip()]
clockwise = move(cups, 100)

cup = clockwise[1]
result = []
for _ in range(len(cups) - 1):
    result.append(str(cup))
    cup = clockwise[cup]
print("".join(result))


# PART 2
#
cups += range(1 + max(cups), 1 + 1_000_000)
clockwise = move(cups, 10_000_000)
print(clockwise[1] * clockwise[clockwise[1]])
