import re
from operator import gt, lt
from copy import copy
from math import prod


def parse_part(txt):
    def parse_key(key):
        k, v = key.split("=")
        return k, int(v)

    keys = txt[1:-1].split(",")
    return dict(parse_key(key) for key in keys)


def parse_rule(txt):
    cond, to = txt.split(":")
    key, op, val = re.match(r"(.+)([><])(.+)", cond).groups()
    op = {">": gt, "<": lt}[op]
    return lambda part: op(part[key], int(val)), to


def parse_workflow(line):
    name, rules = re.match(r"(\w+){(.+)}", line).groups()
    rules = rules.split(",")
    last = rules.pop()

    def workflow(part):
        for rule in rules:
            test, val = parse_rule(rule)
            if test(part):
                return val
        return last

    return name, workflow


def run_workflows(part, workflows):
    key = "in"
    while True:
        key = workflows[key](part)
        if key in ["A", "R"]:
            return key


def part_a(data):
    workflows, parts = data.split("\n\n")
    workflows = dict(parse_workflow(line) for line in workflows.splitlines())
    parts = [parse_part(part) for part in parts.splitlines()]
    parts = [part for part in parts if run_workflows(part, workflows) == "A"]
    return sum(sum(part.values()) for part in parts)


# Returns a function that takes a part and returns two sub parts
def parse_rule2(txt):
    cond, to = txt.split(":")
    key, op, val = re.match(r"(.+)([><])(.+)", cond).groups()
    val = int(val)

    def run(part):
        parts = [copy(part), copy(part)]
        if op == ">":
            parts[0][key] = range(val + 1, part[key].stop)
            parts[1][key] = range(part[key].start, val + 1)
        else:
            parts[0][key] = range(part[key].start, val)
            parts[1][key] = range(val, part[key].stop)
        return parts

    return run


def parse_workflow2(line):
    name, rules = re.match(r"(\w+){(.+)}", line).groups()
    rules = rules.split(",")
    last = rules.pop()
    subnames = [name + str(i) for i in range(len(rules) - 1)]
    trues = [x.split(":")[1] for x in rules]
    falses = subnames + [last]
    rules = [parse_rule2(rule) for rule in rules]
    return dict(zip([name] + subnames, zip(rules, trues, falses)))


def part_b(data):
    workflows, _ = data.split("\n\n")
    wfs = dict()
    for line in workflows.splitlines():
        wfs = wfs | parse_workflow2(line)

    part = {k: range(1, 4001) for k in "xmas"}
    todo = [[part, "in"]]
    done = []
    while todo:
        part = todo.pop(0)
        fn, t, f = wfs[part[1]]
        for p, v in zip(fn(part[0]), [t, f]):
            if v not in ["A", "R"]:
                todo += [[p, v]]
            elif v == "A":
                done += [p]
    return sum(prod(len(r) for r in part.values()) for part in done)
