# src/wiki/embeddings/client.py
# GROUP: wiki.embeddings
# DESCRIPTION: Embedding generator for Wiki RAG system (Vertex AI)

import logging
from typing import List

from src.config.config import load_config

logger = logging.getLogger("wiki.embeddings.client")

config = load_config()


class EmbeddingClient:
    """
    Generates embeddings for text using Vertex AI.
    This is the core semantic layer for RAG search.
    """

    def __init__(self):
        self.model_name = getattr(
            config.ai,
            "embedding_model",
            "text-embedding-004"
        )

    # =========================
    # EMBEDDING GENERATION
    # =========================
    def embed(self, text: str) -> List[float]:
        """
        Returns embedding vector for given text.
        """

        if not text or not text.strip():
            return []

        try:
            # Lazy import (faster boot + optional dependency isolation)
            from vertexai.language_models import TextEmbeddingModel

            model = TextEmbeddingModel.from_pretrained(self.model_name)
            result = model.get_embeddings([text])[0]

            return result.values

        except Exception as e:
            logger.exception("Embedding generation failed: %s", e)
            return []

    # =========================
    # BATCH EMBEDDINGS
    # =========================
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds multiple texts at once (used for chunking / learning).
        """

        if not texts:
            return []

        try:
            from vertexai.language_models import TextEmbeddingModel

            model = TextEmbeddingModel.from_pretrained(self.model_name)
            results = model.get_embeddings(texts)

            return [r.values for r in results]

        except Exception as e:
            logger.exception("Batch embedding failed: %s", e)
            return [[] for _ in texts]