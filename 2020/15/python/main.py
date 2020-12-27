import sys

numbers = []
for n in next(sys.stdin).split(","):
    numbers.append(int(n))


# PART 1: 2020
# PART 2: 30_000_000
#
TURNS = 30_000_000

last_turns = {n: turn for turn, n in enumerate(numbers[:-1], start=1)}
last_spoken = numbers[-1]

for turn in range(len(numbers) + 1, TURNS + 1):
    # "turn - 1" is the last turn where last_spoken was spoken
    # last_turns[last_spoken] is the turn before that (not updated yet to "turn - 1").
    if last_spoken in last_turns:
        spoken = turn - 1 - last_turns[last_spoken]
    else:
        spoken = 0
    last_turns[last_spoken] = turn - 1
    last_spoken = spoken

print(last_spoken)
