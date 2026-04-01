# Dependency-Aware Orchestrator (DB → API → UI)

from ai.agents.db_agent import DBAgent
from ai.agents.api_agent import APIAgent
from ai.agents.ui_agent import UIAgent


def run_feature(task: str):
    db = DBAgent()
    api = APIAgent()
    ui = UIAgent()

    # Step 1: Generate DB Schema
    db_schema = db.generate_schema(task)

    # Step 2: API uses DB schema
    api_context = f"DB Schema:\n{db_schema}"
    api_code = api.generate_api(task, context=api_context)

    # Step 3: UI uses API contract
    ui_context = f"API Code:\n{api_code}"
    ui_code = ui.generate_ui(task, context=ui_context)

    return {
        "db": db_schema,
        "api": api_code,
        "ui": ui_code
    }
