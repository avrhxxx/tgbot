# src/services/index_service.py
# GROUP: services
# DESCRIPTION: Execution layer (Firestore + Sheets) for validated commands

import logging
from typing import Dict, Any

from src.google.firestore.client import FirestoreClient
from src.google.sheets.client import GoogleSheetsClient
from src.google.sheets.writer import SheetsWriter
from src.core.commands.command_model import Command

logger = logging.getLogger("services.index_service")


class IndexService:
    """
    EXECUTION LAYER ONLY

    Responsibilities:
    - Persist validated Command into Firestore
    - Sync index metadata to Sheets
    """

    def __init__(self):
        self.firestore = FirestoreClient()

        self.sheets_client = GoogleSheetsClient()
        self.writer = SheetsWriter(self.sheets_client)

        logger.info("⚙️ IndexService initialized (EXECUTION MODE)")

    # =========================
    # CREATE
    # =========================
    def create(self, command: Command) -> Dict[str, Any]:

        if not command.target:
            raise ValueError("Missing target for create")

        doc_id = self._normalize_id(command.target)

        data = {
            "id": doc_id,
            "type": command.entity,
            "name": command.target,
            "normalized": doc_id,
            "fields": {},
            "stats": {},
            "links": {},
        }

        self.firestore.set_document(
            collection=command.entity + "s",
            doc_id=doc_id,
            data=data
        )

        self.writer.append_row({
            "id": doc_id,
            "type": command.entity,
            "name": command.target,
            "normalized": doc_id,
            "parent_type": command.context.get("parent_type"),
            "parent_name": command.context.get("parent_name"),
        })

        logger.info("✅ CREATE | %s (%s)", command.target, command.entity)

        return {
            "status": "created",
            "id": doc_id
        }

    # =========================
    # UPDATE
    # =========================
    def update(self, command: Command) -> Dict[str, Any]:

        if not command.target:
            raise ValueError("Missing target for update")

        # 🔥 COMPAT LAYER: attr is canonical, field legacy-safe
        attr = command.attr or getattr(command, "field", None)

        if not attr:
            raise ValueError("Missing attribute for update")

        doc_id = self._normalize_id(command.target)

        update_payload = {
            f"fields.{attr}": command.value
        }

        self.firestore.update_document(
            collection=command.entity + "s",
            doc_id=doc_id,
            update=update_payload
        )

        logger.info(
            "🟡 UPDATE | %s.%s = %s",
            command.target,
            attr,
            command.value
        )

        return {
            "status": "updated",
            "id": doc_id
        }

    # =========================
    # DEFINE
    # =========================
    def define(self, command: Command) -> Dict[str, Any]:
        return self.update(command)

    # =========================
    # LINK
    # =========================
    def link_command(self, command: Command) -> Dict[str, Any]:

        if not command.target:
            raise ValueError("Missing source for link")

        relation = command.relation or command.context.get("target")

        if not relation:
            raise ValueError("Missing relation data for link")

        doc_id = self._normalize_id(command.target)
        target_id = self._normalize_id(relation["name"])

        self.firestore.update_document(
            collection=command.entity + "s",
            doc_id=doc_id,
            update={
                f"links.{relation['type']}": {
                    "type": relation["type"],
                    "id": target_id
                }
            }
        )

        logger.info(
            "🔗 LINK | %s -> %s",
            command.target,
            relation["name"]
        )

        return {
            "status": "linked",
            "source": doc_id,
            "target": target_id
        }

    # =========================
    # QUERY
    # =========================
    def query(self, command: Command) -> Dict[str, Any]:

        if not command.target:
            raise ValueError("Missing target for query")

        doc_id = self._normalize_id(command.target)

        data = self.firestore.get_document(
            collection=command.entity + "s",
            doc_id=doc_id
        )

        return {
            "data": data
        }

    # =========================
    # UTILS
    # =========================
    def _normalize_id(self, name: str) -> str:
        return name.lower().replace(" ", "_")