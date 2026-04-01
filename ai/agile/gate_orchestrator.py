# Gate Orchestrator (Quality Gates)

class GateOrchestrator:
    def __init__(self, threshold_score: int = 8):
        self.threshold_score = threshold_score

    def run_contract_gate(self, validation):
        api_errors = validation.get("api_errors", [])
        ui_errors = validation.get("ui_errors", [])
        return {
            "passed": len(api_errors) == 0 and len(ui_errors) == 0,
            "errors": api_errors + ui_errors
        }

    def run_test_gate(self, validation):
        # Placeholder: assume tests generated; CI should execute them
        api_tests = validation.get("api_tests")
        ui_tests = validation.get("ui_tests")
        return {
            "passed": bool(api_tests) and bool(ui_tests),
            "errors": [] if (api_tests and ui_tests) else ["Missing tests"]
        }

    def run_llm_judge(self, artifacts):
        # Placeholder scoring; replace with real LLM-as-judge
        score = 8
        return {
            "passed": score >= self.threshold_score,
            "score": score
        }

    def decide(self, validation, artifacts):
        contract_gate = self.run_contract_gate(validation)
        if not contract_gate["passed"]:
            return {"action": "fix", "reason": contract_gate}

        test_gate = self.run_test_gate(validation)
        if not test_gate["passed"]:
            return {"action": "fix", "reason": test_gate}

        judge = self.run_llm_judge(artifacts)
        if not judge["passed"]:
            return {"action": "fix", "reason": judge}

        return {"action": "merge", "reason": {"score": judge["score"]}}
