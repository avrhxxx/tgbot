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

    async def add_knowledge(self, topic: str, url: str, content: str) -> None:
        doc = {
            "topic": topic.lower().strip(),
            "url": url,
            "content": content,
            "created_at": int(time.time()),
            "keywords": topic.lower().split(),
        }

        self.db.collection(self.collection).add(doc)

        logger.info("Knowledge added: %s (%s)", topic, url)

    # =========================
    # IMPROVED RAG SEARCH (v2)
    # =========================
    async def search_knowledge(
        self,
        query: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:

        q = query.lower()
        query_tokens = set(q.split())

        docs = (
            self.db.collection(self.collection)
            .limit(100)
            .stream()
        )

        results: List[Dict[str, Any]] = []

        for doc in docs:
            data: Optional[Dict[str, Any]] = doc.to_dict()
            if not data:
                continue

            topic = (data.get("topic") or "").lower()
            content = (data.get("content") or "").lower()
            url = data.get("url") or ""

            if not content:
                continue

            score = 0

            # 1. topic match (soft)
            if topic and (topic in q or q in topic):
                score += 4

            # 2. keyword overlap (improved)
            keywords = data.get("keywords") or []
            for k in keywords:
                if k in q:
                    score += 2

            # 3. content overlap (stronger now)
            for t in query_tokens:
                if t in content:
                    score += 1

            # 4. phrase bonus (IMPORTANT FIX)
            if any(len(t) > 4 and t in content for t in query_tokens):
                score += 2

            if score > 0:
                results.append({
                    "topic": topic,
                    "content": data.get("content", ""),
                    "url": url,
                    "score": score,
                })

        results.sort(key=lambda x: x["score"], reverse=True)

        logger.info("Firestore results (scored v2): %s", len(results))

        return results[:limit]