# Schema Extractor (Structured DB Parsing)

import re

class SchemaExtractor:
    def extract(self, db_schema: str):
        """Extract tables and fields from SQL-like schema"""
        tables = {}
        current_table = None

        for line in db_schema.splitlines():
            line = line.strip()

            if line.lower().startswith("create table"):
                current_table = line.split()[2]
                tables[current_table] = []

            elif current_table and line and not line.startswith("--"):
                field = re.split(r"\s+", line)[0]
                if field.lower() not in ["primary", "foreign", ")"]:
                    tables[current_table].append(field)

        return tables
