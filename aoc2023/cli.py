import typer
import importlib
from aocd.models import Puzzle

app = typer.Typer()


@app.command()
def solve(day: str):
    """Solve a challenge for a given day"""
    day = int(day)
    module = importlib.import_module(f"aoc2023.day{day:02d}")
    puzzle = Puzzle(year=2023, day=day)
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
