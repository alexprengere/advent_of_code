import sys

ROCK = 0
PAPER = 1
SCISSORS = 2

score = 0
for row in sys.stdin:
    op_move, outcome_code = row.strip().split(" ")

    if op_move == "A":
        op_shape = ROCK
    elif op_move == "B":
        op_shape = PAPER
    elif op_move == "C":
        op_shape = SCISSORS

    if outcome_code == "X":
        my_shape = (op_shape - 1) % 3
    elif outcome_code == "Y":
        my_shape = op_shape
    elif outcome_code == "Z":
        my_shape = (op_shape + 1) % 3

    score += my_shape + 1
    outcome = (my_shape - op_shape) % 3
    if outcome == 1:
        score += 6
    elif outcome == 0:
        score += 3
    elif outcome == 2:
        score += 0

print(score)
