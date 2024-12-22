import sys
from collections import Counter

secrets = [int(row) for row in sys.stdin]


def evolve(secret):
    secret ^= secret * 64
    secret %= 0x1000000
    secret ^= secret // 32
    secret %= 0x1000000
    secret ^= secret * 2048
    secret %= 0x1000000
    return secret


# I used to represent the sequence of last 4 diffs using a deque(maxlen=4),
# but as we know each of the 4 numbers is in the range [-9, 9], we can encode
# them in 5 bits each: adding 9 gives the [0, 18], and 2**4 <= 18 < 2**5.
# So our number looks like this: 0b00000_00000_00000_00000
#                                  ^^^^^             ^^^^^
#                               newest diff       oldest diff
# The initial value is 11111_11111_11111_11111, and note that as 11111 does
# not represent a value in [0, 18], we can test this to know if we do not
# have the 4 diffs yet (by masking with 0b11111).
# Using this representation yields impressive results on PyPy, not so much on CPython.

evolved_secrets_sum = 0  # for part 1
price_per_seq: dict[int, int] = Counter()  # for part 2
seq_seen_for_secret = set()

for secret in secrets:
    seq_seen_for_secret.clear()

    seq = (1 << 20) - 1
    last_price = secret % 10

    for _ in range(2000):
        secret = evolve(secret)
        price = secret % 10
        # Updating seq by right shifting by 5 bits to remove the oldest diff,
        # and adding the newest diff in the leftmost 5 bits.
        seq >>= 5
        seq |= (price - last_price + 9) << 15

        if seq not in seq_seen_for_secret and seq & 0b11111 != 0b11111:
            seq_seen_for_secret.add(seq)
            price_per_seq[seq] += price

        last_price = price
    evolved_secrets_sum += secret

print(evolved_secrets_sum)
print(max(price_per_seq.values()))
