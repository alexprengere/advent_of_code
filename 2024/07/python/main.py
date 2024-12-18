import sys
from operator import add, mul
import multiprocessing


def concat(a, b):
    offset = 1
    while offset <= b:
        offset *= 10
    return a * offset + b


OPERATORS = {
    "+": add,
    "*": mul,
    "||": concat,
}


def search(test_value, numbers, operators):
    op_functions = [OPERATORS[name] for name in operators]

    # Rather than doing the full itertools.product, we use DFS to only
    # pursue operators that do not exceed the target test_value.
    stack = [(1, numbers[0])]  # (next index in numbers, current value)

    while stack:
        index, value = stack.pop()

        if index == len(numbers):  # terminal node, we check against test_value
            if value == test_value:
                return test_value
        else:
            number = numbers[index]
            for op_func in op_functions:
                new_value = op_func(value, number)

                # As numbers can only grow, only pursue if we are below target
                if new_value <= test_value:
                    stack.append((index + 1, new_value))

    return 0  # never found


def main(pool, operations, operators):
    results = pool.starmap(
        search,
        [(test_value, numbers, operators) for test_value, numbers in operations],
    )
    print(sum(results))


operations = []
for row in sys.stdin:
    test_value, numbers = row.split(":")
    test_value = int(test_value)
    numbers = list(map(int, numbers.split()))
    operations.append((test_value, numbers))

with multiprocessing.Pool() as pool:
    main(pool, operations, ["+", "*"])
    main(pool, operations, ["+", "*", "||"])
