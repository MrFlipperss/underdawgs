from environment.environment import PaymentEnvironment
import learner
import learner
from observer.observer import Observer
from decision import Decision
from executor import Executor
from learner import Learner
import time
from reasoner import Reasoner
import reasoner


def main():
    print("Agent started\n")
    reasoner = Reasoner()
    env = PaymentEnvironment()
    observer = Observer(window_size=20)
    decision = Decision()
    executor = Executor()
    learner = Learner()


    for i in range(30):
        evt = env.step()
        observer.consume(evt)

        print(
            f"[{i+1:02}] {evt.issuer:10} "
            f"{evt.status:7} "
            f"{evt.error_code or '-':12} "
            f"{evt.latency_ms}ms"
        )

    if (i + 1) % 10 == 0:
       snap = observer.snapshot()
       print("\n--- SNAPSHOT ---")
       print(snap)
       result = reasoner.analyze(snap)

    print("\n--- REASONER OUTPUT ---")
    for b in result["beliefs"]:
        print(
        f"{b['hypothesis']:22} "
        f"confidence={b['confidence']:.2f} "
        f"evidence={b['evidence']}"
    )

    decision_out = decision.decide(result, learner.action_trust)

    print("\n--- DECISION OUTPUT ---")
    for r in decision_out["recommendations"]:
        print(
        f"action={r['action']:18} "
        f"confidence={r['confidence']} "
        f"autonomy={r['autonomy']:15} "
        f"rationale={r['rationale']}"
    )

        exec_result = executor.execute(r, snap)
        print("  -> EXECUTION:", exec_result)
        learner.learn(r, exec_result)

    print("\n--- LEARNER STATE ---")
    print(learner.snapshot())

    print("Decision Summary:", decision_out["decision_summary"])
    print("-----------------------\n")
    time.sleep(0.05)

if __name__ == "__main__":
    main()
