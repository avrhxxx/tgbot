# src/wiki/knowledge/firestore_client.py
# GROUP: wiki
# DESCRIPTION: Firestore knowledge storage (admin-fed RAG memory)

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
    async def add_knowledge(self, topic: str, url: str, content: str) -> None:
        doc = {
            "topic": topic.lower(),
            "url": url,
            "content": content,
            "created_at": int(time.time()),
        }

        self.db.collection(self.collection).add(doc)

        logger.info("Knowledge added: %s (%s)", topic, url)

    # =========================
    # READ
    # =========================
    async def search_knowledge(
        self,
        query: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:

        query = query.lower()

        docs = (
            self.db.collection(self.collection)
            .limit(50)
            .stream()
        )

        results: List[Dict[str, Any]] = []

        for doc in docs:
            data: Optional[Dict[str, Any]] = doc.to_dict()

            if not data:
                continue

            topic = data.get("topic", "")
            content = data.get("content", "")
            url = data.get("url", "")

            if not content:
                continue

            # simple relevance match (MVP)
            if topic and topic in query:
                results.append(
                    {
                        "topic": topic,
                        "content": content,
                        "url": url,
                    }
                )

        logger.info("Firestore results: %s", len(results))

        return results[:limit]