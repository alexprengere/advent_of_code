import sys

data = []
for row in sys.stdin:
    data.append(row.strip())


# PART 1
#
memory = {}

mask = None
for row in data:
    left, _, right = row.split()
    if left == "mask":
        mask = right
    else:
        address = int(left[4:-1])
        value = int(right)
        value_bits = ["0"] * len(mask)
        for bn, b in enumerate(bin(value)[2:][::-1], start=1):  # 0b...
            value_bits[-bn] = b
        masked_bits = "".join(b if m == "X" else m for m, b in zip(mask, value_bits))
        memory[address] = int(masked_bits, 2)

print(sum(memory.values()))


# PART 2
#
memory = {}

mask = None
for row in data:
    left, _, right = row.split()
    if left == "mask":
        mask = right
    else:
        value = int(right)
        address = int(left[4:-1])
        address_bits = ["0"] * len(mask)
        for bn, b in enumerate(bin(address)[2:][::-1], start=1):  # 0b...
            address_bits[-bn] = b
        floating = [[]]
        for m, b in zip(mask, address_bits):
            for bits in floating[:]:
                if m == "0":
                    bits.append(b)
                elif m == "1":
                    bits.append("1")
                elif m == "X":
                    bits.append("0")
                    floating.append(bits[:-1] + ["1"])

        for bits in floating:
            address = int("".join(bits), 2)
            memory[address] = value

print(sum(memory.values()))
