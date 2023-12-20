from .modules import Packet, ModuleFactory
from math import lcm
from collections import defaultdict


def invert_network(network):
    rnetwork = defaultdict(list)
    for k, v in network.items():
        for m in v:
            rnetwork[m] += [k]
    return rnetwork


def parse_modules(data):
    network = {}
    modules = {}
    for line in data.splitlines():
        name, dests = line.split(" -> ")
        dests = dests.split(", ")
        mod = ModuleFactory(name, dests)
        modules[mod.name] = mod
        network[mod.name] = dests

    # add modules that only appear as outputs
    outputs = set(x for v in network.values() for x in v)
    inputs = set(network.keys())
    for x in outputs - inputs:
        modules[x] = ModuleFactory(x, dests)
    return modules, network


def setup_modules(modules, network):
    rnetwork = invert_network(network)
    for k in modules.keys():
        modules[k].setup(rnetwork)


def run(modules, packets):
    count = {"low": 0, "high": 0}
    while packets:
        packet = packets.pop(0)
        count[packet.val] += 1
        packets += list(modules[packet.to].exe(packet))
    return count["low"], count["high"]


def part_a(data):
    modules, network = parse_modules(data)
    setup_modules(modules, network)
    low, high = 0, 0
    for _ in range(1000):
        counts = run(modules, [Packet("button", "broadcaster", "low")])
        low += counts[0]
        high += counts[1]
    return low * high


def track_module(modules, network, name):
    setup_modules(modules, network)
    modules[name].track = True
    count = 0
    while True:
        count += 1
        try:
            run(modules, [Packet("button", "broadcaster", "low")])
        except Exception:
            return count


# rx is the final untyped module
# there is one conjunction (zh) leading to rx
# there are 4 conjunctions leading to zh
# Let's track when each of these issue a high value
# When these all coincide we will get a high value at rx...
def part_b(data):
    modules, network = parse_modules(data)
    setup_modules(modules, network)
    parent = modules["rx"].inputs[0]
    times = [track_module(modules, network, name) for name in modules[parent].inputs]
    return lcm(*times)
