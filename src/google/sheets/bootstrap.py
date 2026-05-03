# src/google/sheets/bootstrap.py
# GROUP: google.sheets
# DESCRIPTION: Single-table Sheets bootstrap (indexes only)

import logging
from googleapiclient.errors import HttpError  # type: ignore

from src.google.sheets.client import GoogleSheetsClient

logger = logging.getLogger("google.sheets.bootstrap")


class SheetsBootstrap:

    SHEET_NAME = "indexes"
    HEADERS = ["id", "type", "name", "normalized", "created_at"]

    def __init__(self, client: GoogleSheetsClient):
        self.client = client

    def ensure(self) -> None:

        if not self.client.sheet_id:
            logger.warning("⚠️ SheetsBootstrap skipped (missing SHEET_ID)")
            return

        logger.info("📊 Bootstrapping single-table schema (indexes)")

        self._ensure_tab()
        self._ensure_headers()

        logger.info("✅ Sheets bootstrap completed")

    def _ensure_tab(self) -> None:
        try:
            sheet = self.client.service.spreadsheets().get(
                spreadsheetId=self.client.sheet_id
            ).execute()

            tabs = [s["properties"]["title"] for s in sheet.get("sheets", [])]

            if self.SHEET_NAME in tabs:
                logger.info("⏭️ Sheet exists: %s", self.SHEET_NAME)
                return

            body = {
                "requests": [
                    {"addSheet": {"properties": {"title": self.SHEET_NAME}}}
                ]
            }

            self.client.service.spreadsheets().batchUpdate(
                spreadsheetId=self.client.sheet_id,
                body=body,
            ).execute()

            logger.info("➕ Created sheet: %s", self.SHEET_NAME)

        except HttpError:
            logger.exception("❌ Failed to create sheet")
            raise

    def _ensure_headers(self) -> None:

        range_ = f"{self.SHEET_NAME}!A1:E1"

        result = self.client.service.spreadsheets().values().get(
            spreadsheetId=self.client.sheet_id,
            range=range_,
        ).execute()

        if result.get("values"):
            logger.info("⏭️ Headers already exist: %s", self.SHEET_NAME)
            return

        self.client.service.spreadsheets().values().update(
            spreadsheetId=self.client.sheet_id,
            range=range_,
            valueInputOption="RAW",
            body={"values": [self.HEADERS]},
        ).execute()

        logger.info("🧾 Headers initialized: %s", self.HEADERS)