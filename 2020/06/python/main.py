import sys


def split_groups(rows):
    group = []
    for row in rows:
        row = row.strip()
        if not row:
            yield group
            group = []
        else:
            group.append(row)
    yield group


# PART 1: set.union
# PART 2: set.intersection
count = 0
for group in split_groups(sys.stdin):
    count += len(set.intersection(*(set(q) for q in group)))
print(count)
