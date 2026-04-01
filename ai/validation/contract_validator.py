# Contract Validator

class ContractValidator:
    def validate_api_against_schema(self, schema: dict, api_contracts: list):
        errors = []

        for api in api_contracts:
            endpoint = api.get("endpoint", "").strip("/")
            if endpoint not in schema:
                errors.append(f"API endpoint {endpoint} not in schema")
                continue

            schema_fields = set(schema[endpoint])
            request_fields = set(api.get("request", []))

            missing = request_fields - schema_fields
            if missing:
                errors.append(f"Fields {missing} not in schema for {endpoint}")

        return errors

    def validate_ui_against_api(self, api_contracts: list, ui_contracts: list):
        errors = []

        api_map = {api["endpoint"]: api for api in api_contracts}

        for ui in ui_contracts:
            endpoint = ui.get("submit_to")
            if endpoint not in api_map:
                errors.append(f"UI endpoint {endpoint} not found in API")
                continue

            api_fields = set(api_map[endpoint].get("request", []))
            ui_fields = set(ui.get("fields", []))

            mismatch = ui_fields - api_fields
            if mismatch:
                errors.append(f"UI fields {mismatch} not in API for {endpoint}")

        return errors
