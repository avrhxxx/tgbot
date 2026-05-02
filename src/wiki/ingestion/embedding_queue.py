# src/wiki/ingestion/embedding_queue.py
# GROUP: wiki.ingestion
# DESCRIPTION: Batch embedding queue to prevent quota overflow

import asyncio
from typing import List, Dict

from src.wiki.embeddings.client import EmbeddingClient


class EmbeddingQueue:
    def __init__(self, embedder: EmbeddingClient):
        self.embedder = embedder
        self.queue: List[Dict] = []
        self.lock = asyncio.Lock()

    async def add(self, item: Dict):
        async with self.lock:
            self.queue.append(item)

    async def flush(self):
        """
        Process embeddings in batches (VERY IMPORTANT for quota)
        """
        async with self.lock:
            batch = self.queue[:10]
            self.queue = self.queue[10:]

        if not batch:
            return

        texts = [b["content"] for b in batch]

        embeddings = self.embedder.embed_batch(texts)

        for item, emb in zip(batch, embeddings):
            item["embedding"] = emb