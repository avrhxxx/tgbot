# GROUP: integrations.firestore
# DESCRIPTION: Firestore sync adapter (NON-CORE, backup layer only)

from typing import Dict, Any
import logging

logger = logging.getLogger("firestore")


class FirestoreClient:
    """
    Firestore is ONLY a sync + persistence layer.
    It must never be source of truth.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.enabled = False  # flip later when credentials ready

    # =========================================
    # ENTITY SYNC
    # =========================================

    def save_entity(self, entity_id: str, data: Dict[str, Any]):
        if not self.enabled:
            logger.info(f"[Firestore disabled] save_entity {entity_id}")
            return

        logger.info(f"[Firestore] saving entity={entity_id}")

        # TODO: real Firestore integration later

    # =========================================
    # RELATION SYNC
    # =========================================

    def save_relation(self, relation: Dict[str, Any]):
        if not self.enabled:
            logger.info(f"[Firestore disabled] save_relation {relation}")
            return

        logger.info(f"[Firestore] saving relation={relation}")

    # =========================================
    # STATE SYNC (FULL SNAPSHOT)
    # =========================================

    def sync_state(self, state: Dict[str, Any]):
        if not self.enabled:
            logger.info("[Firestore disabled] sync_state called")
            return

        logger.info("[Firestore] syncing full state snapshot")