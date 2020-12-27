import sys


def memory_game(numbers, turns):
    last_turns = {n: turn for turn, n in enumerate(numbers[:-1], start=1)}
    last_spoken = numbers[-1]

    for turn_1 in range(len(numbers), turns):
        # turn_1 is "turn - 1": the last turn where last_spoken was spoken
        # last_turns[last_spoken] is the turn before that (not updated yet to "turn - 1").
        last_turn = last_turns.get(last_spoken, turn_1)
        last_turns[last_spoken] = turn_1
        last_spoken = turn_1 - last_turn

    return last_spoken


numbers = []
for n in next(sys.stdin).split(","):
    numbers.append(int(n))


# PART 1: 2020
# PART 2: 30_000_000
#
print(memory_game(numbers, 2020))
print(memory_game(numbers, 30_000_000))
