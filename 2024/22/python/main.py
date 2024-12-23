import sys
from collections import Counter

secrets = [int(row) for row in sys.stdin]


def evolve(secret):
    # The pruning process uses modulo 0x1000000 to keep the secret in the
    # range [0, 0xFFFFFF]. Here we used a mask instead, and we do the modulo
    # before the mix, as it gives the same results anyway.
    secret ^= (secret * 64) & 0xFFFFFF
    secret ^= (secret // 32) & 0xFFFFFF
    secret ^= (secret * 2048) & 0xFFFFFF
    return secret


# I used to represent the sequence of last 4 diffs using a deque(maxlen=4),
# but as we know each of the 4 numbers is in the range [-9, 9], adding 9 gives
# the range [0, 18], so we can encode then in "base 19". This gives a single
# integer to represent the 4 numbers, and adding a new diff is just dividing
# by the base (19), this works like a right bitshift in that base, and adding
# the number diff in the highest bits.
# Using this representation yields impressive results on PyPy, meh on CPython.

last_secrets_sum = 0  # for part 1
price_per_seq: dict[int, int] = Counter()  # for part 2

# We only want to keep the first sequence seen for each secret, so we use
# this set to record each sequence.
seq_seen_for_secret: set[int] = set()

for secret in secrets:
    seq_seen_for_secret.clear()

    seq = 0
    prev_price = secret % 10

    # To avoid the first 3 diffs to be counted, we roll out the loop 3 times.
    # This avoids to have repeated checks for this in the main loop.
    for _ in range(3):
        secret = evolve(secret)
        price = secret % 10
        seq = (seq // 19) + (19**3) * (price - prev_price + 9)

    for _ in range(3, 2000):
        secret = evolve(secret)
        price = secret % 10
        seq = (seq // 19) + (19**3) * (price - prev_price + 9)

        if seq not in seq_seen_for_secret:
            seq_seen_for_secret.add(seq)
            price_per_seq[seq] += price

        prev_price = price
    last_secrets_sum += secret

print(last_secrets_sum)
print(max(price_per_seq.values()))
