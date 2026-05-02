# src/wiki/knowledge/firestore_client.py
# GROUP: wiki
# DESCRIPTION: Firestore knowledge storage (RAG-ready MVP + future embeddings)

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
            "topic": topic.lower().strip(),
            "url": url,
            "content": content,
            "created_at": int(time.time()),
            "keywords": topic.lower().split(),
            # future vector search
            "embedding": None,
        }

        self.db.collection(self.collection).add(doc)

        logger.info("Knowledge added: %s (%s)", topic, url)

    # =========================
    # READ (IMPROVED RAG MVP)
    # =========================
    async def search_knowledge(
        self,
        query: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:

        query_norm = query.lower()
        query_tokens = set(query_norm.split())

        docs = (
            self.db.collection(self.collection)
            .limit(100)
            .stream()
        )

        scored_results: List[Dict[str, Any]] = []

        for doc in docs:
            data: Optional[Dict[str, Any]] = doc.to_dict()

            if not data:
                continue

            topic = (data.get("topic") or "").lower()
            content = data.get("content") or ""
            url = data.get("url") or ""

            if not content:
                continue

            score = 0

            # direct topic match
            if topic and topic in query_norm:
                score += 5

            # keyword overlap
            keywords = data.get("keywords") or []
            for k in keywords:
                if k in query_tokens:
                    score += 2

            # weak content match
            if any(t in content.lower() for t in query_tokens):
                score += 1

            if score > 0:
                scored_results.append(
                    {
                        "topic": topic,
                        "content": content,
                        "url": url,
                        "score": score,
                    }
                )

        # sort by relevance
        scored_results.sort(key=lambda x: x["score"], reverse=True)

        results = scored_results[:limit]

        logger.info("Firestore results (scored): %s", len(results))

        return results