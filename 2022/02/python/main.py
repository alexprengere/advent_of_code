import sys

ROCK = 1
PAPER = 2
SCISSORS = 3

score = 0
for row in sys.stdin:
    op_move, my_move = row.strip().split(" ")

    if op_move == "A":
        op_shape = ROCK
    elif op_move == "B":
        op_shape = PAPER
    elif op_move == "C":
        op_shape = SCISSORS

    if my_move == "X":
        my_shape = ROCK
    elif my_move == "Y":
        my_shape = PAPER
    elif my_move == "Z":
        my_shape = SCISSORS

    score += my_shape
    outcome = (my_shape - op_shape) % 3
    if outcome == 1:
        score += 6
    elif outcome == 0:
        score += 3
    elif outcome == 2:
        score += 0

print(score)
