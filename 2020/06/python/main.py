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


groups = list(split_groups(sys.stdin))


# PART 1: set.union
#
count = 0
for group in groups:
    count += len(set.union(*(set(q) for q in group)))
print(count)


# PART 2: set.intersection
#
count = 0
for group in groups:
    count += len(set.intersection(*(set(q) for q in group)))
print(count)
