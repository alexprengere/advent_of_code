import re
import sys
import math

# We define the operations as functions that take a column of strings.
# This helps with part 2 where we need to reinterpret the strings.
OPERATIONS = {
    "+": lambda column: sum(map(int, column)),
    "*": lambda column: math.prod(map(int, column)),
}


def t(column):
    """Transpose a column of strings into rows.

    >>> t(['123', ' 45', '  6'])
    ['1  ', '24 ', '356']
    """
    return ["".join(row) for row in zip(*column)]


# INPUT PARSING
#
*_numbers, _operations = sys.stdin.readlines()

# Because whitespace is significant in this puzzle input, we have to keep them,
# so we first parse the "operations" line to determine column widths.
# Note that it is important the _operations ends with a single \n.
column_widths = list(map(len, re.findall(r"[*+]\s+", _operations)))

numbers = []
for row in _numbers:
    ind, line = 0, []
    for width in column_widths:
        line.append(row[ind : ind + width - 1])  # -1 to remove the space separator
        ind += width
    numbers.append(line)

columns = list(zip(*numbers))  # transpose rows to columns
functions = [OPERATIONS[op] for op in _operations.split()]

# For part 2 we just re-transpose each column before applying the operation.
# It works because we carefully preserved whitespace when parsing.
# We could also have directly re-parse the input to have the columns.
print(sum(func(column) for column, func in zip(columns, functions)))
print(sum(func(t(column)) for column, func in zip(columns, functions)))
