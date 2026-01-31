from typing import Dict, List

class Decision:
    """
    Converts beliefs into recommended actions with guardrails.
    """

    def decide(self, reasoning: Dict) -> Dict:
        beliefs = reasoning["beliefs"]

        recommendations = []

        for belief in beliefs:
            name = belief["hypothesis"]
            confidence = belief["confidence"]
            evidence = belief["evidence"]

            # --- Guardrails ---
            top = beliefs[0]
            second = beliefs[1]

            if top["confidence"] - second["confidence"] < 0.1:
                continue


            if name == "issuer_degradation":
                recommendations.append(
                    self._recommend(
                        action="throttle_issuer",
                        confidence=confidence,
                        rationale="Issuer shows elevated failure rates",
                        evidence=evidence,
                        autonomy="recommend_only"
                    )
                )

            elif name == "network_instability":
                recommendations.append(
                    self._recommend(
                        action="increase_timeout",
                        confidence=confidence,
                        rationale="High latency suggests network instability",
                        evidence=evidence,
                        autonomy="recommend_only"
                    )
                )

            elif name == "retry_storm_risk":
                recommendations.append(
                    self._recommend(
                        action="limit_retries",
                        confidence=confidence,
                        rationale="High failure rate risks retry storms",
                        evidence=evidence,
                        autonomy="safe_autonomous"
                    )
                )

        # Fallback: do nothing if no strong signal
        if not recommendations:
            recommendations.append(
                self._recommend(
                    action="observe_only",
                    confidence=1.0,
                    rationale="No dominant risk detected",
                    evidence=[],
                    autonomy="none"
                )
            )

        return {
            "recommendations": recommendations,
            "decision_summary": self._summarize(recommendations)
        }

    def _recommend(self, action, confidence, rationale, evidence, autonomy):
        return {
            "action": action,
            "confidence": round(confidence, 2),
            "rationale": rationale,
            "evidence": evidence,
            "autonomy": autonomy
        }

    def _summarize(self, recs: List[Dict]) -> str:
        top = recs[0]
        if top["action"] == "observe_only":
            return "No intervention recommended at this time."
        return (
            f"Recommended action: {top['action']} "
            f"(confidence={top['confidence']}, autonomy={top['autonomy']})"
        )
