# src/wiki/embeddings/vector_store.py
# GROUP: wiki.embeddings
# DESCRIPTION: Vector similarity search engine for RAG retrieval (Cosine similarity)

import logging
import math
from typing import List, Dict, Any, Tuple

logger = logging.getLogger("wiki.embeddings.vector_store")

MIN_SCORE = 0.2


# =========================
# COSINE SIMILARITY
# =========================
def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b, strict=True))

    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


# =========================
# VECTOR STORE
# =========================
class VectorStore:
    """
    Simple in-memory + Firestore-backed vector ranking layer.
    (MVP version before moving to proper vector DB)
    """

    def __init__(self, firestore_client, embedding_client):
        self.firestore = firestore_client
        self.embedder = embedding_client

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search over Firestore knowledge base.
        """

        if not query:
            return []

        query_vec = self.embedder.embed(query)

        if not query_vec:
            logger.warning("Empty query embedding")
            return []

        try:
            docs = await self.firestore.search_knowledge_raw(limit=100)
        except Exception as e:
            logger.exception("Firestore fetch failed: %s", e)
            return []

        scored: List[Tuple[float, Dict[str, Any]]] = []
        seen_urls = set()

        for d in docs:
            embedding = d.get("embedding")

            if not embedding or not isinstance(embedding, list):
                continue

            url = d.get("url")

            if url:
                if url in seen_urls:
                    continue
                seen_urls.add(url)

            score = _cosine_similarity(query_vec, embedding)

            if score >= MIN_SCORE:
                scored.append((score, d))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = [item[1] for item in scored[:limit]]

        logger.info("Vector search results: %s", len(results))

        return results