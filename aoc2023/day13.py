def reflections(array):
    nrow = len(array)
    for i in range(nrow - 1):
        j = 0
        all_true = True
        while i - j >= 0 and i + 1 + j < nrow:
            l1 = array[i - j]
            l2 = array[i + 1 + j]
            if l1 != l2:
                all_true = False
                break
            j += 1
        if all_true:
            yield i + 1


# Transpose a list of lists
def t(array):
    return list(map(list, zip(*array)))


def part_a(data):
    tot = 0
    for pattern in data.split("\n\n"):
        array = [[x for x in list(line)] for line in pattern.splitlines()]
        tot += sum(reflections(t(array))) + 100 * sum(reflections(array))
    return tot


def reflections_smudged(array):
    nrow = len(array)
    for i in range(nrow - 1):
        j = 0
        mismatches = 0
        while i - j >= 0 and i + 1 + j < nrow:
            l1 = array[i - j]
            l2 = array[i + 1 + j]
            mismatches += sum(x != y for x, y in zip(l1, l2))
            j += 1
        if mismatches == 1:
            yield i + 1


def part_b(data):
    tot = 0
    for pattern in data.split("\n\n"):
        array = [[x for x in list(line)] for line in pattern.splitlines()]
        tot += sum(reflections_smudged(t(array)))
        tot += 100 * sum(reflections_smudged(array))
    return tot
