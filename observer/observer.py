from collections import defaultdict, deque
import statistics

class Observer:
    def __init__(self, window_size=5E0):
        self.window = deque(maxlen=window_size)

    def consume(self, event):
        self.window.append(event)

    def snapshot(self):
        total = len(self.window)
        if total == 0:
            return {}

        failures = [e for e in self.window if e.status != "success"]
        latencies = [e.latency_ms for e in self.window]

        by_issuer = defaultdict(list)
        for e in self.window:
            by_issuer[e.issuer].append(e)

        issuer_stats = {}
        for issuer, events in by_issuer.items():
            fail_rate = sum(e.status != "success" for e in events) / len(events)
            issuer_stats[issuer] = {
                "fail_rate": round(fail_rate, 2),
                "count": len(events)
            }

        return {
            "total": total,
            "fail_rate": round(len(failures) / total, 2),
            "p95_latency": statistics.quantiles(latencies, n=20)[-1],
            "issuers": issuer_stats
        }
