# src/wiki/knowledge/firestore_client.py

import logging
import time
import hashlib
from typing import List, Dict, Any, Optional

from google.cloud import firestore  # type: ignore
from src.google.auth import load_service_account

logger = logging.getLogger("wiki.firestore")


class FirestoreClient:
    def __init__(self):
        credentials = load_service_account()
        self.db = firestore.Client(credentials=credentials)
        self.collection = "knowledge"

    # =========================
    # UTILS
    # =========================
    def _doc_id(self, url: str) -> str:
        """
        Stable document ID based on URL.
        Prevents duplicates.
        """
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    # =========================
    # WRITE (IDEMPOTENT)
    # =========================
    async def add_knowledge(
        self,
        topic: str,
        url: str,
        content: str,
        embedding: Optional[List[float]] = None,
    ) -> bool:
        """
        Stores knowledge entry safely (no duplicates).
        Returns True if created, False if already exists.
        """

        doc_id = self._doc_id(url)
        ref = self.db.collection(self.collection).document(doc_id)

        # 🔥 CHECK IF EXISTS
        existing = ref.get()
        if existing.exists:
            logger.info("Skipping duplicate URL: %s", url)
            return False

        doc = {
            "topic": topic.lower().strip(),
            "url": url,
            "content": content,
            "created_at": int(time.time()),
            "keywords": topic.lower().split(),
            "embedding": embedding if embedding is not None else [],
        }

        ref.set(doc)

        logger.info("Knowledge added: %s (%s)", topic, url)
        return True

    # =========================
    # RAW FETCH (FOR VECTOR STORE)
    # =========================
    async def search_knowledge_raw(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Returns raw documents WITHOUT scoring.
        Used ONLY by VectorStore.
        """

        try:
            docs = (
                self.db.collection(self.collection)
                .limit(limit)
                .stream()
            )

            results: List[Dict[str, Any]] = []

            for doc in docs:
                data = doc.to_dict()
                if not data:
                    continue

                data["embedding"] = data.get("embedding") or []
                results.append(data)

            logger.info("Firestore raw fetch: %s docs", len(results))

            return results

        except Exception as e:
            logger.exception("Firestore raw fetch failed: %s", e)
            return []

    # =========================
    # DUPLICATE CHECK (OPTIONAL PUBLIC API)
    # =========================
    async def source_exists(self, url: str) -> bool:
        """
        Fast check using deterministic doc ID.
        """
        doc_id = self._doc_id(url)
        ref = self.db.collection(self.collection).document(doc_id)

        return ref.get().exists