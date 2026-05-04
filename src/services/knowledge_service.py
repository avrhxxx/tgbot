# src/services/knowledge_service.py
# GROUP: services
# DESCRIPTION: Game knowledge layer (Firestore abstraction + business logic)

import logging
from src.google.firestore.client import FirestoreClient

logger = logging.getLogger("services.knowledge")

firestore = FirestoreClient()


class KnowledgeService:

    # =========================
    # READ KNOWLEDGE
    # =========================
    async def get(self, object_type: str, name: str):
        return await firestore.get_definition(object_type, name)

    # =========================
    # WRITE KNOWLEDGE (NEW LAYER)
    # =========================
    async def create_or_update(self, object_type: str, name: str, definition: dict):
        logger.info("🧠 Saving KNOWLEDGE | %s:%s", object_type, name)

        # 🔥 IMPORTANT: separate namespace from INDEX system
        return await firestore.set_knowledge(
            object_type,
            name,
            definition
        )

    # =========================
    # CHECK KNOWLEDGE
    # =========================
    async def exists(self, object_type: str, name: str):
        return await firestore.get_definition(object_type, name) is not None