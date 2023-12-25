from aocd.models import Puzzle
from aocd.examples import Example
from datetime import datetime
import pickle


def get_examples(day):
    puzzle = Puzzle(year=2023, day=day)
    if datetime.now(puzzle.unlock_time().tzinfo) < puzzle.unlock_time():
        return day, None

    examples = puzzle.examples

    # Patch examples for day 1
    # TODO: there must be a better way of doing this!
    eg = puzzle.examples[0]
    if day == 1:
        examples = [Example(eg.input_data, eg.answer_a)]
    if day == 6:
        examples = [Example(eg.input_data, "288", "71503")]
    if day == 8:
        examples = [Example(eg.input_data, "2", None)]
    if day == 10:
        examples = [Example("..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...", "8", None)]
    if day == 12:
        examples = [
            Example(
                "???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1",
                "21",
                "525152",
            )
        ]
    if day == 20:
        examples = [Example(eg.input_data, "32000000")]
    if day == 21:
        examples = [Example(eg.input_data, "16")]
    if day == 23:
        examples = [Example(eg.input_data, "94", "154")]
    if day == 24:
        examples = [Example(eg.input_data, "2", "47")]
    return day, examples


# Test each day by importing the module and running part_a and part_b functions
# against all the examples for that day's puzzle.
# We skip tests if there is no defined function.
all_examples = dict(get_examples(day) for day in range(1, 25))

with open("tests/examples.pkl", "wb") as file:
    pickle.dump(all_examples, file)
