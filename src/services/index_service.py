# src/services/index_service.py
# GROUP: services
# DESCRIPTION: Core AI Admin Orchestrator (DSL → Firestore → Sheets sync layer)

import logging
from typing import Dict, Any, Optional

from src.google.firestore.client import FirestoreClient
from src.google.sheets.client import SheetsClient

logger = logging.getLogger("services.index_service")


class IndexService:
    """
    AI ADMIN CORE SYSTEM

    Responsibility:
    - Executes IntentParser DSL commands
    - Writes to Firestore (source of truth)
    - Syncs lightweight index metadata to Google Sheets
    - Manages entity relationships (link system)
    """

    def __init__(self):
        self.firestore = FirestoreClient()
        self.sheets = SheetsClient()

        logger.info("🧠 IndexService initialized (AI Admin Core Online)")

    # =========================
    # ENTRY POINT
    # =========================
    def execute(self, intent: Dict[str, Any]) -> Dict[str, Any]:

        action = intent.get("action")
        obj = intent.get("object")
        name = intent.get("name")
        context = intent.get("context", {})

        logger.info("⚙️ EXECUTE | action=%s object=%s name=%s", action, obj, name)

        # ROUTING
        if action == "add_definition":
            return self._create_entity(obj, name, context)

        if action == "add_knowledge":
            return self._add_knowledge(obj, name, intent.get("knowledge", {}))

        if action == "check_existence":
            return self._exists(obj, name)

        if action == "get_definition":
            return self._get(obj, name)

        if action == "query":
            return {"status": "noop", "message": "No operation executed"}

        raise ValueError(f"Unknown action: {action}")

    # =========================
    # CREATE ENTITY (CORE)
    # =========================
    def _create_entity(self, obj: str, name: str, context: Dict[str, Any]):

        doc_id = name.lower().replace(" ", "_")

        data = {
            "id": doc_id,
            "type": obj,
            "name": name,
            "normalized": doc_id,
            "context": context,
            "lore": "",
            "fields": {},
            "links": {},
        }

        # FIRESTORE (SOURCE OF TRUTH)
        self.firestore.set_document(collection=obj + "s", doc_id=doc_id, data=data)

        # SHEETS (INDEX REGISTER)
        self.sheets.writer.append_row({
            "id": doc_id,
            "type": obj,
            "name": name,
            "normalized": doc_id,
            "parent_type": context.get("parent_type"),
            "parent_name": context.get("parent_name"),
        })

        logger.info("✅ CREATED ENTITY | %s (%s)", name, obj)

        return {
            "status": "created",
            "id": doc_id,
            "type": obj,
            "name": name
        }

    # =========================
    # KNOWLEDGE UPDATE
    # =========================
    def _add_knowledge(self, obj: str, name: str, knowledge: Dict[str, Any]):

        doc_id = name.lower().replace(" ", "_")

        self.firestore.update_document(
            collection=obj + "s",
            doc_id=doc_id,
            update={
                "lore": knowledge.get("lore", ""),
                "gameplay": knowledge.get("gameplay", {}),
                "stats": knowledge.get("stats", {}),
            }
        )

        logger.info("📚 UPDATED KNOWLEDGE | %s", name)

        return {
            "status": "updated_knowledge",
            "id": doc_id
        }

    # =========================
    # EXISTS CHECK
    # =========================
    def _exists(self, obj: str, name: str):

        doc_id = name.lower().replace(" ", "_")

        exists = self.firestore.exists(obj + "s", doc_id)

        return {
            "exists": exists,
            "id": doc_id
        }

    # =========================
    # GET ENTITY
    # =========================
    def _get(self, obj: str, name: str):

        doc_id = name.lower().replace(" ", "_")

        data = self.firestore.get_document(obj + "s", doc_id)

        return {
            "data": data
        }

    # =========================
    # LINK SYSTEM (NEXT PHASE READY)
    # =========================
    def link(self, source_type: str, source: str, relation: str, target_type: str, target: str):

        src_id = source.lower().replace(" ", "_")
        tgt_id = target.lower().replace(" ", "_")

        self.firestore.update_document(
            collection=source_type + "s",
            doc_id=src_id,
            update={
                f"links.{relation}": {
                    "type": target_type,
                    "id": tgt_id
                }
            }
        )

        logger.info("🔗 LINK CREATED | %s -> %s (%s)", source, target, relation)

        return {
            "status": "linked",
            "source": src_id,
            "target": tgt_id,
            "relation": relation
        }