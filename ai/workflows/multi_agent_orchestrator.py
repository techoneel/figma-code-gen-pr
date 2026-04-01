# Multi-Agent Orchestrator

from ai.agents.ui_agent import UIAgent
from ai.agents.api_agent import APIAgent
from ai.agents.db_agent import DBAgent


def run_full_feature(task: str):
    ui = UIAgent()
    api = APIAgent()
    db = DBAgent()

    ui_code = ui.generate_ui(task)
    api_code = api.generate_api(task)
    db_schema = db.generate_schema(task)

    return {
        "ui": ui_code,
        "api": api_code,
        "db": db_schema
    }
