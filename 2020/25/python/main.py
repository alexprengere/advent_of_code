import sys
import itertools

CONSTANT = 20201227


def find_loop_size(subject_number, public_key):
    value = 1
    for loop_size in itertools.count(1):
        value *= subject_number
        value %= CONSTANT
        if value == public_key:
            return loop_size


def transform(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= CONSTANT
    return value


card_public_key, door_public_key = [int(n) for n in sys.stdin.read().split()]

subject_number = 7
card_loop_size = find_loop_size(subject_number, card_public_key)
door_loop_size = find_loop_size(subject_number, door_public_key)

# Both should return the same value!
print(transform(card_public_key, door_loop_size))
print(transform(door_public_key, card_loop_size))
