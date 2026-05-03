# src/google/sheets/writer.py
# GROUP: google.sheets
# DESCRIPTION: Schema-driven Sheets writer (relations-ready, production-safe)

import logging
from datetime import datetime

from src.google.sheets.schema import SHEETS_SCHEMA

logger = logging.getLogger("google.sheets.writer")


class SheetsWriter:

    def __init__(self, client):
        self.client = client
        self.service = client.get_service()
        self.sheet_id = client.sheet_id

        logger.info("📊 SheetsWriter initialized | sheet_id=%s", self.sheet_id)

    # =========================
    # SERIALIZATION (SCHEMA-DRIVEN)
    # =========================
    def _serialize(self, sheet: str, row: dict) -> list:

        headers = SHEETS_SCHEMA[sheet]

        serialized = []

        for field in headers:
            if field == "created_at":
                serialized.append(row.get(field) or datetime.utcnow().isoformat())
            else:
                serialized.append(row.get(field))

        return serialized

    # =========================
    # APPEND
    # =========================
    def append_row(self, sheet: str, row: dict):

        logger.info(
            "✍️ Append → sheet=%s type=%s name=%s",
            sheet,
            row.get("type"),
            row.get("name"),
        )

        headers = SHEETS_SCHEMA[sheet]

        # dynamic range (A:G etc.)
        last_column_letter = chr(ord("A") + len(headers) - 1)
        range_ = f"{sheet}!A:{last_column_letter}"

        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=range_,
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [self._serialize(sheet, row)]},
            ).execute()

            logger.info("✅ Row inserted | id=%s", row.get("id"))

        except Exception:
            logger.exception("❌ Append failed")
            raise

    # =========================
    # DUPLICATE CHECK
    # =========================
    def find_by_normalized(self, sheet: str, normalized: str):

        logger.debug("🔎 Lookup normalized=%s", normalized)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:D",
        ).execute()

        rows = result.get("values", [])

        for row in rows:
            if len(row) >= 4 and row[3] == normalized:
                logger.info("⚠️ Duplicate found: %s", normalized)
                return row

        return None

    # =========================
    # NEXT ID
    # =========================
    def get_next_id(self, sheet: str) -> int:

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:A",
        ).execute()

        rows = result.get("values", [])

        if len(rows) <= 1:
            return 1

        ids = [
            int(r[0])
            for r in rows[1:]
            if r and str(r[0]).isdigit()
        ]

        return max(ids, default=0) + 1