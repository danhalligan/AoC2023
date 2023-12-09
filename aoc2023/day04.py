from .helpers import ints


def parse_data(data):
    lines = data.splitlines()
    for line in lines:
        _, nums = line.split(": ")
        winning, mine = nums.split(" | ")
        yield sum(num in ints(winning) for num in ints(mine))


def part_a(data):
    scores = list(parse_data(data))
    return sum(2 ** (score - 1) if score else 0 for score in scores)


def part_b(data):
    scores = list(parse_data(data))
    card_counts = [1 for _ in range(len(scores))]
    for i in range(len(scores)):
        for j in range(i + 1, i + 1 + scores[i]):
            card_counts[j] += card_counts[i]
    return sum(card_counts)
