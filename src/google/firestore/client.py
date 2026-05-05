# src/google/firestore/client.py
# GROUP: google.firestore
# DESCRIPTION: Firestore low-level client (CRUD for AI Admin system)

import logging
from typing import Any, Dict, Optional

from google.cloud import firestore
from google.cloud.firestore import DocumentSnapshot

logger = logging.getLogger("google.firestore.client")


class FirestoreClient:
    """
    Thin wrapper over Firestore.

    Used ONLY by IndexService.
    No business logic here.
    """

    def __init__(self):
        self.db = firestore.Client()
        logger.info("🔥 FirestoreClient initialized")

    # =========================
    # SET / CREATE
    # =========================
    def set_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> None:
        logger.info("🟢 SET | %s/%s", collection, doc_id)
        self.db.collection(collection).document(doc_id).set(data)

    # =========================
    # UPDATE (partial)
    # =========================
    def update_document(self, collection: str, doc_id: str, update: Dict[str, Any]) -> None:
        logger.info("🟡 UPDATE | %s/%s", collection, doc_id)
        self.db.collection(collection).document(doc_id).update(update)

    # =========================
    # GET (SAFE SNAPSHOT HANDLING)
    # =========================
    def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        logger.info("🔵 GET | %s/%s", collection, doc_id)

        doc_ref = self.db.collection(collection).document(doc_id)
        doc: DocumentSnapshot = doc_ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        return data if data is not None else None

    # =========================
    # EXISTS
    # =========================
    def exists(self, collection: str, doc_id: str) -> bool:
        doc_ref = self.db.collection(collection).document(doc_id)
        doc: DocumentSnapshot = doc_ref.get()

        return bool(doc.exists)