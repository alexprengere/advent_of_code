import sys


def move(cups, turns):
    min_cups, max_cups = min(cups), max(cups)

    # clockwise holds positions of the next cup
    clockwise = [0] * (len(cups) + 1)  # could be a dict as well
    for i, _ in enumerate(cups[:-1]):
        clockwise[cups[i]] = cups[i + 1]
    clockwise[cups[-1]] = cups[0]

    current_cup = cups[0]
    for _ in range(turns):
        selected = []
        selected_next = clockwise[current_cup]
        for _ in range(3):  # could be faster by rolling out the loop
            selected.append(selected_next)
            selected_next = clockwise[selected_next]
        clockwise[current_cup] = selected_next

        destination = current_cup - 1
        if destination < min_cups:
            destination = max_cups
        while destination in selected:
            destination -= 1
            if destination < min_cups:
                destination = max_cups

        # Insert the selected cups after the destination
        clockwise[selected[-1]] = clockwise[destination]
        clockwise[destination] = selected[0]

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
