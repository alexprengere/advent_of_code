import sys
import operator


def generate_operation(v1, op, v2):
    def _func(i):
        arg_0 = i if v1 == "old" else int(v1)
        arg_1 = i if v2 == "old" else int(v2)

        if op == "+":
            return arg_0 + arg_1
        elif op == "*":
            return arg_0 * arg_1
        else:
            raise Exception()

    return _func


PART = 1
monkeys = {}
monkey = None

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
        monkey["operation"] = right.split()

    elif row.startswith("Test"):
        _, _, n = row.removeprefix("Test: ").split()
        monkey["test"] = [int(n)]

    elif row.startswith("If"):
        *_, n = row.split()
        monkey["test"].append(int(n))


for monkey in monkeys.values():
    monkey["operation"] = generate_operation(*monkey["operation"])

ROUNDS = 20 if PART == 1 else 1_000

for round_ in range(1, 1 + ROUNDS):
    for number in sorted(monkeys):
        monkey = monkeys[number]
        for item in monkey["items"]:
            monkey["inspected"] += 1
            item = monkey["operation"](item)
            if PART == 1:
                item //= 3
            test, a, b = monkey["test"]
            if item % test == 0:
                target = a
            else:
                target = b
            monkeys[target]["items"].append(item)
        monkey["items"].clear()

    if round_ % 100 == 0:
        print(f"After round {round_}")
        for number in sorted(monkeys):
            inspected = monkeys[number]["inspected"]
            print(f"Monkey {number}: {inspected}")

most_active = sorted(m["inspected"] for m in monkeys.values())[-2:]
print(operator.mul(*most_active))
