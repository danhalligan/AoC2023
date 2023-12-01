import re
from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=1)


def part_a(puzzle):
    lines = puzzle.input_data.splitlines()
    tot = 0
    for x in lines:
        ints = re.findall(r"\d", x)
        tot += int(ints[0] + ints[-1])
    return tot


def convert_num(x):
    return {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }[x]


def part_b(puzzle):
    lines = puzzle.input_data.splitlines()
    tot = 0
    for x in lines:
        ints = re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", x)
        ints = [convert_num(n) for n in ints]
        tot += int(ints[0] + ints[-1])
    return tot
