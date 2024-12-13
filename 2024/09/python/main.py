import sys
from heapq import heappop, heappush
from collections import defaultdict

diskmap = sys.stdin.read().rstrip()

disk0: list[int | None] = []
file_data_per_id = {}  # for part 2
empty_positions: dict[int, list] = defaultdict(list)  # for part 2

id_ = 0
for n, c in enumerate(diskmap):
    length = int(c)
    disk_pos = len(disk0)
    if n % 2 == 0:
        if id_ not in file_data_per_id:  # first position stored
            file_data_per_id[id_] = disk_pos, length
        for _ in range(length):
            disk0.append(id_)
        id_ += 1
    else:
        # Pushing the length of the empty space in the heap
        if length > 0:
            heappush(empty_positions[length], disk_pos)
        for _ in range(length):
            disk0.append(None)

first_id, last_id = 0, id_ - 1


def checksum(disk):
    return sum(p * id_ for p, id_ in enumerate(disk) if id_ is not None)


def show_disk(disk):
    for _, id_ in enumerate(disk):
        if id_ is None:
            print(".", end="")
        else:
            print(id_, end="")
    print()


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
disk = disk0.copy()

# empty_positions is a dict of heaps, where the key is the length of the empty space
# and the value is a heap of the leftmost positions of the empty spaces of that length.
# When looking for the leftmost empty space of a certain length, we can just pop the
# heap, after selecting the leftmost position from all length-compatible heaps.
# The thing that is important: after moving a file, we do not need to update all the
# heaps, as we *know* that the spaces just freed will never be used again, as we go
# from the last file to the first, so from the right to the left.
# A small additional optimization could be to have those heaps in some kind of tree,
# so we could select the heap with compatible lengths in O(log n) time.
# Here it would make no difference as the empty lengths are small (up to 10).
for id_ in range(last_id, first_id - 1, -1):
    file_pos, file_length = file_data_per_id[id_]

    leftmost_positions = [
        (heap[0], L)
        for L, heap in empty_positions.items()
        if L >= file_length and heap[0] < file_pos
    ]
    # Having this empty means that there are no empty spaces left for the file
    if not leftmost_positions:
        continue
    empty_pos, empty_length = min(leftmost_positions)

    # We then manage the heaps for future operations
    #
    heap = empty_positions[empty_length]
    heappop(heap)  # will return empty_pos as well
    if not heap:  # if the heap is empty, we remove it
        del empty_positions[empty_length]
    # Once we will put the file in the empty position, if there are some empty spaces
    # left after the file, we will store them in the heap
    if empty_length > file_length:
        heappush(empty_positions[empty_length - file_length], empty_pos + file_length)

    # We then manage the disk
    #
    for i in range(file_length):
        disk[empty_pos + i] = id_
    for i in range(file_length):
        disk[file_pos + i] = None
    # show_disk(disk)

print(checksum(disk))
