# src/google/firestore/client.py
# GROUP: google.firestore
# DESCRIPTION: Firestore low-level client (CRUD for AI Admin system)

import logging
from typing import Any, Dict

from google.cloud import firestore

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
    def set_document(self, collection: str, doc_id: str, data: Dict[str, Any]):
        logger.info("🟢 SET | %s/%s", collection, doc_id)
        self.db.collection(collection).document(doc_id).set(data)

    # =========================
    # UPDATE (partial)
    # =========================
    def update_document(self, collection: str, doc_id: str, update: Dict[str, Any]):
        logger.info("🟡 UPDATE | %s/%s", collection, doc_id)
        self.db.collection(collection).document(doc_id).update(update)

    # =========================
    # GET
    # =========================
    def get_document(self, collection: str, doc_id: str):
        logger.info("🔵 GET | %s/%s", collection, doc_id)
        doc = self.db.collection(collection).document(doc_id).get()

        if not doc.exists:
            return None

        return doc.to_dict()

    # =========================
    # EXISTS
    # =========================
    def exists(self, collection: str, doc_id: str) -> bool:
        doc = self.db.collection(collection).document(doc_id).get()
        return doc.exists