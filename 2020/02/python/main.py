import sys

rows = list(sys.stdin)

total_valid_1 = 0
total_valid_2 = 0

for row in rows:
    digits, letter, password = row.strip().split()
    digits = [int(n) for n in digits.split("-", 1)]
    letter = letter.rstrip(":")
    if digits[0] <= password.count(letter) <= digits[1]:
        total_valid_1 += 1
    if sum(password[n - 1] == letter for n in digits) == 1:
        total_valid_2 += 1

print(total_valid_1)
print(total_valid_2)
