import importlib
import pytest
from itertools import product
from aocd.models import Puzzle
from aocd.examples import Example


# Test each day by importing the module and running part1 and part2
@pytest.mark.parametrize("day,part", product(range(1, 25), ["a", "b"]))
def test_all(day, part):
    try:
        module = importlib.import_module(f"aoc2023.day{day:02d}")
        fn = getattr(module, f"part_{part}")
    except:
        pytest.skip(f"skipping day {day}, part {part}")
    puzzle = Puzzle(year=2023, day=day)
    examples = puzzle.examples

    # Patch examples for day 1
    # TODO: there's a better way of doing this!
    if day == 1:
        eg = puzzle.examples[0]
        examples = [Example(eg.input_data, eg.answer_a)]

    for example in examples:
        answer = example.answers[{"a": 0, "b": 1}[part]]
        if answer is not None:
            assert str(fn(example.input_data)) == answer
