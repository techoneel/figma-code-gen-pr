# QA Agent (Self-Healing Loop)

class QAAgent:
    def analyze_failure(self, logs: str) -> str:
        """Analyze CI/CD logs and return a fix suggestion"""
        return f"Fix issues based on logs: {logs}"

    def apply_fix(self, developer, task: str, logs: str) -> str:
        """Re-run developer agent with fix context"""
        fix_task = self.analyze_failure(logs)
        return developer.generate_code(f"{task}\nFix: {fix_task}")
