# src/services/index_service.py
# GROUP: services
# DESCRIPTION: Central index engine (single-table architecture for AI-safe indexing)

import logging
import re
from typing import Dict, Any

from src.google.sheets.writer import SheetsWriter

logger = logging.getLogger("services.index")


class IndexService:

    def __init__(self, sheets: SheetsWriter):
        self.sheets = sheets
        logger.info("📦 IndexService initialized (single-table mode: indexes)")

    # =========================
    # NORMALIZATION
    # =========================
    def normalize(self, name: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        logger.debug("🔤 Normalized '%s' → '%s'", name, normalized)
        return normalized

    # =========================
    # MAIN ENTRY
    # =========================
    def handle(self, intent: Dict[str, Any]):

        logger.info("⚙️ Processing intent: %s", intent)

        entity_type = intent["type"]
        name = intent["name"]

        normalized = self.normalize(name)

        logger.info(
            "📍 Processing index | type=%s name=%s normalized=%s",
            entity_type,
            name,
            normalized,
        )

        # =========================
        # DUPLICATE CHECK (GLOBAL)
        # =========================
        existing = self.sheets.find_by_normalized("indexes", normalized)

        if existing:
            logger.warning("⚠️ Duplicate detected | normalized=%s", normalized)
            logger.debug("🔎 Existing row: %s", existing)
            return existing

        # =========================
        # ID GENERATION
        # =========================
        new_id = self.sheets.get_next_id("indexes")

        logger.info("🆔 Generated ID=%s for indexes", new_id)

        # =========================
        # ROW STRUCTURE (STRICT SCHEMA)
        # =========================
        row = {
            "id": new_id,
            "type": entity_type,
            "name": name,
            "normalized": normalized,
        }

        logger.info("📝 Writing row → %s", row)

        self.sheets.append_row("indexes", row)

        logger.info("✅ Successfully inserted index | id=%s", new_id)

        return row