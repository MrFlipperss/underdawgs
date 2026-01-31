from typing import Dict
import random

class Executor:
    """
    Executes (or simulates) actions with guardrails.
    """

    def execute(self, recommendation: Dict, snapshot: Dict) -> Dict:
        action = recommendation["action"]
        autonomy = recommendation["autonomy"]

        # --- Hard guardrails ---
        if autonomy == "recommend_only":
            return self._result(
                action,
                executed=False,
                outcome="requires_human_approval",
                detail="Action requires human review"
            )

        if autonomy == "none":
            return self._result(
                action,
                executed=False,
                outcome="no_action",
                detail="Observation only"
            )

        # --- Safe autonomous actions ---
        if action == "limit_retries":
            # simulate effect: slightly reduce failures, reduce latency risk
            success = random.random() < 0.7
            return self._result(
                action,
                executed=True,
                outcome="retry_policy_updated",
                detail="Retry limits applied safely",
                success=success
            )

        # fallback safety
        return self._result(
            action,
            executed=False,
            outcome="blocked",
            detail="Action blocked by executor guardrails"
        )

    def _result(self, action, executed, outcome, detail, success=None):
        return {
            "action": action,
            "executed": executed,
            "outcome": outcome,
            "success": success,
            "detail": detail
        }
