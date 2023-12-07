import re


def calibration_values(line):
    ints = re.findall(r"\d", line)
    return ints[0] + ints[-1]


def convert_num(x):
    ints = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    return str(ints.index(x) + 1) if x in ints else x


def calibration_values_fixed(line):
    ints = re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", line)
    return convert_num(ints[0]) + convert_num(ints[-1])


def part_a(data):
    lines = data.splitlines()
    return sum(int(calibration_values(line)) for line in lines)


def part_b(data):
    lines = data.splitlines()
    return sum(int(calibration_values_fixed(line)) for line in lines)
