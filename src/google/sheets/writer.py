# src/google/sheets/writer.py
# GROUP: google.sheets
# DESCRIPTION: Minimal Sheets writer (append + lookup + id generator)

import logging

logger = logging.getLogger("google.sheets.writer")


class SheetsWriter:

    def __init__(self, client):
        self.client = client
        self.service = client.get_service()
        self.sheet_id = client.sheet_id

        logger.info("📊 SheetsWriter initialized | sheet_id=%s", self.sheet_id)

    # -------------------------
    # APPEND ROW
    # -------------------------
    def append_row(self, sheet: str, row: dict):

        logger.info("✍️ Appending row → sheet=%s", sheet)
        logger.debug("📦 Row payload: %s", row)

        values = [[
            row["id"],
            row["name"],
            row["normalized"],
        ]]

        self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:C",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()

        logger.info("✅ Row appended successfully → sheet=%s id=%s", sheet, row["id"])

    # -------------------------
    # DUPLICATE CHECK
    # -------------------------
    def find_by_normalized(self, sheet: str, normalized: str):

        logger.debug("🔎 Searching duplicates | sheet=%s norm=%s", sheet, normalized)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:C",
        ).execute()

        rows = result.get("values", [])

        for row in rows:
            if len(row) >= 3 and row[2] == normalized:
                logger.warning("⚠️ Duplicate found in %s → %s", sheet, normalized)
                return row

        logger.debug("✔️ No duplicate found")
        return None

    # -------------------------
    # ID GENERATION
    # -------------------------
    def get_next_id(self, sheet: str) -> int:

        logger.debug("🆔 Calculating next ID for sheet=%s", sheet)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=f"{sheet}!A:A",
        ).execute()

        rows = result.get("values", [])

        if len(rows) <= 1:
            logger.debug("🆕 Empty sheet → starting ID=1")
            return 1

        ids = [
            int(r[0])
            for r in rows[1:]
            if r and str(r[0]).isdigit()
        ]

        next_id = max(ids, default=0) + 1

        logger.debug("📈 Next ID calculated: %s", next_id)

        return next_id