# src/google/sheets/writer.py
# GROUP: google.sheets
# DESCRIPTION: Sheets writer for AI Admin index registry sync

import logging
from typing import Dict, Any

logger = logging.getLogger("google.sheets.writer")


class SheetsWriter:
    """
    Writes index metadata into Google Sheets.

    Acts as:
    - Admin UI layer
    - quick lookup registry
    """

    def __init__(self, sheet_client):
        self.client = sheet_client
        self.sheet_name = "indexes"

        logger.info("📊 SheetsWriter initialized")

    # =========================
    # APPEND ROW
    # =========================
    def append_row(self, row: Dict[str, Any]):

        values = [
            row.get("id"),
            row.get("type"),
            row.get("name"),
            row.get("normalized"),
            row.get("parent_type"),
            row.get("parent_name"),
        ]

        logger.info("🟢 SHEETS APPEND | %s", values)

        self.client.append_row(self.sheet_name, values)