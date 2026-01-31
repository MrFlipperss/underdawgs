import random
from utils.types import PaymentEvent

class Simulator:
    ISSUERS = ["AcmeBank", "GlobalPay", "ProtoCard"]

    def generate(self):
        issuer = random.choice(self.ISSUERS)
        amount = round(random.uniform(10, 500), 2)
        latency = random.randint(80, 600)

        if random.random() < 0.75:
            return PaymentEvent.new(issuer, amount, "success", None, latency)
        else:
            error = random.choice(["NET_TIMEOUT", "DECLINED", "RATE_LIMIT"])
            return PaymentEvent.new(issuer, amount, "failed", error, latency)
