import re
from math import prod
from collections import defaultdict


def parse_subset(subset):
    for draw in subset.split(", "):
        draw = draw.split(" ")
        yield draw[1], int(draw[0])


def parse_line(line):
    game, results = line.split(": ")
    game = int(re.findall(r"\d+", game)[0])
    subsets = results.split("; ")
    subsets = [defaultdict(int, parse_subset(subset)) for subset in subsets]
    return {"id": game, "subsets": subsets}


def valid_draw(subset, required):
    for col in ["red", "green", "blue"]:
        if subset[col] > required[col]:
            return False
    return True


def valid_game(game, required):
    return all([valid_draw(draw, required) for draw in game])


def game_power(game):
    minimum = {"red": 0, "green": 0, "blue": 0}
    for subset in game["subsets"]:
        for col in ["red", "green", "blue"]:
            minimum[col] = max(minimum[col], subset[col])
    return prod(minimum.values())


def part_a(data):
    data = [parse_line(line) for line in data.splitlines()]
    req = {"red": 12, "green": 13, "blue": 14}
    return sum(game["id"] for game in data if valid_game(game["subsets"], req))


def part_b(data):
    data = [parse_line(line) for line in data.splitlines()]
    return sum(game_power(game) for game in data)
