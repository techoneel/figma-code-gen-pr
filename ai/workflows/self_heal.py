# Self-Healing Workflow

from ai.agents.qa import QAAgent
from ai.agents.developer import DeveloperAgent


def self_heal(task: str, logs: str):
    qa = QAAgent()
    dev = DeveloperAgent()

    fixed_code = qa.apply_fix(dev, task, logs)
    return fixed_code
