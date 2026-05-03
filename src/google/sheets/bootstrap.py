# src/google/sheets/bootstrap.py
# GROUP: google.sheets
# DESCRIPTION: Single-table Sheets bootstrap (schema-driven, auto-migration ready)

import logging
from googleapiclient.errors import HttpError  # type: ignore

from src.google.sheets.client import GoogleSheetsClient
from src.google.sheets.schema import SHEETS_SCHEMA

logger = logging.getLogger("google.sheets.bootstrap")


class SheetsBootstrap:

    SHEET_NAME = "indexes"

    def __init__(self, client: GoogleSheetsClient):
        self.client = client

    def ensure(self) -> None:

        if not self.client.sheet_id:
            logger.warning("⚠️ SheetsBootstrap skipped (missing SHEET_ID)")
            return

        logger.info("📊 Bootstrapping schema-driven sheets")

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

        headers = SHEETS_SCHEMA[self.SHEET_NAME]

        # dynamic range (A1:G1 etc.)
        last_column_letter = chr(ord("A") + len(headers) - 1)
        range_ = f"{self.SHEET_NAME}!A1:{last_column_letter}1"

        result = self.client.service.spreadsheets().values().get(
            spreadsheetId=self.client.sheet_id,
            range=range_,
        ).execute()

        existing = result.get("values")

        # =========================
        # CASE 1: NO HEADERS → INIT
        # =========================
        if not existing:
            self.client.service.spreadsheets().values().update(
                spreadsheetId=self.client.sheet_id,
                range=range_,
                valueInputOption="RAW",
                body={"values": [headers]},
            ).execute()

            logger.info("🧾 Headers initialized: %s", headers)
            return

        existing_headers = existing[0]

        # =========================
        # CASE 2: MIGRATION (ADD MISSING COLUMNS)
        # =========================
        if existing_headers != headers:
            logger.warning("⚠️ Header mismatch detected → applying migration")

            missing = [h for h in headers if h not in existing_headers]

            if missing:
                logger.info("➕ Adding missing columns: %s", missing)

                new_headers = existing_headers + missing

                last_column_letter = chr(ord("A") + len(new_headers) - 1)
                new_range = f"{self.SHEET_NAME}!A1:{last_column_letter}1"

                self.client.service.spreadsheets().values().update(
                    spreadsheetId=self.client.sheet_id,
                    range=new_range,
                    valueInputOption="RAW",
                    body={"values": [new_headers]},
                ).execute()

                logger.info("✅ Headers updated: %s", new_headers)

            else:
                logger.info("⏭️ Headers already aligned")

            return

        logger.info("⏭️ Headers already exist and match schema")