import sys

total_valid = 0
for row in sys.stdin:
    range_, letter, password = row.strip().split()
    first, last = range_.split("-", 1)
    letter = letter.rstrip(":")
    if sum(password[int(pos) - 1] == letter for pos in (first, last)) == 1:
        total_valid += 1
print(total_valid)
