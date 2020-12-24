import sys
from itertools import islice
from collections import deque

decks = {}
for row in sys.stdin:
    row = row.strip()
    if row.startswith("Player"):
        player = row.strip(":").split()[1]
        decks[player] = deque()
    elif row:
        decks[player].append(int(row))


def play(deck_1, deck_2, recursive):
    # Returns True if player 1 wins, False if player 2 wins.
    # Decks will be modified in place.
    seen = set()

    while deck_1 and deck_2:
        if recursive:
            state = tuple(deck_1), tuple(deck_2)
            if state in seen:
                return True  # player 1 wins
            seen.add(state)

        card_1 = deck_1.popleft()
        card_2 = deck_2.popleft()

        if len(deck_1) >= card_1 and len(deck_2) >= card_2 and recursive:
            player_1_wins = play(
                deque(islice(deck_1, None, card_1)),
                deque(islice(deck_2, None, card_2)),
                recursive,
            )
        else:
            player_1_wins = card_1 > card_2

        if player_1_wins:
            deck_1.extend([card_1, card_2])
        else:
            deck_2.extend([card_2, card_1])

    return True if deck_1 else False


# PART 1: recursive = False
# PART 2: recursive = True
#
for recursive in False, True:
    # We copy the decks for next parts, because "play" modifies them
    deck_1 = decks["1"].copy()
    deck_2 = decks["2"].copy()
    if play(deck_1, deck_2, recursive):
        deck_w = deck_1
    else:
        deck_w = deck_2
    print(sum(card * cn for cn, card in enumerate(reversed(deck_w), start=1)))
