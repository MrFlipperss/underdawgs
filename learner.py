import json
import os
from typing import Dict

STATE_FILE = os.path.join("data", "learner_state.json")


class Learner:
    """
    Learner with persisted state.
    Tracks trust scores for actions and saves them to disk.
    """

    def __init__(self):
        self.action_trust: Dict[str, float] = {
            "limit_retries": 0.5,
            "throttle_issuer": 0.5,
            "increase_timeout": 0.5
        }
        self._load_state()

    # ---------- Persistence ----------

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                if "action_trust" in data:
                    self.action_trust.update(data["action_trust"])
                print("[LEARNER] Loaded persisted state:", self.action_trust)
            except Exception as e:
                print("[LEARNER] Failed to load state, using defaults:", e)

    def _save_state(self):
        os.makedirs("data", exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(
                {"action_trust": self.action_trust},
                f,
                indent=2
            )

    # ---------- Learning ----------

    def learn(self, decision: Dict, execution: Dict):
        action = execution["action"]
        success = execution.get("success")

        # No learning if no outcome
        if success is None:
            return

        previous = self.action_trust.get(action, 0.5)

        if success:
            updated = min(1.0, previous + 0.05)
        else:
            updated = max(0.0, previous - 0.1)

        self.action_trust[action] = updated
        self._save_state()

        print(
            f"[LEARNER] Updated trust for '{action}': "
            f"{previous:.2f} → {updated:.2f}"
        )

    def snapshot(self):
        return {
            "action_trust": dict(self.action_trust)
        }
