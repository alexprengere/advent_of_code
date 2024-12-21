import sys


def search(test_value, numbers, part=1):
    # Rather than going from the initial number to the target test_value, we
    # go from the target test_value to the initial number. This way we can
    # stop early of it turns out the current value is not reachable using
    # the available operators (for example, if the current value cannot be
    # the result of a multiplication or concatenation of the previous value).
    stack = [(-1, test_value)]  # (next index in numbers, current value)

    while stack:
        index, value = stack.pop()

        if index == -len(numbers):  # terminal node
            if numbers[0] == value:
                return True
            continue

        # First we check if the current value is reachable using addition
        # value = 185, numbers[index] = 5 => new_value = 180
        if value >= numbers[index]:
            stack.append((index - 1, value - numbers[index]))

        # Second we check if the current value is reachable using multiplication
        # value = 190, numbers[index] = 10 => new_value = 19
        if value % numbers[index] == 0:
            stack.append((index - 1, value // numbers[index]))

        if part == 1:
            continue
        # Third we check if the current value is reachable using concatenation
        # value = 123456, numbers[index] = 56 => new_value = 1234
        value_s = str(value)
        number_s = str(numbers[index])
        if len(value_s) > len(number_s) and value_s.endswith(number_s):
            stack.append((index - 1, int(value_s[: -len(number_s)])))

    return False


def main(operations, part):
    total = 0
    for test_value, numbers in operations:
        if search(test_value, numbers, part):
            total += test_value
    print(total)


operations = []
for row in sys.stdin:
    test_value, numbers = row.split(":")
    test_value = int(test_value)
    numbers = list(map(int, numbers.split()))
    operations.append((test_value, numbers))

main(operations, part=1)
main(operations, part=2)
