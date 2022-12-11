import sys
import math
import heapq


def gen_func(v1, op, v2):
    # This function could be cleaner, but it has been tweaked for speed :)
    if (v1, op, v2) == ("old", "*", "old"):
        return lambda i: i * i  # faster than i ** 2
    if (v1, op, v2) == ("old", "+", "old"):
        return lambda i: i + i  # faster than i * 2

    # In the remaining case if should always be ("old", op, <int>)
    v2 = int(v2)
    if op == "*":
        return lambda i: i * v2
    if op == "+":
        return lambda i: i + v2

    raise Exception(f"Should not happen for {v1} {op} {v2}")


monkeys = {}
divisors = []

for row in sys.stdin:
    row = row.strip()
    if row.startswith("Monkey"):
        _, number = row[:-1].split()
        monkeys[int(number)] = monkey = {"inspected": 0}

    elif row.startswith("Starting"):
        items = row.removeprefix("Starting items: ").split(", ")
        monkey["items"] = [int(i) for i in items]

    elif row.startswith("Operation"):
        operation = row.removeprefix("Operation: ")
        _, _, right = operation.partition(" = ")
        monkey["operation"] = gen_func(*right.split())

    elif row.startswith("Test"):
        _, _, n = row.removeprefix("Test: ").split()
        monkey["test"] = [int(n)]
        divisors.append(int(n))

    elif row.startswith("If"):
        *_, n = row.split()
        monkey["test"].append(int(n))


LCM = math.lcm(*divisors)
PART = 2
ROUNDS = 20 if PART == 1 else 10_000

for _ in range(ROUNDS):
    for number in monkeys:  # should be sorted per input order
        monkey = monkeys[number]
        for item in monkey["items"]:
            monkey["inspected"] += 1
            item = monkey["operation"](item)
            if PART == 1:
                item //= 3
            else:  # optimisation, not necessary
                item %= LCM
            divisor, a, b = monkey["test"]
            target = a if item % divisor == 0 else b
            monkeys[target]["items"].append(item)
        monkey["items"].clear()

most_active = heapq.nlargest(2, (m["inspected"] for m in monkeys.values()))
print(math.prod(most_active))
