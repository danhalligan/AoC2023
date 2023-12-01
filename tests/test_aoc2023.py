import importlib
import pytest
from itertools import product
from aocd.models import Puzzle


# Test each day by importing the module and running part1 and part2
parts = product(range(1, 25), ["a", "b"])


@pytest.mark.parametrize("day,part", parts)
def test_all(day, part):
    try:
        module = importlib.import_module(f"aoc2023.day{day:02d}")
        fn = getattr(module, f"part_{part}")
    except:
        pytest.skip(f"skipping day {day}, part {part}")
    puzzle = Puzzle(year=2023, day=day)
    for example in puzzle.examples:
        answer = example.answers[{"a": 0, "b": 1}[part]]
        assert str(fn(example.input_data)) == answer
