def reflections(array, mm=0):
    nrow = len(array)
    for i in range(nrow - 1):
        j = 0
        mismatches = 0
        while i - j >= 0 and i + 1 + j < nrow:
            l1 = array[i - j]
            l2 = array[i + 1 + j]
            mismatches += sum(x != y for x, y in zip(l1, l2))
            j += 1
        if mismatches == mm:
            yield i + 1


# Transpose a list of lists
def t(array):
    return list(map(list, zip(*array)))


def summary(pattern, mm):
    array = [[x for x in list(line)] for line in pattern.splitlines()]
    return sum(reflections(t(array)), mm) + 100 * sum(reflections(array, mm))


def part_a(data):
    return sum(summary(pattern, 0) for pattern in data.split("\n\n"))


def part_b(data):
    return sum(summary(pattern, 1) for pattern in data.split("\n\n"))
