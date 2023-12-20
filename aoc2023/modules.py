from dataclasses import dataclass


@dataclass
class Packet:
    fr: str
    to: str
    val: str


def ModuleFactory(name, dests):
    """Factory Method"""
    if name == "broadcaster":
        return Module("broadcaster", dests)
    elif name.startswith("%"):
        return FlipFlop(name[1:], dests)
    elif name.startswith("&"):
        return Conjunction(name[1:], dests)
    else:
        return Module(name, [])


class Module:
    def __init__(self, name, dests):
        self.dests = dests
        self.name = name

    def setup(self, rnetwork):
        self.track = False
        self.inputs = rnetwork[self.name]

    def calculate(self, packet):
        return packet.val

    def exe(self, packet):
        val = self.calculate(packet)
        if self.track and val == "high":
            raise Exception("High found")
        if val:
            for dest in self.dests:
                yield Packet(self.name, dest, val)


class FlipFlop(Module):
    def setup(self, rnetwork):
        self.track = False
        self.inputs = rnetwork[self.name]
        self.state = "low"

    def calculate(self, packet):
        if packet.val == "low":
            self.state = "low" if self.state == "high" else "high"
            return self.state


class Conjunction(Module):
    def setup(self, rnetwork):
        self.track = False
        self.inputs = rnetwork[self.name]
        self.mem = {x: "low" for x in self.inputs}

    def calculate(self, packet):
        self.mem[packet.fr] = packet.val
        return "low" if all(x == "high" for x in self.mem.values()) else "high"
