import sys

BASE, SHIFT = 5, -2


def from_snafu(s):
    n = 0
    for cn, c in enumerate(reversed(s)):
        if c == "=":
            r = -2
        elif c == "-":
            r = -1
        else:
            r = int(c)
        n += r * BASE**cn
    return n


def to_snafu(n):
    res = []
    while n > 0:
        rem = (n - SHIFT) % BASE + SHIFT
        n = (n - SHIFT) // BASE
        if rem == -2:
            c = "="
        elif rem == -1:
            c = "-"
        else:
            c = str(rem)
        res.append(c)
    return "".join(res[::-1])


_input = sys.stdin.read().splitlines()
print(to_snafu(sum(from_snafu(row) for row in _input)))
