# UI Contract Generator

class UIContract:
    def generate(self, api_contracts):
        """Generate UI bindings from API contracts"""
        ui_bindings = []

        for api in api_contracts:
            ui_bindings.append({
                "form": api["endpoint"],
                "fields": api["request"],
                "submit_to": api["endpoint"]
            })

        return ui_bindings
