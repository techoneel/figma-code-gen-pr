# Full Pipeline Orchestrator (CI + Auto Merge + QA Feedback)

from ai.agile.sprint_manager import SprintManager
from ai.agile.gate_orchestrator import GateOrchestrator
from ai.agents.qa import QAAgent

class PipelineOrchestrator:
    def __init__(self):
        self.sprint = SprintManager()
        self.gates = GateOrchestrator()
        self.qa = QAAgent()

    def run(self, feature: str, max_retries: int = 2):
        attempt = 0

        while attempt <= max_retries:
            result = self.sprint.run_sprint(feature)

            decision = self.gates.decide(
                result["validation"],
                result["artifacts"]
            )

            if decision["action"] == "merge":
                return {
                    "status": "merged",
                    "attempt": attempt,
                    "details": decision
                }

            # QA feedback loop
            logs = str(decision["reason"])
            self.qa.apply_fix(None, feature, logs)

            attempt += 1

        return {
            "status": "failed",
            "attempts": attempt
        }
