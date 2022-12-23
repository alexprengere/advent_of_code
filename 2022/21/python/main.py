import sys
import operator
from collections import deque

monkeys = {}

for row in sys.stdin:
    name, job = row.rstrip().split(": ")
    try:
        num = int(job)
    except ValueError:
        name_0, symbol, name_1 = job.split(" ")
        if symbol == "+":
            op = operator.add
        elif symbol == "-":
            op = operator.sub
        elif symbol == "*":
            op = operator.mul
        elif symbol == "/":
            op = operator.truediv
        monkeys[name] = [name_0, op, name_1]
    else:
        monkeys[name] = num


def yell(name):
    if isinstance(monkeys[name], (int, float)):
        return monkeys[name]
    name_0, op, name_1 = monkeys[name]
    return op(yell(name_0), yell(name_1))


# PART 1
#
print(int(yell("root")))


# PART 2
#
# We treat this as an optimization problem where the root
# monkey returns the difference between the 2 inputs.
# We want to converge towards 0 using gradient descent.
monkeys["root"][1] = lambda a, b: abs(b - a)


def f(x):
    monkeys["humn"] = x  # modifying global state
    return yell("root")


last_df_signs = deque(maxlen=10)
rate = 10_000_000_000
x, e = 0, 0.1

while abs(f(x)) >= 0.1:
    df = (f(x + e) - f(x)) / e
    last_df_signs.append(1 if df > 0 else -1)
    if len(set(last_df_signs)) == 2:  # oscillating gradient
        rate /= 2
    x -= round(rate * df)

print(x)
