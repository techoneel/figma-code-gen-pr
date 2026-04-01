# API Contract Generator

class APIContract:
    def generate(self, task: str, schema: dict):
        """Generate structured API contract from schema"""
        endpoints = []

        for table, fields in schema.items():
            endpoints.append({
                "endpoint": f"/{table}",
                "method": "POST",
                "request": fields,
                "response": ["id"] + fields
            })

        return endpoints
