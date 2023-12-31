import importlib
import pytest
from itertools import product
import pickle

all_examples = pickle.load(open("tests/examples.pkl", "rb"))


# Test each day by importing the module and running part_a and part_b functions
# against all the examples for that day's puzzle.
# We skip tests if there is no defined function.
@pytest.mark.parametrize("day,part", product(range(1, 25), ["a", "b"]))
def test_all(day, part):
    try:
        module = importlib.import_module(f"aoc2023.day{day:02d}")
        fn = getattr(module, f"part_{part}")
    except AttributeError:
        pytest.skip(f"Skipping day {day}, part {part}")
    examples = all_examples[day]

    for example in examples:
        answer = example.answers[{"a": 0, "b": 1}[part]]
        if answer is not None:
            assert str(fn(example.input_data)) == answer
