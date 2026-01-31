from typing import Dict, List

class Hypothesis:
    def __init__(self, name: str):
        self.name = name
        self.score = 0.0
        self.evidence: List[str] = []

    def add(self, weight: float, reason: str):
        self.score += weight
        self.evidence.append(reason)


class Reasoner:
    """
    Turns observation snapshots into beliefs with confidence.
    """

    def analyze(self, snapshot: Dict) -> Dict:
        hypotheses = {
            "issuer_degradation": Hypothesis("issuer_degradation"),
            "network_instability": Hypothesis("network_instability"),
            "retry_storm_risk": Hypothesis("retry_storm_risk"),
            "normal_noise": Hypothesis("normal_noise"),
        }

        global_fail = snapshot["fail_rate"]
        p95_latency = snapshot["p95_latency"]

        # --- Global signals ---
        if global_fail > 0.25:
            hypotheses["retry_storm_risk"].add(
                0.4, f"High global failure rate ({global_fail})"
            )

        if p95_latency and p95_latency > 500:
            hypotheses["network_instability"].add(
                0.4, f"High global latency p95={p95_latency}ms"
            )

        # --- Issuer-level reasoning ---
        for issuer, info in snapshot["issuers"].items():
            fail_rate = info["fail_rate"]
            count = info["count"]

            if count < 5:
                continue  # insufficient data

            if fail_rate > 0.35:
                hypotheses["issuer_degradation"].add(
                    0.5,
                    f"{issuer} failure rate high ({fail_rate})"
                )

            if fail_rate > 0.2 and global_fail < 0.2:
                hypotheses["issuer_degradation"].add(
                    0.3,
                    f"{issuer} failing while others are healthy"
                )

        # --- Default / uncertainty handling ---
        if all(h.score < 0.3 for h in hypotheses.values()):
            hypotheses["normal_noise"].add(
                0.6, "No strong degradation signals detected"
            )

        # --- Normalize into confidence ---
        total_score = sum(max(h.score, 0) for h in hypotheses.values()) or 1.0

        beliefs = []
        for h in hypotheses.values():
            confidence = round(h.score / total_score, 2)
            beliefs.append({
                "hypothesis": h.name,
                "confidence": confidence,
                "evidence": h.evidence
            })

        beliefs.sort(key=lambda x: x["confidence"], reverse=True)

        return {
            "beliefs": beliefs,
            "summary": self._summarize(beliefs)
        }

    def _summarize(self, beliefs: List[Dict]) -> str:
        top = beliefs[0]
        if top["confidence"] < 0.4:
            return "No dominant failure pattern detected."
        return (
            f"Most likely issue: {top['hypothesis']} "
            f"(confidence={top['confidence']})"
        )
