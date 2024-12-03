import sys

# We could have gone the regex way, but it is not as fun as writing our own
# stack-based parser. Who knows, if this exercise gets more complex, we might
# re-use this code to recursively evaluate expressions :).

PART = 2

memory = sys.stdin.read().rstrip()


def pop_last_number(stack, stop_char):
    digits = []
    while stack and (char := stack.pop()) != stop_char:
        if not char.isdigit():
            return None
        digits.append(char)
    if not digits:
        return None
    return int("".join(reversed(digits)))


do = True
stack = []
total = 0
i = 0
while i < len(memory):
    # First we read the next chars and update the index.
    if memory[i : i + 4] == "do()":
        do = True
        i += 4
    if memory[i : i + 7] == "don't()":
        do = False
        i += 7
    elif memory[i : i + 3] == "mul":
        stack.append("mul")
        i += 3
    elif memory[i] in "(,)" or memory[i].isdigit():
        stack.append(memory[i])
        i += 1
    else:
        stack.clear()
        i += 1

    # If we just closed a parenthesis, we can evaluate the expression.
    if stack and stack[-1] == ")":
        _ = stack.pop()
        n2 = pop_last_number(stack, stop_char=",")
        n1 = pop_last_number(stack, stop_char="(")
        if (
            n1 is not None
            and n2 is not None
            and stack
            and stack.pop() == "mul"
            and (PART == 1 or (PART == 2 and do))
        ):
            total += n1 * n2
            # For the record, you can put the result back in the stack if you
            # want to evaluate more complex expressions.
            # for c in str(n1 * n2):
            #     stack.append(c)


print(total)
