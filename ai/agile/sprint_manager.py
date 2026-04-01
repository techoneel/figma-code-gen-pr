# Sprint Manager (AI Agile)

from ai.workflows.contract_orchestrator import run_feature as run_contract_flow
from ai.workflows.validation_orchestrator import validate_and_generate_tests

class SprintManager:
    def __init__(self):
        self.backlog = []

    def create_backlog(self, feature: str):
        # naive decomposition; replace with Planner agent later
        self.backlog = [
            f"Design DB for {feature}",
            f"Build API for {feature}",
            f"Build UI for {feature}"
        ]
        return self.backlog

    def run_sprint(self, feature: str):
        # End-to-end execution using contract-aware flow
        result = run_contract_flow(feature)

        validation = validate_and_generate_tests(
            result.get("schema", {}),
            result.get("api_contracts", []),
            result.get("ui_contracts", [])
        )

        return {
            "feature": feature,
            "artifacts": result,
            "validation": validation
        }
