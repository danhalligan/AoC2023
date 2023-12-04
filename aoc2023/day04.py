import re


def parse_data(data):
    lines = data.splitlines()
    for line in lines:
        card, nums = line.split(": ")
        winning, mine = nums.split(" | ")
        winning = [int(x) for x in re.findall("\d+", winning)]
        mine = [int(x) for x in re.findall("\d+", mine)]
        yield winning, mine


def n_winning(card):
    return sum(num in card[0] for num in card[1])


def part_a(data):
    cards = list(parse_data(data))
    tot = 0
    for card in cards:
        matches = n_winning(card)
        tot += 2 ** (matches - 1) if matches else 0
    return tot


def part_b(data):
    cards = list(parse_data(data))
    card_counts = [1 for i in range(len(cards))]
    for i in range(len(cards)):
        nw = n_winning(cards[i])
        for j in range(i + 1, i + 1 + nw):
            card_counts[j] += card_counts[i]
    return sum(card_counts)
