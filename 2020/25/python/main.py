import sys
import itertools

SUBJECT_NUMBER = 7
CONSTANT = 20201227


def find_loop_size(public_key, subject_number=SUBJECT_NUMBER, constant=CONSTANT):
    value = 1
    for loop_size in itertools.count(1):
        value *= subject_number
        value %= constant
        if value == public_key:
            return loop_size


card_public_key, door_public_key = [int(n) for n in sys.stdin.read().split()]

door_loop_size = find_loop_size(door_public_key)
print(pow(card_public_key, door_loop_size, CONSTANT))
