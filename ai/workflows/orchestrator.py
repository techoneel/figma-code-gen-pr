# Orchestrator

def run(task: str):
    from ai.agents.planner import plan
    return plan(task)