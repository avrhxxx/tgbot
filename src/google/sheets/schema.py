# src/google/sheets/schema.py
# GROUP: google.sheets
# DESCRIPTION: Minimal game index schema (ID → name → type mapping structure)

SHEETS_SCHEMA: dict[str, list[str]] = {
    "buildings": ["id", "name", "type"],
    "heroes": ["id", "name", "faction", "rarity"],
    "items": ["id", "name", "category"],
    "resources": ["id", "name", "type"],
    "events": ["id", "name", "type"],
}