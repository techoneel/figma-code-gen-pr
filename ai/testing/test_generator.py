# Automated Test Generator

class TestGenerator:
    def generate_api_tests(self, api_contracts: list):
        tests = []

        for api in api_contracts:
            test = f"""
def test_{api['endpoint'].strip('/')}():
    payload = {{{', '.join([f'\"{f}\": \"test\"' for f in api['request']])}}}
    response = client.post('{api['endpoint']}', json=payload)
    assert response.status_code == 200
"""
            tests.append(test)

        return "\n".join(tests)

    def generate_ui_tests(self, ui_contracts: list):
        tests = []

        for ui in ui_contracts:
            test = f"""
def test_ui_{ui['form'].strip('/')}():
    assert render_form('{ui['form']}') is not None
"""
            tests.append(test)

        return "\n".join(tests)
