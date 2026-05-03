# src/services/index_service.py
# GROUP: services
# DESCRIPTION: Unified index ingestion engine (AI → single DB table)

import logging
import re
from typing import Dict, Any

from src.google.sheets.writer import SheetsWriter

logger = logging.getLogger("services.index")


class IndexService:

    def __init__(self, sheets: SheetsWriter):
        self.sheets = sheets
        logger.info("📦 IndexService initialized")

    def normalize(self, name: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        logger.debug("🔤 normalize: %s → %s", name, normalized)
        return normalized

    def handle(self, intent: Dict[str, Any]):

        logger.info("⚙️ Intent received: %s", intent)

        name = intent["name"]
        entity_type = intent["type"]

        normalized = self.normalize(name)

        logger.info("📍 Processing | type=%s name=%s", entity_type, name)

        existing = self.sheets.find_by_normalized("indexes", normalized)

        if existing:
            logger.warning("⚠️ Duplicate skipped: %s", normalized)
            return existing

        new_id = self.sheets.get_next_id("indexes")

        row = {
            "id": new_id,
            "type": entity_type,
            "name": name,
            "normalized": normalized,
            "created_at": None,
        }

        logger.info("📝 Writing row: %s", row)

        self.sheets.append_row("indexes", row)

        logger.info("✅ Inserted successfully | id=%s", new_id)

        return row