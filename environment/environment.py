from simulator.simulator import Simulator

class PaymentEnvironment:
    def __init__(self):
        self.sim = Simulator()

    def step(self):
        return self.sim.generate()
