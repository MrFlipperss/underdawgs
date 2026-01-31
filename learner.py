from typing import Dict

class Learner:
    """
    Updates internal parameters based on execution outcomes.
    """

    def __init__(self):
        # trust score per action
        self.action_trust = {
            "limit_retries": 0.5,
            "throttle_issuer": 0.5,
            "increase_timeout": 0.5
        }

    def learn(self, decision: Dict, execution: Dict):
        action = execution["action"]
        success = execution.get("success")

        if success is None:
            return  # nothing to learn

        # simple reinforcement update
        if success:
            self.action_trust[action] = min(
                1.0, self.action_trust.get(action, 0.5) + 0.05
            )
        else:
            self.action_trust[action] = max(
                0.0, self.action_trust.get(action, 0.5) - 0.1
            )

    def snapshot(self):
        return {
            "action_trust": self.action_trust
        }
