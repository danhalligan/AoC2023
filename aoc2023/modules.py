from dataclasses import dataclass


@dataclass
class Packet:
    fr: str
    to: str
    val: str


def ModuleFactory(name):
    if name.startswith("%"):
        return FlipFlop(name[1:])
    elif name.startswith("&"):
        return Conjunction(name[1:])
    else:
        return Module(name)


class Module:
    def __init__(self, name, inputs=None):
        self.name = name
        self.inputs = inputs

    def setup(self):
        self.track = False

    def calculate(self, packet):
        return packet.val

    def exe(self, packet):
        val = self.calculate(packet)
        if self.track and val == "high":
            raise Exception("High found")
        return val


class FlipFlop(Module):
    def setup(self):
        self.track = False
        self.state = "low"

    def calculate(self, packet):
        if packet.val == "low":
            self.state = "low" if self.state == "high" else "high"
            return self.state


class Conjunction(Module):
    def setup(self):
        self.track = False
        self.mem = {x: "low" for x in self.inputs}

    def calculate(self, packet):
        self.mem[packet.fr] = packet.val
        return "low" if all(x == "high" for x in self.mem.values()) else "high"
