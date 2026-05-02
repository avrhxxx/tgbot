# src/wiki/knowledge/firestore_client.py
# GROUP: wiki
# DESCRIPTION: Firestore knowledge storage (admin-fed RAG memory)

import logging
import time
from typing import List

from google.cloud import firestore

from src.google.auth import load_service_account

logger = logging.getLogger("wiki.firestore")


class FirestoreClient:
    def __init__(self):
        credentials = load_service_account()
        self.db = firestore.Client(credentials=credentials)

        # collection name
        self.collection = "knowledge"

    # =========================
    # WRITE
    # =========================
    async def add_knowledge(self, topic: str, url: str, content: str) -> None:
        """
        Stores new knowledge entry.
        """

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
    async def search_knowledge(self, query: str, limit: int = 3) -> List[str]:
        """
        Retrieves relevant knowledge by simple topic match.
        (can upgrade later to embeddings)
        """

        query = query.lower()

        docs = (
            self.db.collection(self.collection)
            .limit(20)
            .stream()
        )

        results: List[str] = []

        for doc in docs:
            data = doc.to_dict()

            topic = data.get("topic", "")
            content = data.get("content", "")

            if topic in query:
                results.append(content)

        logger.info("Firestore results: %s", len(results))

        return results[:limit]