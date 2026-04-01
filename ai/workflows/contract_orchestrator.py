# Contract-Aware Orchestrator

from ai.agents.db_agent import DBAgent
from ai.agents.api_agent import APIAgent
from ai.agents.ui_agent import UIAgent
from ai.contracts.schema_extractor import SchemaExtractor
from ai.contracts.api_contract import APIContract
from ai.contracts.ui_contract import UIContract


def run_feature(task: str):
    db = DBAgent()
    api = APIAgent()
    ui = UIAgent()

    extractor = SchemaExtractor()
    api_contract_gen = APIContract()
    ui_contract_gen = UIContract()

    # Step 1: DB Schema
    db_schema = db.generate_schema(task)
    schema = extractor.extract(db_schema)

    # Step 2: API Contract
    api_contracts = api_contract_gen.generate(task, schema)
    api_code = api.generate_api(task, context=str(api_contracts))

    # Step 3: UI Contract
    ui_contracts = ui_contract_gen.generate(api_contracts)
    ui_code = ui.generate_ui(task, context=str(ui_contracts))

    return {
        "schema": schema,
        "api_contracts": api_contracts,
        "ui_contracts": ui_contracts,
        "db": db_schema,
        "api": api_code,
        "ui": ui_code
    }
