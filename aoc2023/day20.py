from .modules import Broadcaster, FlipFlop, Conjunction, Untyped
from math import lcm
import re


def build_network(data):
    network = {}
    for line in data.splitlines():
        name, connections = line.split(" -> ")
        connections = connections.split(", ")
        name = re.findall("[%&]*(.+)", name)[0]
        network[name] = connections
    return network


def invert_network(network):
    rnetwork = {}
    for k, v in network.items():
        for m in v:
            rnetwork[m] = rnetwork.get(m, []) + [k]
    return rnetwork


def init_modules(data):
    network = build_network(data)
    rnetwork = invert_network(network)
    modules = {}
    for line in data.splitlines():
        name, dests = line.split(" -> ")
        dests = dests.split(", ")
        if name == "broadcaster":
            modules["broadcaster"] = Broadcaster(dests)
        if name.startswith("%"):
            modules[name[1:]] = FlipFlop(name[1:], dests)
        if name.startswith("&"):
            modules[name[1:]] = Conjunction(name[1:], dests, rnetwork[name[1:]])
    outputs = set(x for l in network.values() for x in l)
    inputs = set(network.keys())
    for x in outputs - inputs:
        modules[x] = Untyped()
    return modules


def run(modules, packets):
    count = {"low": 0, "high": 0}
    while packets:
        packet = packets.pop(0)
        count[packet[2]] += 1
        packets += list(modules[packet[1]].exe(packet))
    return count["low"], count["high"]


def part_a(data):
    modules = init_modules(data)
    low, high = 0, 0
    for _ in range(1000):
        counts = run(modules, [("button", "broadcaster", "low")])
        low += counts[0]
        high += counts[1]
    return low * high


def track_module(data, modules, name):
    modules = init_modules(data)
    modules[name].track = True
    count = 0
    while True:
        count += 1
        try:
            run(modules, [("button", "broadcaster", "low")])
        except:
            return count


# rx is the final untyped module
# there is one conjunction (zh) leading to rx
# there are 4 conjunctions leading to zh
# Let's track when each of these issue a high value
# When these all coincide we will get a high value at rx...
def part_b(data):
    rnetwork = invert_network(build_network(data))
    modules = init_modules(data)
    parent = rnetwork["rx"][0]
    times = [track_module(data, modules, name) for name in rnetwork[parent]]
    return lcm(*times)
