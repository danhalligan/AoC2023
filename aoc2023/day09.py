from itertools import pairwise
from .helpers import ints


def interpolate(seq):
    if all(x == 0 for x in seq):
        return 0
    else:
        diffs = [y - x for x, y in pairwise(seq)]
        return seq[-1] + interpolate(diffs)


def parse_data(data):
    return [ints(line) for line in data.splitlines()]


def part_a(data):
    return sum([interpolate(seq) for seq in parse_data(data)])


def part_b(data):
    return sum([interpolate(seq[::-1]) for seq in parse_data(data)])
