import sys
from collections import deque

secrets = [int(row) for row in sys.stdin]


def evolve(secret):
    secret ^= secret * 64
    secret %= 0x1000000
    secret ^= secret // 32
    secret %= 0x1000000
    secret ^= secret * 2048
    secret %= 0x1000000
    return secret


def evolve_multi(secret, times=1):
    for _ in range(times):
        secret = evolve(secret)
    return secret


# PART 1
#
N = 2000
print(sum(evolve_multi(secret, times=N) for secret in secrets))


# PART 2
#
def show(secret, times):
    price = secret % 10
    print(f"{secret:>15d}: {price}")

    for _ in range(times - 1):
        secret = evolve(secret)
        last_price, price = price, secret % 10
        diff = price - last_price if last_price is not None else 0
        print(f"{secret:>15d}: {price} ({diff:+>2d})")


def get_seqs_until(secret, times):
    last_diffs = deque(maxlen=4)
    price = secret % 10
    for _ in range(times):
        secret = evolve(secret)
        last_price, price = price, secret % 10
        if last_price is not None:
            last_diffs.append(price - last_price)
        if len(last_diffs) == 4:
            yield (price, tuple(last_diffs))


show(123, 10)


CACHE = {}
for secret in secrets:
    seq_to_price = {}
    for price, seq in get_seqs_until(secret, times=N):
        if seq not in seq_to_price:
            seq_to_price[seq] = price
    CACHE[secret] = seq_to_price


all_seq = set()
for secret in secrets:
    all_seq.update(CACHE[secret])


print(len(all_seq))


max_price = 0
max_seq = None
for i, seq in enumerate(all_seq):
    if i % 1000 == 0:
        print(i, len(all_seq))
    price = sum(CACHE[secret].get(seq, 0) for secret in secrets)
    if price > max_price:
        max_price = price
        max_seq = seq
print(max_price, max_seq)
