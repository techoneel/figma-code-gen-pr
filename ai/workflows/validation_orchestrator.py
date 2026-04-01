# Validation + Test Orchestrator

from ai.validation.contract_validator import ContractValidator
from ai.testing.test_generator import TestGenerator


def validate_and_generate_tests(schema, api_contracts, ui_contracts):
    validator = ContractValidator()
    tester = TestGenerator()

    api_errors = validator.validate_api_against_schema(schema, api_contracts)
    ui_errors = validator.validate_ui_against_api(api_contracts, ui_contracts)

    api_tests = tester.generate_api_tests(api_contracts)
    ui_tests = tester.generate_ui_tests(ui_contracts)

    return {
        "api_errors": api_errors,
        "ui_errors": ui_errors,
        "api_tests": api_tests,
        "ui_tests": ui_tests
    }
