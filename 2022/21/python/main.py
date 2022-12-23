import sys
import operator
import functools

monkeys = {}

for row in sys.stdin:
    name, job = row.rstrip().split(": ")
    try:
        job = int(job)
    except ValueError:
        name_0, op, name_1 = job.split(" ")
        if op == "+":
            op_func = operator.add
        elif op == "-":
            op_func = operator.sub
        elif op == "*":
            op_func = operator.mul
        elif op == "/":
            op_func = operator.floordiv
        monkeys[name] = [name_0, op_func, name_1]
    else:
        monkeys[name] = job


def yell(name):
    if isinstance(monkeys[name], int):
        return monkeys[name]
    name_0, op_func, name_1 = monkeys[name]
    return op_func(yell(name_0), yell(name_1))


# PART 1
#
print(yell("root"))


# PART 2 (not finished)
#
monkeys["root"][1] = operator.eq

for i in range(1_000):
    monkeys["humn"] = i
    if yell("root") is True:
        print(i)
        break
