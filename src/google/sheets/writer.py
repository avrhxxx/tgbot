# src/google/sheets/writer.py
# GROUP: google.sheets
# DESCRIPTION: Production-safe Sheets writer (strict schema, indexes-only, AI-safe)

import logging
from datetime import datetime

logger = logging.getLogger("google.sheets.writer")


class SheetsWriter:

    SCHEMA = ["id", "type", "name", "normalized", "created_at"]

    def __init__(self, client):
        self.client = client
        self.service = client.get_service()
        self.sheet_id = client.sheet_id

        logger.info("📊 SheetsWriter initialized | sheet_id=%s", self.sheet_id)

    # =========================
    # SERIALIZER (STRICT SCHEMA)
    # =========================
    def _serialize(self, row: dict) -> list:

        serialized = [
            row.get("id"),
            row.get("type"),
            row.get("name"),
            row.get("normalized"),
            row.get("created_at", datetime.utcnow().isoformat()),
        ]

        logger.debug("📦 Serialized row: %s", serialized)

        return serialized

    # =========================
    # APPEND ROW
    # =========================
    def append_row(self, sheet: str, row: dict):

        logger.info("✍️ Appending row → sheet=%s", sheet)
        logger.debug("📦 Raw row: %s", row)

        values = [self._serialize(row)]

        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=f"{sheet}!A:E",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": values},
            ).execute()

            logger.info(
                "✅ Row appended → sheet=%s id=%s type=%s",
                sheet,
                row.get("id"),
                row.get("type"),
            )

        except Exception as e:
            logger.exception("❌ Failed to append row → sheet=%s", sheet)
            raise

    # =========================
    # DUPLICATE CHECK
    # =========================
    def find_by_normalized(self, sheet: str, normalized: str):

        logger.debug("🔎 Searching duplicates | sheet=%s norm=%s", sheet, normalized)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:D",
        ).execute()

        rows = result.get("values", [])

        for row in rows:
            if len(row) >= 4 and row[3] == normalized:
                logger.warning("⚠️ Duplicate found → %s", normalized)
                return row

        logger.debug("✔️ No duplicate found")
        return None

    # =========================
    # ID GENERATION
    # =========================
    def get_next_id(self, sheet: str) -> int:

        logger.debug("🆔 Calculating next ID | sheet=%s", sheet)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:A",
        ).execute()

        rows = result.get("values", [])

        if len(rows) <= 1:
            logger.debug("🆕 Empty sheet → ID=1")
            return 1

        ids = [
            int(r[0])
            for r in rows[1:]
            if r and str(r[0]).isdigit()
        ]

        next_id = max(ids, default=0) + 1

        logger.debug("📈 Next ID computed: %s", next_id)

        return next_id