# src/google/sheets/schema.py
# GROUP: google.sheets
# DESCRIPTION: Unified single-table schema (indexes DB model with relations support)

SHEETS_SCHEMA: dict[str, list[str]] = {
    "indexes": [
        "id",
        "type",
        "name",
        "normalized",
        "parent_type",
        "parent_name",
        "created_at",
    ],
}