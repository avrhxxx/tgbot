# src/google/sheets/writer.py
# GROUP: google.sheets
# DESCRIPTION: Production-safe Sheets writer (indexes-only DB model)

import logging
from datetime import datetime

logger = logging.getLogger("google.sheets.writer")


class SheetsWriter:

    def __init__(self, client):
        self.client = client
        self.service = client.get_service()
        self.sheet_id = client.sheet_id

        logger.info("📊 SheetsWriter initialized | sheet_id=%s", self.sheet_id)

    def _serialize(self, row: dict) -> list:
        return [
            row.get("id"),
            row.get("type"),
            row.get("name"),
            row.get("normalized"),
            row.get("created_at", datetime.utcnow().isoformat()),
        ]

    def append_row(self, sheet: str, row: dict):

        logger.info("✍️ Append → sheet=%s type=%s name=%s",
                    sheet, row.get("type"), row.get("name"))

        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range="indexes!A:E",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [self._serialize(row)]},
            ).execute()

            logger.info("✅ Row inserted | id=%s", row.get("id"))

        except Exception as e:
            logger.exception("❌ Append failed")
            raise

    def find_by_normalized(self, sheet: str, normalized: str):

        logger.debug("🔎 Lookup normalized=%s", normalized)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range="indexes!A:D",
        ).execute()

        rows = result.get("values", [])

        for row in rows:
            if len(row) >= 4 and row[3] == normalized:
                logger.info("⚠️ Duplicate found: %s", normalized)
                return row

        return None

    def get_next_id(self, sheet: str) -> int:

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range="indexes!A:A",
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