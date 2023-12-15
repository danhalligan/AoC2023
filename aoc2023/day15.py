import re


def hash(string):
    val = 0
    for x in string:
        val = (val + ord(x)) * 17 % 256
    return val


def part_a(data):
    return sum(hash(x) for x in data.split(","))


def part_b(data):
    data = data.split(",")
    boxes = [[]] * 256

    for instr in data:
        box, val, num = re.match("(.+)([=-])(\d+)*", instr).groups()
        boxh = hash(box)
        if val == "-":
            boxes[boxh] = [(l, v) for l, v in boxes[boxh] if l != box]
        if val == "=":
            num = int(num)
            if box in [l for l, _ in boxes[boxh]]:
                boxes[boxh] = [
                    (box, num) if l == box else (l, v) for l, v in boxes[boxh]
                ]
            else:
                boxes[boxh] = boxes[boxh] + [(box, num)]

    tot = 0
    for i, x in enumerate(boxes):
        tot += sum((i + 1) * (j + 1) * v for j, (_, v) in enumerate(x))

    return tot
