from dataclasses import dataclass


@dataclass
class Packet:
    fr: str
    to: str
    val: str


def ModuleFactory(name, dests):
    """Factory Method"""
    if name == "broadcaster":
        return Broadcaster("broadcaster", dests)
    elif name.startswith("%"):
        return FlipFlop(name[1:], dests)
    elif name.startswith("&"):
        return Conjunction(name[1:], dests)
    else:
        return Module(name, dests)


class Module:
    def __init__(self, name, dests):
        self.dests = dests
        self.name = name

    def setup(self, rnetwork):
        self.track = False
        self.inputs = rnetwork[self.name]

    def exe(self, _):
        return []


class FlipFlop(Module):
    def setup(self, rnetwork):
        self.track = False
        self.inputs = rnetwork[self.name]
        self.state = "low"

    def exe(self, packet):
        if packet.val == "low":
            self.state = "low" if self.state == "high" else "high"
            for dest in self.dests:
                # print(self.name, self.state, "->", dest)
                yield Packet(self.name, dest, self.state)


class Conjunction(Module):
    def setup(self, rnetwork):
        self.track = False
        self.inputs = rnetwork[self.name]
        self.mem = {x: "low" for x in self.inputs}

    def exe(self, packet):
        self.mem[packet.fr] = packet.val
        out = "low" if all(x == "high" for x in self.mem.values()) else "high"
        if self.track and out == "high":
            raise Exception("High found")
        for dest in self.dests:
            # print(self.name, out, "->", dest)
            yield Packet(self.name, dest, out)


class Broadcaster(Module):
    def exe(self, packet):
        for dest in self.dests:
            # print("broadcaster", pulse, "->", dest)
            yield Packet(self.name, dest, packet.val)
