# src/google/sheets/client.py
# GROUP: google.sheets
# DESCRIPTION: Advanced Google Sheets ingestion system (queue + full read API + retry + audit logging)

import logging
import time
from typing import List, Dict, Any, Optional, Tuple

from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

from src.google.auth import load_service_account
from src.config.config import load_config

logger = logging.getLogger("google.sheets.client")

config = load_config()


# =========================
# RETRY CONFIG
# =========================
MAX_RETRIES = 5
BASE_DELAY = 1.5


class GoogleSheetsClient:
    """
    Advanced Sheets ingestion layer.

    Features:
    - full sheet / range / cell access
    - ingestion queue system
    - retry + backoff for API calls
    - structured audit logging
    """

    def __init__(self):
        self.credentials = load_service_account()

        self.service = build(
            "sheets",
            "v4",
            credentials=self.credentials,
            cache_discovery=False,
        )

        self.sheet_id = config.google.search.api_key  # placeholder safety fallback

        # FIX: proper env must be injected via config.google.sheets_id (you must add it)
        self.sheet_id = getattr(config.google, "sheets_id", None)

        self.sources_tab = "sources"

        if not self.sheet_id:
            logger.error("❌ Missing GOOGLE_SHEETS_ID in config!")

    # =========================================================
    # RETRY WRAPPER
    # =========================================================
    def _retry(self, fn, context: str):
        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return fn()

            except HttpError as e:
                last_error = e

                logger.warning(
                    "Sheets API error [%s] attempt %s/%s: %s",
                    context,
                    attempt,
                    MAX_RETRIES,
                    str(e),
                )

                time.sleep(BASE_DELAY * attempt)

            except Exception as e:
                logger.exception("Unexpected error [%s]: %s", context, e)
                raise

        logger.error("❌ Max retries reached for: %s", context)
        raise last_error

    # =========================================================
    # AUDIT LOGGING
    # =========================================================
    def _audit(self, action: str, payload: Dict[str, Any]):
        logger.info(
            "[SHEETS-AUDIT] action=%s payload=%s",
            action,
            payload,
        )

    # =========================================================
    # SHEET STRUCTURE INIT
    # =========================================================
    def ensure_structure(self) -> None:
        if not self.sheet_id:
            return

        def _run():
            sheet = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()

            existing = [
                s["properties"]["title"]
                for s in sheet.get("sheets", [])
            ]

            if self.sources_tab not in existing:
                self._create_tab()

            self._ensure_headers()

        self._retry(_run, "ensure_structure")

    def _create_tab(self):
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {"title": self.sources_tab}
                    }
                }
            ]
        }

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.sheet_id,
            body=body,
        ).execute()

        self._audit("create_tab", {"tab": self.sources_tab})

    def _ensure_headers(self):
        range_ = f"{self.sources_tab}!A1:D1"

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=range_,
        ).execute()

        if result.get("values"):
            return

        headers = [["url", "topic", "status", "meta"]]

        self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=range_,
            valueInputOption="RAW",
            body={"values": headers},
        ).execute()

        self._audit("init_headers", {"range": range_})

    # =========================================================
    # FULL SHEET READ
    # =========================================================
    def read_full_sheet(self, tab: str = "sources") -> List[List[str]]:
        range_ = f"{tab}"

        def _run():
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_,
            ).execute()

            return result.get("values", [])

        data = self._retry(_run, "read_full_sheet")

        self._audit("read_full_sheet", {
            "tab": tab,
            "rows": len(data),
        })

        return data

    # =========================================================
    # QUEUE FETCH
    # =========================================================
    def fetch_new_sources(self) -> List[Dict[str, Any]]:
        rows = self.read_full_sheet(self.sources_tab)

        output = []

        for idx, row in enumerate(rows[1:], start=2):
            url = row[0] if len(row) > 0 else ""
            topic = row[1] if len(row) > 1 else ""
            status = row[2] if len(row) > 2 else "NEW"

            if not url:
                continue

            if status.strip().upper() != "NEW":
                continue

            output.append({
                "row": idx,
                "url": url,
                "topic": topic,
                "status": status,
            })

        self._audit("fetch_new_sources", {
            "count": len(output)
        })

        return output

    # =========================================================
    # UPDATE CELL
    # =========================================================
    def update_cell(self, tab: str, cell: str, value: str):
        range_ = f"{tab}!{cell}"

        def _run():
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_,
                valueInputOption="RAW",
                body={"values": [[value]]},
            ).execute()

        self._retry(_run, "update_cell")

        self._audit("update_cell", {
            "tab": tab,
            "cell": cell,
            "value": value,
        })

    # =========================================================
    # STATUS HELPERS
    # =========================================================
    def mark_done(self, row: int):
        self.update_cell(self.sources_tab, f"C{row}", "DONE")

    def mark_error(self, row: int):
        self.update_cell(self.sources_tab, f"C{row}", "ERROR")