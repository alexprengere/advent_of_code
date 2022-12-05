import sys
import re
from itertools import islice
from collections import defaultdict, deque


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


stacks = defaultdict(deque)
for row in sys.stdin:
    if not row.strip():
        break
    for n, gt in enumerate(batched(row, 4), start=1):
        if gt[1].strip():
            stacks[n].appendleft(gt[1])

REG = re.compile(r"move (\d+) from (\d+) to (\d+)")
for row in sys.stdin:
    amount, source, target = REG.match(row).groups()
    for _ in range(int(amount)):
        crate = stacks[int(source)].pop()
        stacks[int(target)].append(crate)

print("".join(stacks[n][-1] for n in sorted(stacks)))
