# src/google/sheets/client.py
# GROUP: google.sheets
# DESCRIPTION: Minimal Sheets API client wrapper for bootstrap + schema engine

import logging
from googleapiclient.discovery import build  # type: ignore

from src.google.auth import load_google_credentials
from src.config.config import load_config

logger = logging.getLogger("google.sheets.client")

config = load_config()


class GoogleSheetsClient:
    def __init__(self):
        logger.info("📊 Initializing Google Sheets client...")

        self.credentials = load_google_credentials()

        self.service = build(
            "sheets",
            "v4",
            credentials=self.credentials,
            cache_discovery=False,
        )

        self.sheet_id = config.google.sheets_id

        if self.sheet_id:
            logger.info("🟢 Sheets ID loaded successfully")
        else:
            logger.warning("⚠️ GOOGLE_SHEET_ID is missing (Sheets disabled)")

        logger.info("📊 Sheets client initialized")

    def get_service(self):
        return self.service