import sys
from operator import itemgetter

_input = sys.stdin.readlines()


def find_max_joltage(bank, ndigits):
    # The algorithm finds the maximum joltage number, by figuring out
    # each digit from most significant to least significant. We just
    # find the maximum digit for each position, excluding the digits
    # of the end of the bank, starting from the last found maximum index.
    max_index = -1
    joltage = 0
    for k in range(ndigits - 1, -1, -1):  # 6 => [5, 4, 3, 2, 1, 0]
        slice_ = slice(max_index + 1, -k if k > 0 else None)
        max_index, max_n = max(bank[slice_], key=itemgetter(1))
        joltage += max_n * (10**k)
    return joltage


def main(ndigits):
    total = 0
    for row in _input:
        bank = list(enumerate(map(int, row.strip())))
        total += find_max_joltage(bank, ndigits)
    print(total)


main(ndigits=2)
main(ndigits=12)
