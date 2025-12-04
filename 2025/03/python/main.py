import sys
from operator import itemgetter

_input = sys.stdin.readlines()


def find_max_joltage(bank, ndigits):
    # The algorithm finds the maximum joltage number, by figuring out
    # each digit from most significant to least significant. We just
    # find the maximum digit for each position, excluding the digits
    # of the end of the bank, starting from the last found maximum index.
    enumerated_bank = list(enumerate(bank))
    max_index = -1
    joltage = 0
    for k in range(ndigits - 1, -1, -1):  # 6 => [5, 4, 3, 2, 1, 0]
        slice_ = slice(max_index + 1, -k if k > 0 else None)
        max_index, max_n = max(enumerated_bank[slice_], key=itemgetter(1))
        joltage += max_n * (10**k)
    return joltage


def monotonic_decreasing_stack(bank, ndigits):
    # The algorithm builds a monotonic decreasing stack of digits,
    # by iterating over the bank from left to right, and popping
    # elements from the stack while the current digit is greater
    # than the top of the stack. The stack is limited to ndigits
    # elements.
    # Even though this solution is algorithmically more efficient,
    # in practice it is slower than solution based on repeated max(),
    # because the bank length is small.
    stack = []
    for index, n in enumerate(bank):
        # If the remaining bank is smaller than the ndigits we need,
        # then we cannot pop any more elements from the stack, and
        # we just append. Note that in that case the stack is no
        # longer monotonic decreasing.
        while stack and n > stack[-1] and ndigits - len(stack) < len(bank) - index:
            stack.pop()
        if len(stack) < ndigits:
            stack.append(n)

    return sum(n * (10**k) for k, n in enumerate(reversed(stack)))


def main(ndigits):
    total = 0
    for row in _input:
        bank = list(map(int, row.strip()))
        total += find_max_joltage(bank, ndigits)
        # total += monotonic_decreasing_stack(bank, ndigits)
    print(total)

main(ndigits=2)
main(ndigits=12)
