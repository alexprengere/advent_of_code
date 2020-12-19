import sys


def extract_sub_expression(tokens):
    sub_expression = []
    nested = 0
    while tokens:
        token = tokens.pop()
        if token == ")" and nested == 0:
            break
        sub_expression.append(token)
        if token == "(":
            nested += 1
        elif token == ")":
            nested -= 1
    return sub_expression


def evaluate(expression, part):
    result = None
    operator = None
    stack = []

    tokens = expression[::-1]
    while tokens:
        token = tokens.pop()
        if token in "+*":
            operator = token
            continue

        if token == "(":
            n = evaluate(extract_sub_expression(tokens), part)
        else:  # number
            n = int(token)

        if result is None:
            result = n
        elif operator == "+":
            result += n
        elif operator == "*" and part == 1:
            result *= n
        elif operator == "*" and part == 2:
            stack.append(result)
            result = n

    for n in stack:
        result *= n
    return result


def parse(row):
    return row.rstrip().replace("(", "( ").replace(")", " )").split()


# PART 1: evaluate with part=1
# PART 2: evaluate with part=2
#
total = 0
for row in sys.stdin:
    total += evaluate(parse(row), part=2)
print(total)
