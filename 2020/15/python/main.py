import sys

numbers = []
for n in next(sys.stdin).split(","):
    numbers.append(int(n))


# PART 1: 2020
# PART 2: 30_000_000
#
TURNS = 30000000
last_spoken = None
last_turns = {}

for turn in range(1, TURNS + 1):
    if turn <= len(numbers):
        spoken = numbers[turn - 1]
    else:
        _, prev_turn = last_turns[last_spoken]
        if prev_turn is None:
            spoken = 0
        else:
            spoken = (turn - 1) - prev_turn

    # Recording 2 previous turns of spoken number
    if spoken in last_turns:
        last_turn, _ = last_turns[spoken]
    else:
        last_turn = None

    last_turns[spoken] = turn, last_turn
    last_spoken = spoken

print(last_spoken)
