# src/google/sheets/schema.py
# GROUP: google.sheets
# DESCRIPTION: Unified single-table schema (indexes DB model)

SHEETS_SCHEMA: dict[str, list[str]] = {
    "indexes": ["id", "type", "name", "normalized", "created_at"],
}