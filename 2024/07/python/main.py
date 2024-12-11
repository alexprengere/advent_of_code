import sys
import functools
from operator import add, mul


@functools.lru_cache(maxsize=1024)
def nb_digits(x):
    if x == 0:
        return 1
    d = 0
    while x > 0:
        x //= 10
        d += 1
    return d


def concat(a, b):
    return a * (10 ** nb_digits(b)) + b


OPERATORS = {
    "+": add,
    "*": mul,
    "||": concat,
}


def find_solution(test_value, numbers, operators):
    op_functions = [OPERATORS[name] for name in operators]

    # Rather than doing the full itertools.product, we use DFS to only
    # pursue operators that do not exceed the target test_value.
    stack = [(1, numbers[0])]  # (next index in numbers, current value)
    found = False

    while stack:
        index, value = stack.pop()

        if index == len(numbers):  # terminal node, we check against test_value
            if value == test_value:
                found = True
                break
        else:
            number = numbers[index]
            for op_func in op_functions:
                new_value = op_func(value, number)

                # As numbers can only grow, only pursue if we are below target
                if new_value <= test_value:
                    stack.append((index + 1, new_value))

    return found


def main(operations, operators):
    print(
        sum(
            test_value
            for test_value, numbers in operations
            if find_solution(test_value, numbers, operators)
        )
    )


operations = []
for row in sys.stdin:
    test_value, numbers = row.split(":")
    test_value = int(test_value)
    numbers = list(map(int, numbers.split()))
    operations.append((test_value, numbers))

main(operations, ["+", "*"])
main(operations, ["+", "*", "||"])
