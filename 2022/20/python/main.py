import sys

KEY = 811_589_153  # 1 for part 1
NB_MIXING = 10  # 1 for part 1

numbers = [int(num) * KEY for num in sys.stdin]
N = len(numbers)

before, after = [None] * N, [None] * N
for index, _ in enumerate(numbers):
    if index - 1 >= 0:
        before[index] = index - 1
    if index + 1 < len(numbers):
        after[index] = index + 1
before[0] = len(numbers) - 1
after[len(numbers) - 1] = 0


def move(before, after, index, nth):
    # nth - 1 movements = stay in the same place
    nth %= N - 1
    if nth == 0:
        return
    target = nth_after(after, index, nth)

    # 2 updated links at deletion site
    before[after[index]] = before[index]
    after[before[index]] = after[index]

    # 4 created links at creation site
    before[index] = target
    before[after[target]] = index
    after[index] = after[target]
    after[target] = index


def nth_after(after, index, nth):
    for _ in range(nth % N):
        index = after[index]
    return index


for _ in range(NB_MIXING):
    for index, num in enumerate(numbers):
        move(before, after, index, nth=num)


index_0 = numbers.index(0)
print(sum(numbers[nth_after(after, index_0, n)] for n in (1000, 2000, 3000)))
