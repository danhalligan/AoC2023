# AoC2023

![CI workflow](https://github.com/danhalligan/AoC2023/actions/workflows/ci.yaml/badge.svg)
![License](https://img.shields.io/github/license/danhalligan/AoC2023)
![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)

`AoC2023` is a python package implementing solutions python solutions for the
[Advent of Code 2023] problems.

## Example

First you need to [setup your session ID] as this package uses 
[`advent-of-code-data`] to retrieve the data input.

To solve all days (where available) run:

``` bash
poetry run aoc2023
```

Or to solve specific day(s) (e.g. days 1 and 5):

``` bash
poetry run aoc2023 1 5
```


[Advent of Code 2023]: https://adventofcode.com/2023
[setup your session ID]: https://github.com/wimglenn/advent-of-code-data/tree/main#quickstart
[`advent-of-code-data`]: https://github.com/wimglenn/advent-of-code-data/
