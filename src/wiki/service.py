# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service (RAG v2 - vector + fallback hybrid)

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.firestore_client import FirestoreClient
from src.ai.prompt_engine import build_prompt

from src.wiki.embeddings.client import EmbeddingClient
from src.wiki.embeddings.vector_store import VectorStore

logger = logging.getLogger("wiki.service")

# =========================
# INIT LAYERS
# =========================
firestore = FirestoreClient()
embedder = EmbeddingClient()
vector_store = VectorStore(firestore, embedder)


async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # VECTOR RETRIEVAL (RAG v2)
    # =========================
    try:
        results = await vector_store.search(text, limit=5)
    except Exception:
        logger.exception("Vector search failed")
        results = []

    context_parts = []

    for r in results:
        content = r.get("content", "")
        url = r.get("url", "")
        topic = r.get("topic", "")

        if not content:
            continue

        context_parts.append(
            f"[TOPIC: {topic}]\nSOURCE: {url}\n{content}"
        )

    context = "\n\n---\n\n".join(context_parts).strip()

    if not context:
        context = "[NO RELEVANT MEMORY FOUND]"

    # =========================
    # PROMPT ENGINE
    # =========================
    prompt = build_prompt(text, context)

    # =========================
    # GEMINI CALL
    # =========================
    try:
        response = await asyncio.to_thread(
            gemini_client.generate,
            prompt
        )

        if not response:
            return "No response from AI."

        return response.strip()

    except Exception:
        logger.exception("Wiki service failed")
        return "⚠️ AI service error. Please try again later."