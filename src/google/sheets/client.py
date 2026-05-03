# src/google/sheets/client.py
# GROUP: google.sheets
# DESCRIPTION: Minimal Sheets API client (MVP-safe, dependency-injected auth)

import logging
from googleapiclient.discovery import build  # type: ignore

from src.config.config import load_config

logger = logging.getLogger("google.sheets.client")

config = load_config()


class GoogleSheetsClient:
    """
    Minimal Google Sheets client.

    Responsibilities:
    - hold authenticated Google Sheets service
    - expose spreadsheet_id
    - no business logic
    """

    def __init__(self, credentials):
        self.credentials = credentials

        logger.info("📊 Sheets client initializing | creds=%s", bool(credentials))

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
            logger.warning("⚠️ GOOGLE_SHEET_ID missing in environment")

        logger.info("📊 Sheets client initialized")