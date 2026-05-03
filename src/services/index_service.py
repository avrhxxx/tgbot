# src/services/index_service.py
# GROUP: services
# DESCRIPTION: Game index engine (normalize, dedup, id generation)

import logging
import re
from typing import Dict, Any

from src.google.sheets.writer import SheetsWriter

logger = logging.getLogger("services.index")


class IndexService:

    def __init__(self, sheets: SheetsWriter):
        self.sheets = sheets
        logger.info("📦 IndexService initialized")

    # -------------------------
    # NORMALIZATION
    # -------------------------
    def normalize(self, name: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        logger.debug("🔤 Normalized '%s' → '%s'", name, normalized)
        return normalized

    # -------------------------
    # MAIN ENTRY
    # -------------------------
    def handle(self, intent: Dict[str, Any]):

        logger.info("⚙️ Processing intent: %s", intent)

        entity_type = intent["type"]
        name = intent["name"]

        sheet = self._resolve_sheet(entity_type)
        normalized = self.normalize(name)

        logger.info(
            "📍 Resolved target | type=%s sheet=%s name=%s",
            entity_type,
            sheet,
            name,
        )

        existing = self.sheets.find_by_normalized(sheet, normalized)

        if existing:
            logger.warning("⚠️ Duplicate detected in sheet=%s | skipping insert", sheet)
            logger.debug("🔎 Existing row: %s", existing)
            return existing

        new_id = self.sheets.get_next_id(sheet)

        logger.info("🆔 Generated new ID=%s for sheet=%s", new_id, sheet)

        row = {
            "id": new_id,
            "name": name,
            "normalized": normalized,
        }

        logger.info("📝 Writing new row → %s", row)

        self.sheets.append_row(sheet, row)

        logger.info("✅ Successfully inserted index into %s", sheet)

        return row

    # -------------------------
    # SHEET ROUTING
    # -------------------------
    def _resolve_sheet(self, entity_type: str) -> str:

        mapping = {
            "building": "buildings",
            "hero": "heroes",
            "item": "items",
            "resource": "resources",
        }

        sheet = mapping.get(entity_type, "misc")

        logger.debug("🧭 Sheet mapping: %s → %s", entity_type, sheet)

        return sheet