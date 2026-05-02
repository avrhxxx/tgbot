# src/wiki/knowledge/firestore_client.py

import logging
import time
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
    # WRITE
    # =========================
    async def add_knowledge(
        self,
        topic: str,
        url: str,
        content: str,
        embedding: Optional[List[float]] = None,
    ) -> None:
        """
        Stores knowledge entry with optional embedding (RAG v2 ready).
        """

        doc = {
            "topic": topic.lower().strip(),
            "url": url,
            "content": content,
            "created_at": int(time.time()),
            "keywords": topic.lower().split(),
            "embedding": embedding if embedding is not None else [],
        }

        self.db.collection(self.collection).add(doc)

        logger.info("Knowledge added: %s (%s)", topic, url)

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

                # normalize embedding field
                data["embedding"] = data.get("embedding") or []

                results.append(data)

            logger.info("Firestore raw fetch: %s docs", len(results))

            return results

        except Exception as e:
            logger.exception("Firestore raw fetch failed: %s", e)
            return []