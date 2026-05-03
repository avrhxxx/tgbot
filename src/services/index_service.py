# src/services/index_service.py
# GROUP: services
# DESCRIPTION: Unified index ingestion engine (relational context mapping)

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
        return normalized

    def handle(self, intent: Dict[str, Any]):

        logger.info("⚙️ Intent received: %s", intent)

        name = intent["name"]

        entity_type = intent.get("object") or intent.get("type")
        if not entity_type:
            raise ValueError("Missing entity_type in intent")

        context = intent.get("context", {}) or {}

        # =========================
        # RELATION EXTRACTION
        # =========================
        parent_name = None
        parent_type = None

        if "hero" in context:
            parent_name = context["hero"]
            parent_type = "hero"

        normalized = self.normalize(name)

        logger.info(
            "📍 Processing | type=%s name=%s parent=%s",
            entity_type,
            name,
            parent_name,
        )

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
            "parent_type": parent_type,
            "parent_name": parent_name,
            "created_at": None,
        }

        logger.info("📝 Writing row: %s", row)

        self.sheets.append_row("indexes", row)

        logger.info("✅ Inserted successfully | id=%s", new_id)

        return row