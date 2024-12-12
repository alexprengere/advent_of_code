import sys

diskmap = sys.stdin.read().rstrip()

disk0: list[int | None] = []
id_ = 0
file_lengths_per_id = {}
file_positions_per_id = {}

for n, c in enumerate(diskmap):
    length = int(c)
    disk_pos = len(disk0)
    if n % 2 == 0:
        file_lengths_per_id[id_] = length
        if id_ not in file_positions_per_id:
            file_positions_per_id[id_] = disk_pos
        for _ in range(length):
            disk0.append(id_)
        id_ += 1
    else:
        for _ in range(length):
            disk0.append(None)

first_id, last_id = 0, id_ - 1


def checksum(disk):
    return sum(p * id_ for p, id_ in enumerate(disk) if id_ is not None)


# PART 1
#
def get_last_file_positions(disk):
    for i in range(len(disk) - 1, -1, -1):
        if disk[i] is not None:
            yield i


def get_first_empty_positions(disk):
    for i in range(len(disk)):
        if disk[i] is None:
            yield i


disk = disk0.copy()
last_file_positions = get_last_file_positions(disk)
first_empty_positions = get_first_empty_positions(disk)

while True:
    file_pos = next(last_file_positions)
    empty_pos = next(first_empty_positions)
    if file_pos <= empty_pos:
        break
    disk[file_pos], disk[empty_pos] = disk[empty_pos], disk[file_pos]

print(checksum(disk))


# PART 2
#
def find_empty_continuous_space(disk, min_length, min_position, max_position):
    current_length = 0
    for i in range(min_position, max_position + 1):
        if disk[i] is None:
            if current_length == min_length - 1:
                return i - min_length + 1
            current_length += 1
        else:
            current_length = 0

    return None


first_empty_position = 0
disk = disk0.copy()
for id_ in range(last_id, first_id - 1, -1):
    file_pos = file_positions_per_id[id_]
    file_length = file_lengths_per_id[id_]

    empty_pos = find_empty_continuous_space(
        disk,
        min_length=file_length,
        min_position=first_empty_position,
        max_position=file_pos - 1,
    )
    if empty_pos is None:  # no continuous space found
        continue
    # Optimizing the search: we do not keep track of "min position per empty size",
    # as it is non trivial to merge those when files are moved, but it is easy to
    # never search before the first empty position, as this one can only move forward
    if file_length == 1:
        first_empty_position = empty_pos + file_length

    # Moving the file to the empty position, then emptying the previous position
    for i in range(file_length):
        disk[empty_pos + i] = id_
    for i in range(file_length):
        disk[file_pos + i] = None

print(checksum(disk))
