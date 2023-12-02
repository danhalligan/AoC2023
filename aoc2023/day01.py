import re


def calibration_values(line):
    ints = re.findall(r"\d", line)
    return ints[0] + ints[-1]


def convert_num(x):
    d = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    return d[x] if x in d else x


def calibration_values_fixed(line):
    ints = re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", line)
    return convert_num(ints[0]) + convert_num(ints[-1])


def part_a(data):
    lines = data.splitlines()
    return sum(int(calibration_values(line)) for line in lines)


def part_b(data):
    lines = data.splitlines()
    return sum(int(calibration_values_fixed(line)) for line in lines)
