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
    """
    Minimal Sheets client used ONLY for bootstrap layer.

    Responsibilities:
    - provide authenticated Google Sheets service
    - expose spreadsheet_id
    """

    def __init__(self):
        self.credentials = load_google_credentials()

        self.service = build(
            "sheets",
            "v4",
            credentials=self.credentials,
            cache_discovery=False,
        )

        self.sheet_id = getattr(config.google, "sheets_id", None)

        if not self.sheet_id:
            logger.warning("⚠️ GOOGLE_SHEETS_ID not set in environment")

    def get_service(self):
        return self.service