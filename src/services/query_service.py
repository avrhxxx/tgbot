# src/services/query_service.py
# GROUP: services
# DESCRIPTION: Read-only query engine for game index database (Sheets)

import logging
from typing import List, Dict, Any

from src.google.sheets.writer import SheetsWriter

logger = logging.getLogger("services.query")


class QueryService:

    def __init__(self, sheets: SheetsWriter):
        self.sheets = sheets
        logger.info("🔎 QueryService initialized")

    def _get_all(self) -> List[List[str]]:
        result = self.sheets.service.spreadsheets().values().get(
            spreadsheetId=self.sheets.sheet_id,
            range="indexes!A:F",
        ).execute()

        return result.get("values", [])

    # -------------------------
    # HEROES
    # -------------------------
    def get_heroes(self) -> List[str]:
        rows = self._get_all()

        return [
            r[2]
            for r in rows[1:]
            if len(r) >= 3 and r[1] == "hero"
        ]

    # -------------------------
    # SKILLS BY HERO
    # -------------------------
    def get_skills_by_hero(self, hero_name: str) -> List[str]:
        rows = self._get_all()

        return [
            r[2]
            for r in rows[1:]
            if len(r) >= 5
            and r[1] == "skill"
            and r[4] == hero_name
        ]

    # -------------------------
    # COUNT BY TYPE
    # -------------------------
    def count_by_type(self, entity_type: str) -> int:
        rows = self._get_all()

        return sum(
            1 for r in rows[1:]
            if len(r) >= 2 and r[1] == entity_type
        )