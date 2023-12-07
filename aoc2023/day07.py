from collections import Counter


def has_n(hand, n):
    return any(x == n for x in Counter(hand).values())


def parse_hands(data):
    for x in data.splitlines():
        a, b = x.split(" ")
        yield list(a), int(b)


def primary_score(hand):
    if has_n(hand, 5):
        return 6
    elif has_n(hand, 4):
        return 5
    elif has_n(hand, 3) and has_n(hand, 2):
        return 4
    elif has_n(hand, 3):
        return 3
    elif sum(x == 2 for x in Counter(hand).values()) == 2:
        return 2
    elif has_n(hand, 2):
        return 1
    else:
        return 0


def card_order(card):
    return ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"].index(card)


def hand_order(hand):
    return [-card_order(x) for x in hand]


def part_a(data):
    hands = list(parse_hands(data))
    hands.sort(key=lambda x: (primary_score(x[0]), *hand_order(x[0])))
    return sum((i + 1) * x[1] for i, x in enumerate(hands))


# when considering jokers, we only ever need to consider setting them to the
# *same* card type.
def yield_hands(hand):
    if "J" in hand:
        for n in ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]:
            yield [n if x == "J" else x for x in hand]
    else:
        yield hand


def joker_score(hand):
    return max(primary_score(new_hand) for new_hand in yield_hands(hand))


def new_card_order(card):
    return ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"].index(card)


def new_hand_order(hand):
    return [-new_card_order(x) for x in hand]


def part_b(data):
    hands = list(parse_hands(data))
    hands.sort(key=lambda x: (joker_score(x[0]), *new_hand_order(x[0])))
    return sum((i + 1) * x[1] for i, x in enumerate(hands))
