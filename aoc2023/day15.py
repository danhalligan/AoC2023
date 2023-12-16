import re
from functools import reduce


def hash(string):
    return reduce(lambda v, x: (v + ord(x)) * 17 % 256, string, 0)


def part_a(data):
    return sum(hash(x) for x in data.split(","))


def part_b(data):
    data = data.split(",")
    boxes = [dict() for _ in range(256)]

    for instr in data:
        box, val, num = re.match("(.+)([=-])(\d+)*", instr).groups()
        if val == "-":
            boxes[hash(box)].pop(box, 0)
        if val == "=":
            boxes[hash(box)][box] = int(num)

    return sum(
        i * j * v for i, x in enumerate(boxes, 1) for j, v in enumerate(x.values(), 1)
    )
