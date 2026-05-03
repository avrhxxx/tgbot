# src/google/sheets/bootstrap.py
# GROUP: google.sheets
# DESCRIPTION: Idempotent Google Sheets schema initializer (create tabs + headers once)

import logging
from typing import List

from googleapiclient.errors import HttpError  # type: ignore

from src.google.sheets.schema import SHEETS_SCHEMA
from src.google.sheets.client import GoogleSheetsClient

logger = logging.getLogger("google.sheets.bootstrap")


class SheetsBootstrap:
    """
    Lightweight initializer for game index sheets.

    Responsibilities:
    - ensure tabs exist
    - ensure headers exist
    - avoid duplicates (idempotent)
    """

    def __init__(self, client: GoogleSheetsClient):
        self.client = client

    # =========================
    # PUBLIC ENTRYPOINT
    # =========================
    def ensure(self) -> None:
        if not self.client.sheet_id:
            logger.warning("SheetsBootstrap skipped (no SHEET_ID)")
            return

        logger.info("📊 Starting Sheets schema bootstrap...")

        self._ensure_tabs()
        self._ensure_headers()

        logger.info("✅ Sheets schema bootstrap completed")

    # =========================
    # TABS
    # =========================
    def _ensure_tabs(self) -> List[str]:
        try:
            sheet = self.client.service.spreadsheets().get(
                spreadsheetId=self.client.sheet_id
            ).execute()

            existing_tabs = [
                s["properties"]["title"]
                for s in sheet.get("sheets", [])
            ]

            for tab in SHEETS_SCHEMA.keys():
                if tab not in existing_tabs:
                    self._create_tab(tab)

            return existing_tabs

        except HttpError as e:
            logger.error("❌ Failed to fetch sheet structure: %s", e)
            raise

    def _create_tab(self, tab_name: str) -> None:
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {"title": tab_name}
                    }
                }
            ]
        }

        self.client.service.spreadsheets().batchUpdate(
            spreadsheetId=self.client.sheet_id,
            body=body,
        ).execute()

        logger.info("➕ Created sheet tab: %s", tab_name)

    # =========================
    # HEADERS
    # =========================
    def _ensure_headers(self) -> None:
        for tab_name, headers in SHEETS_SCHEMA.items():
            range_ = f"{tab_name}!A1:{chr(64 + len(headers))}1"

            result = self.client.service.spreadsheets().values().get(
                spreadsheetId=self.client.sheet_id,
                range=range_,
            ).execute()

            if result.get("values"):
                logger.info("⏭️ Headers already exist: %s", tab_name)
                continue

            self.client.service.spreadsheets().values().update(
                spreadsheetId=self.client.sheet_id,
                range=range_,
                valueInputOption="RAW",
                body={"values": [headers]},
            ).execute()

            logger.info("🧾 Headers initialized: %s -> %s", tab_name, headers)