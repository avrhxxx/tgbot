# src/wiki/service.py
# GROUP: wiki
# DESCRIPTION: AI Wiki service (RAG v2 - vector-based orchestration)

import logging
import asyncio

from src.ai.gemini import gemini_client
from src.wiki.guard import is_game_related, build_redirect_message
from src.wiki.knowledge.firestore_client import FirestoreClient
from src.ai.prompt_engine import build_prompt

# 👉 NEW: vector layer (musisz mieć ten moduł)
from src.ai.embeddings import vector_store

logger = logging.getLogger("wiki.service")

firestore = FirestoreClient()


async def answer_wiki_question(text: str) -> str:
    logger.info("Game query received: %s", text)

    if not text or not text.strip():
        return "Please ask a question about Tiles Survive!."

    if not is_game_related(text):
        return build_redirect_message()

    # =========================
    # VECTOR RETRIEVAL (NEW CORE)
    # =========================
    try:
        results = vector_store.search(text, top_k=5)
    except Exception:
        logger.exception("Vector search failed")
        results = []

    context_parts = []

    # =========================
    # BUILD RAG CONTEXT
    # =========================
    for r in results:
        content = r.get("content", "")
        metadata = r.get("metadata", {})

        if not content:
            continue

        topic = metadata.get("topic", "")
        url = metadata.get("url", "")

        context_parts.append(
            f"[TOPIC: {topic}]\nSOURCE: {url}\n{content}"
        )

    context = "\n\n---\n\n".join(context_parts).strip()

    if not context:
        context = "[NO RELEVANT MEMORY FOUND]"

    # =========================
    # PROMPT ENGINE (RAG-AWARE)
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