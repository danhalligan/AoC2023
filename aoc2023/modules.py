class FlipFlop:
    def __init__(self, name, dests):
        self.state = "low"
        self.name = name
        self.dests = dests

    def exe(self, packet):
        fr, to, pulse = packet
        if pulse == "low":
            self.state = "low" if self.state == "high" else "high"
            for dest in self.dests:
                # print(self.name, self.state, "->", dest)
                yield (self.name, dest, self.state)


class Conjunction:
    def __init__(self, name, dests, inputs):
        self.dests = dests
        self.name = name
        self.mem = {x: "low" for x in inputs}
        self.track = False

    def exe(self, packet):
        fr, to, pulse = packet
        self.mem[fr] = pulse
        out = "low" if all(x == "high" for x in self.mem.values()) else "high"
        if self.track and out == "high":
            raise Exception("High found")
        for dest in self.dests:
            # print(self.name, out, "->", dest)
            yield (self.name, dest, out)


class Broadcaster:
    def __init__(self, dests):
        self.name = "broadcaster"
        self.dests = dests

    def exe(self, packet):
        fr, to, pulse = packet
        for dest in self.dests:
            # print("broadcaster", pulse, "->", dest)
            yield (self.name, dest, pulse)


class Untyped:
    def __init__(self):
        self.name = "output"

    def exe(self, packet):
        return []
