import sys

_input = sys.stdin.readlines()

# PART 1
#
total = 0
for row in _input:
    digits = [c for c in row if c.isdigit()]
    total += int(f"{digits[0]}{digits[-1]}")

print(total)


# PART 2
#
numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
MIN_NUMBER_LENGTH = min(len(s) for s in numbers)
MAX_NUMBER_LENGTH = max(len(s) for s in numbers)

total = 0
for row in _input:
    digits = []
    for n, _ in enumerate(row):
        if row[n].isdigit():
            digits.append(row[n])
        else:
            for i in range(MIN_NUMBER_LENGTH - 1, MAX_NUMBER_LENGTH + 1):
                last_i_chars = row[n - i: n + 1]
                if last_i_chars in numbers:
                    digits.append(numbers[last_i_chars])
                    break
    total += int(f"{digits[0]}{digits[-1]}")

print(total)
