import typer
from typing import List
import importlib
from datetime import datetime
from aocd.models import Puzzle

app = typer.Typer()


@app.command()
def solve(days: List[str] = list(range(1, 25))):
    """Solve a challenge for given days"""
    for day in days:
        day = int(day)
        module = importlib.import_module(f"aoc2023.day{day:02d}")
        puzzle = Puzzle(year=2023, day=day)
        if datetime.now(puzzle.unlock_time().tzinfo) < puzzle.unlock_time():
            continue

        print(f"--- Day {day}: {puzzle.title} ---")

        try:
            print("Part A:", getattr(module, "part_a")(puzzle.input_data))
        except AttributeError:
            print("No part A")
        try:
            print("Part B:", getattr(module, "part_b")(puzzle.input_data))
        except AttributeError:
            print("No part B")
        print()


@app.command()
def submit(day: str):
    day = int(day)
    module = importlib.import_module(f"aoc2023.day{day:02d}")
    puzzle = Puzzle(year=2023, day=day)
    try:
        puzzle.answer_a = getattr(module, "part_a")(puzzle.input_data)
    except AttributeError:
        print("No part A")
    try:
        puzzle.answer_b = getattr(module, "part_b")(puzzle.input_data)
    except AttributeError:
        print("No part B")


def main():
    app()
